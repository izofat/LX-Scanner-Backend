import bcrypt
from pydantic import BaseModel, field_validator

from lx_scanner_backend.api import exceptions


class User(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def username_length(cls, v):
        if len(v) < 6:
            raise exceptions.UsernameTooShort()
        if len(v) > 30:
            raise exceptions.UsernameTooLong()

        return v

    @field_validator("password")
    @classmethod
    def password_length(cls, v):
        if len(v) < 4:
            raise exceptions.PasswordTooShort()
        if len(v) > 300:
            raise exceptions.PasswordTooLong()

        return v

    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()

    def decrypt_password(self, decrypted_password: str):
        return bcrypt.checkpw(decrypted_password.encode(), self.password.encode())
