class UnrestrictableUser(Exception):
    """
    Exception thrown when user can't be restricted.

    For example - because of their admin status.
    """

    pass


class NotAnInstanceAdmin(Exception):
    """
    Exception thrown when a certain action require an instance admin privilegies,
    but theuser lacks them.
    """

    pass
