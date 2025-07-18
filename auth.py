import bcrypt


def hash_password(password: str) -> str:
    password = password.encode()
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    hashed_password = hashed_password.decode()
    return hashed_password


def check_password(password_user: str, hashed_password_db: str) -> bool:
    password_user = password_user.encode()
    hashed_password_db = hashed_password_db.encode()
    return bcrypt.checkpw(password_user, hashed_password_db)
