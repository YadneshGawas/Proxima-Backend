class UserAlreadyExistsError(Exception):
    """Exception raised when attempting to create a user that already exists."""
    pass

class UserNotFoundError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

