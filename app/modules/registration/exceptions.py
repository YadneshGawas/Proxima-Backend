class RegistrationError(Exception):
    """Base class for registration-related errors"""
    pass


class HackathonNotFoundError(RegistrationError):
    pass


class RegistrationClosedError(RegistrationError):
    pass


class InvalidParticipationTypeError(RegistrationError):
    pass


class DuplicateRegistrationError(RegistrationError):
    pass


class TeamRequiredError(RegistrationError):
    pass


class TeamNotFoundError(RegistrationError):
    pass


class TeamMembershipError(RegistrationError):
    pass


class TeamSizeError(RegistrationError):
    pass


class RegistrationNotFoundError(RegistrationError):
    pass
