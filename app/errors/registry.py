from app.modules.users.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError
)

# Map exception -> (HTTP code, default_message)
ERROR_MAP = {
    UserAlreadyExistsError: (400, "User already exists."),
    InvalidCredentialsError: (401, "Invalid credentials."),
    UserNotFoundError: (404, "User not found."),

  
}
