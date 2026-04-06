import re


EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
SPECIAL_REGEX = re.compile(r"[^a-zA-Z0-9]")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))


def is_safe_cron(expr: str) -> bool:
    parts = expr.strip().split()
    if len(parts) != 5:
        return False
    # Keep this permissive; scheduler still validates actual trigger fields.
    return True


def password_policy_errors(password: str) -> list[str]:
    errors: list[str] = []
    if len(password) < 12:
        errors.append("Password must be at least 12 characters.")
    if not any(ch.isupper() for ch in password):
        errors.append("Password must include at least one uppercase letter.")
    if not any(ch.islower() for ch in password):
        errors.append("Password must include at least one lowercase letter.")
    if not any(ch.isdigit() for ch in password):
        errors.append("Password must include at least one number.")
    if not SPECIAL_REGEX.search(password):
        errors.append("Password must include at least one special character.")
    return errors
