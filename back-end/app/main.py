from quart import Quart
from quart_cors import cors
from app.routers.admin import router as admin_router
from app.routers.student import router as student_router
from app.services.student import StudentService
from app.routers.api_key import router as api_router

app = Quart(__name__)
app.secret_key = "1"

# app = cors(app, allow_origin="http://localhost:5173")

@app.websocket("/ws")
async def ws():
    await StudentService.handle_websocket()

app.register_blueprint(admin_router)
app.register_blueprint(student_router)
app.register_blueprint(api_router)

if __name__ == "__main__":
    app.run()