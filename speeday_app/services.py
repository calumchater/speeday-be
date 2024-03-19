from typing import Tuple

from django.db import transaction
from django.core.management.utils import get_random_secret_key

from datetime import datetime, timedelta
from .models import User
from google_client.credentials import GoogleAccessTokens


def user_create(email, password=None, **extra_fields) -> User:
    extra_fields = {
        'is_staff': False,
        'is_superuser': False,
        **extra_fields
    }

    user = User(email=email, **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user


def user_create_superuser(email, password=None, **extra_fields) -> User:
    extra_fields = {
        **extra_fields,
        'is_staff': True,
        'is_superuser': True
    }

    user = user_create(email=email, password=password, **extra_fields)

    return user


def user_record_login(*, user: User) -> User:
    user.last_login = datetime.now()
    user.save()

    return user


@transaction.atomic
def user_change_secret_key(*, user: User) -> User:
    user.secret_key = get_random_secret_key()
    user.full_clean()
    user.save()

    return user


@transaction.atomic
def user_get_or_create(email: str) -> User:
    user = User.objects.filter(email=email).first()

    if user:
        return user

    return user_create(email=email)

def user_set_token_info(*, user: User, google_tokens: GoogleAccessTokens) -> User:
    user.access_token = google_tokens.access_token
    user.refresh_token = google_tokens.refresh_token
    user.refresh_token_expiry_date = datetime.now() + timedelta(seconds= google_tokens.expires_in)

    user.save()

    return user