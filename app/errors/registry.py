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

from app.modules.registration.exceptions import (
    HackathonNotFoundError,
    RegistrationClosedError,
    InvalidParticipationTypeError,
    DuplicateRegistrationError,
    TeamRequiredError,
    TeamNotFoundError,
    TeamMembershipError,
    TeamSizeError,
    RegistrationNotFoundError,
)

from app.modules.teams.exceptions import *
from werkzeug.exceptions import Forbidden

# Map exception -> (HTTP code, default_message)
ERROR_MAP = {
    UserAlreadyExistsError: (400, "User already exists."),
    InvalidCredentialsError: (401, "Invalid credentials."),
    UserNotFoundError: (404, "User not found."),

    #Hackathon
    HackathonNotFoundError: (404, "Hackathon not found."),
    HackathonQueryError: (500, "Failed to fetch hackathons."),
    HackathonCreateError: (500, "Failed to create hackathon."),
    Teamsizelimit:(400,"min team size should be lower"),
    PermissionError: (403, "Not allowed to perform this action."),

    #teams
    TeamException : (500,"Teams module error"),
    NotTeamOwnerException : (400,"not a owner"),
    MemberAlreadyExistsException : (400,"Team member already exists"),
    MemberNotFoundException : (404,"Teams member not found"),
    TeamNotFoundException : (404,"Team not found"),

    #registrations
    HackathonNotFoundError: (404, "Hackathon not found"),
    RegistrationClosedError: (400, "Registration closed"),
    DuplicateRegistrationError: (409, "Already registered"),
    TeamRequiredError: (400, "Team is required"),
    TeamNotFoundError: (404, "Team not found"),
    TeamMembershipError: (403, "User not in team"),
    TeamSizeError: (400, "Invalid team size"),
    RegistrationNotFoundError: (404, "Registration not found"),

  
}
