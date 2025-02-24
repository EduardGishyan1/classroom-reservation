from quart import session
import secrets

def generate_secret_code_admin(length: int = 6) -> str:
    secret_code = secrets.token_hex(length // 2) 
    return f"0{secret_code}"

def generate_secret_code_student(length: int = 6) -> str:
    secret_code = secrets.token_hex(length // 2) 
    return f"1{secret_code}"

def generate_api_key(length: int = 6) -> str:
    secret_code = secrets.token_hex(length // 2) 
    return secret_code


def get_api_key():
    api_key = session.get("x-api-key")

    if not api_key:
        return None

    return api_key