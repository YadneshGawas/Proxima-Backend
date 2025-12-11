from app.modules.users.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError
)

from app.modules.hackathons.exceptions import (
    HackathonNotFoundError,
    HackathonCreateError,
    HackathonQueryError,
    Teamsizelimit
)

# Map exception -> (HTTP code, default_message)
ERROR_MAP = {
    UserAlreadyExistsError: (400, "User already exists."),
    InvalidCredentialsError: (401, "Invalid credentials."),
    UserNotFoundError: (404, "User not found."),

    #Hackathon
    HackathonNotFoundError: (404, "Hackathon not found."),
    HackathonQueryError: (500, "Failed to fetch hackathons."),
    HackathonCreateError: (500, "Failed to create hackathon."),
    Teamsizelimit:(400,"min team size should be lower")

  
}
