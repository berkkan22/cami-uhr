import secrets


def generate_api_key():
    return secrets.token_urlsafe(32)  # Generates a 32-byte long token


print(generate_api_key())
