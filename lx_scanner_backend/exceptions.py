class NotAuthenticatedException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class NotFoundException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class UserAlreadyExists(NotAuthenticatedException):
    """Raised when the user already exists in the database"""

    def __init__(self, message="User already exists"):
        super().__init__(message, 409)


class InvalidCredentials(NotAuthenticatedException):
    """Raised when the user's username and password didn't match"""

    def __init__(self, message="Invalid credentials"):
        super().__init__(message, 401)


class UsernameTooLong(NotAuthenticatedException):
    """Raised when the username is too long"""

    def __init__(self, message="Username is too long"):
        super().__init__(message, 400)


class UsernameTooShort(NotAuthenticatedException):
    """Raised when the username is too short"""

    def __init__(self, message="Username is too short"):
        super().__init__(message, 400)


class PasswordTooLong(NotAuthenticatedException):
    """Raised when the password is too long"""

    def __init__(self, message="Password is too long"):
        super().__init__(message, 400)


class PasswordTooShort(NotAuthenticatedException):
    """Raised when the password is too short"""

    def __init__(self, message="Password is too short"):
        super().__init__(message, 400)


class ExpectedOutputNotExist(NotAuthenticatedException):
    """Raised when the expected output is not exist"""

    def __init__(self, message="Expected output is not exist"):
        super().__init__(message, 400)


class InputLanguageNotExist(NotAuthenticatedException):
    """Raised when the input language is not exist"""

    def __init__(self, message="Input language is not exist"):
        super().__init__(message, 400)
