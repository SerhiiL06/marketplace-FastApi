class UserAlreadyExists(Exception):
    def __init__(self, email):
        self.email = email


class PasswordDifference(Exception):
    pass
