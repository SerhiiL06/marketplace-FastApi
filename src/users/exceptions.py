class UserAlreadyExists(Exception):
    def __init__(self, email):
        self.email = email


class UserIDError(Exception):
    def __init__(self, id):
        self.id = id


class PasswordDifference(Exception):
    pass
