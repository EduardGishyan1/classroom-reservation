from quart import Quart
from app.routers.admin import router as admin_router
from app.routers.student import router as student_router
from app.routers.auth import router as auth_router
from app.routers.api_key import router as api_router
from app.config.settings import settings

app = Quart(__name__)
app.secret_key = settings.SECRET_KEY

app.register_blueprint(admin_router)
app.register_blueprint(student_router)
app.register_blueprint(api_router)
app.register_blueprint(auth_router)