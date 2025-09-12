import bcrypt
import jwt
from datetime import datetime, timedelta


class JwtUtil:
    def __init__(
        self,
        secret_password_key: str = "default_password_secret",
        secret_authorization_key: str = "default_auth_secret",
        token_expire_minutes: int = 60,
    ):
        self.secret_password_key = secret_password_key
        self.secret_authorization_key = secret_authorization_key
        self.token_expire_minutes = token_expire_minutes

    # Hash password
    def hash_password(self, plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

    # Check password
    def check_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    # Parse ID -> Token
    def parse_id_to_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=self.token_expire_minutes),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, self.secret_authorization_key, algorithm="HS256")

    # Parse Token -> ID
    def parse_token_to_id(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token, self.secret_authorization_key, algorithms=["HS256"]
            )
            return payload.get("user_id")
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
