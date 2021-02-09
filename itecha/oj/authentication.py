import hashlib
import time

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication
from werkzeug.security import gen_salt


def check_token(token: str, life=604800):
    user_id, timestamp, salt, token_hash = token.split(",", 4)
    expected_token = hashlib.sha256(
        f"{user_id}{timestamp}{salt}{settings.SECRET_KEY}".encode()
    ).hexdigest()
    if token_hash != expected_token or time.time() - int(timestamp) >= life:
        return None

    return user_id


def generate_token(user: User) -> str:
    timestamp = int(time.time())
    salt = gen_salt(8)
    token = hashlib.sha256(
        f"{user.id}{timestamp}{salt}{settings.SECRET_KEY}".encode()
    ).hexdigest()

    return f"{user.id},{timestamp},{salt},{token}"


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header: str = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        token = auth_header[7:]

        user_id = check_token(token)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

        return (user, token)
