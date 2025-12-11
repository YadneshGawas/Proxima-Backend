class HackathonNotFoundError(Exception):
    pass


class HackathonCreateError(Exception):
    """Raised when an unexpected error occurs while creating a hackathon."""
    pass

class HackathonQueryError(Exception):
    """Raised when fetching hackathons fails due to a database error."""
    pass

class Teamsizelimit(Exception):
    pass