import secrets

from argon2 import PasswordHasher

PASSWORD_HASHER = PasswordHasher()


def url_safe_id(length: int) -> str:
    """Used for generating invite Ids, as can't have '-' in them.

    Args:
        length (int)

    Returns:
        str
    """

    allowed_characters = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
    )

    return "".join(secrets.choice(allowed_characters) for _ in range(length))
