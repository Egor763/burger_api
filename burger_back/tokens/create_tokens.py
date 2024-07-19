import datetime
import jwt
from django.conf import settings


# функция добавления access_token
def generate_access_token(user):
    # словарь access_token
    access_token_payload = {
        "user_email": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=100),
        # "iat": datetime.datetime.utcnow(),
    }
    # access_token кодируется в секретный ключ
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return access_token


# функция добавления refresh_token
def generate_refresh_token(user):
    # словарь refresh_token
    refresh_token_payload = {
        "user_email": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=100),
        "iat": datetime.datetime.utcnow(),
    }

    # refresh_token кодируется в секретный ключ
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm="HS256"
    )

    return refresh_token
