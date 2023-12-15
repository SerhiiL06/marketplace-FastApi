from passlib.context import CryptContext


class HashedPassword:
    bcrypt = CryptContext(schemes=["bcrypt"])
