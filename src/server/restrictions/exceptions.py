class UnrestrictableUser(Exception):
    """
    Exception thrown when user can't be restricted.

    For example - because of their admin status.
    """

    pass
