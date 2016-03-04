class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class CredentialError(Error):
    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "Wrong email or password for user: {}".format(self.username)
