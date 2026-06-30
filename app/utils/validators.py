import re


def strip_whitespace(v: str) -> str:
    """
    Trim leading and trailing whitespace from strings.
    """
    if isinstance(v, str):
        return v.strip()
    return v


def lowercase_email(v: str) -> str:
    """
    Convert email address to lowercase.
    """
    if isinstance(v, str):
        return v.lower()
    return v


def prevent_empty(v: str) -> str:
    """
    Prevent empty strings or strings that become empty after trimming.
    """
    if isinstance(v, str):
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Value cannot be empty or consist only of whitespace.")
        return trimmed
    return v


def validate_password_strength(v: str) -> str:
    """
    Ensure password has at least one letter and one number, and is at least 6 characters long.
    """
    if isinstance(v, str):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit.")
        if not any(c.isalpha() for c in v):
            raise ValueError("Password must contain at least one letter.")
    return v
