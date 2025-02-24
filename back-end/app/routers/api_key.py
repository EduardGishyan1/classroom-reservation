from quart import Blueprint
from app.utils.util_functions import generate_api_key

router = Blueprint("API_key",__name__,url_prefix = "/gen")

@router.route("/secret_code",methods = ["GET"])
async def gen_secret_code():
    api_key = generate_api_key()
    return {"api_key":api_key}