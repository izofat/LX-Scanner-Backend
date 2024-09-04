from typing import Optional

import bcrypt
from pydantic import BaseModel, Field, field_validator

from lx_scanner_backend import exceptions


class User(BaseModel):
    id: Optional[int] = Field(default=None)
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


class ScannerInput(BaseModel):
    id: int
    user_id: int
    expected_output: str
    file_name: str
    input_language: str = "en"

    @field_validator("expected_output")
    @classmethod
    def is_expected_output_exist(cls, v):
        if not v:
            raise exceptions.ExpectedOutputNotExist()

        return v

    @field_validator("input_language")
    @classmethod
    def is_input_language_exist(cls, v):
        if not v:
            raise exceptions.InputLanguageNotExist()

        return v
