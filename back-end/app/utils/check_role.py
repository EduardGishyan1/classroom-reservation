from app.utils.util_functions import get_api_key

async def is_admin():
    api_key = get_api_key()
    if api_key:
        if api_key[0] != "0":
            return False
        return True

async def is_student():
    api_key = get_api_key()
    if api_key:
        if api_key[0] != "1":
            return False
        return True
