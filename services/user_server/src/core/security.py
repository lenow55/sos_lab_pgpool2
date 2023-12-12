import bcrypt


async def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password)


def get_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt())
