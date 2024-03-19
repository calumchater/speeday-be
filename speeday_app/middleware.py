from django.shortcuts import redirect

from google_client.credentials import GoogleLoginFlowService

from django.utils.deprecation import MiddlewareMixin


class GoogleAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print(request.path)
        if request.path != "/google/redirect/" and request.path != "/google/callback/":
            refresh_token = request.COOKIES.get("refresh_token")
            if (
                refresh_token is None
            ):  # Cookie is not set - user is definitely not logged in
                return        # redirect("google-login-redirect")
            else:
                # Let's always try and refresh the token to make session as long as possible, this means we also need to add the refresh token back to the response cookie
                tokens = GoogleLoginFlowService().refresh_tokens(
                    refresh_token=refresh_token
                )
                if tokens is not None:
                    request.session['access_token'] = tokens.access_token
                else:
                    return    # redirect("google-login-redirect")

    def process_response(self, request, response):
        if response is not None:
            return response
