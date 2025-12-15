class TeamException(Exception):
    pass


class NotTeamOwnerException(TeamException):
    pass


class MemberAlreadyExistsException(TeamException):
    pass


class MemberNotFoundException(TeamException):
    pass

class TeamNotFoundException(TeamException):
    pass