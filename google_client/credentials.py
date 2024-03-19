from random import SystemRandom
from typing import Any, Dict
from urllib.parse import urlencode

import jwt
import requests
from attrs import define
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET

from speeday_app.exceptions import ApplicationError

from .settings import (
    GOOGLE_OAUTH2_CLIENT_ID,
    GOOGLE_OAUTH2_CLIENT_SECRET,
    GOOGLE_OAUTH2_PROJECT_ID,
    BASE_BACKEND_URL,
)


@define
class GoogleLoginCredentials:
    client_id: str
    client_secret: str
    project_id: str


@define
class GoogleAccessTokens:
    id_token: str
    access_token: str
    refresh_token: str
    expires_in: int

    def decode_id_token(self) -> Dict[str, str]:
        id_token = self.id_token
        decoded_token = jwt.decode(jwt=id_token, options={"verify_signature": False})
        return decoded_token


class GoogleLoginFlowService:

    API_URI = "/google/callback/"
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/calendar",
        "openid",
    ]

    def __init__(self):
        self._credentials = google_login_get_credentials()

    @staticmethod
    def _generate_state_session_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        # This is how it's implemented in the official SDK
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    def _get_redirect_uri(self):
        domain = BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f"{domain}{api_uri}"

        return redirect_uri

    def get_authorization_url(self):
        redirect_uri = self._get_redirect_uri()

        state = self._generate_state_session_token()

        params = {
            "response_type": "code",
            "client_id": self._credentials.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.SCOPES),
            "state": state,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "select_account",
        }

        query_params = urlencode(params)
        authorization_url = f"{self.GOOGLE_AUTH_URL}?{query_params}"

        return authorization_url, state

    def get_tokens(self, *, code: str) -> GoogleAccessTokens:
        redirect_uri = self._get_redirect_uri()

        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
        data = {
            "code": code,
            "client_id": self._credentials.client_id,
            "client_secret": self._credentials.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        
        }

        response = requests.post(self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

        if not response.ok:
            raise ApplicationError("Failed to obtain access token from Google.")

        tokens = response.json()

        google_tokens = GoogleAccessTokens(
            id_token=tokens["id_token"],
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            expires_in=tokens["expires_in"],
        )

        return google_tokens

    def refresh_tokens(self, *, refresh_token: str) -> GoogleAccessTokens:

        data = {
            "refresh_token": refresh_token,
            "client_id": self._credentials.client_id,
            "client_secret": self._credentials.client_secret,
            "grant_type": "refresh_token",
            "prompt": "consent"
        }

        response = requests.post(self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
        breakpoint()
        if not response.ok:
            raise ApplicationError("Failed to refresh token from Google.")

        tokens = response.json()
        google_tokens = GoogleAccessTokens(
            id_token=tokens["id_token"],
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            expires_in=tokens["expires_in"],
        )

        return google_tokens

    def get_user_info(self, *, google_tokens: GoogleAccessTokens) -> Dict[str, Any]:
        access_token = google_tokens.access_token
        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#callinganapi
        response = requests.get(
            self.GOOGLE_USER_INFO_URL, params={"access_token": access_token}
        )

        if not response.ok:
            raise ApplicationError("Failed to obtain user info from Google.")

        return response.json()


def google_login_get_credentials() -> GoogleLoginCredentials:

    client_id = GOOGLE_OAUTH2_CLIENT_ID
    client_secret = GOOGLE_OAUTH2_CLIENT_SECRET
    project_id = GOOGLE_OAUTH2_PROJECT_ID

    if not client_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_ID missing in env.")

    if not client_secret:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_SECRET missing in env.")

    if not project_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_PROJECT_ID missing in env.")

    credentials = GoogleLoginCredentials(
        client_id=client_id, client_secret=client_secret, project_id=project_id
    )

    return credentials
