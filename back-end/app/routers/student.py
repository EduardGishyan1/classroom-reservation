from quart import Blueprint, request, jsonify, make_response,session
from app.services.student import StudentService
from app.utils.util_functions import generate_secret_code_admin,generate_secret_code_student
from app.utils.check_role import is_student

from app.schemas.student import Roles

router = Blueprint("students",__name__,url_prefix="/classrooms")

@router.route("/",methods = ["GET"])
async def get_rooms():
  try:
    rooms = await StudentService.get_all_rooms()
    return jsonify(rooms)
  
  except Exception:
    return jsonify({"error": f"An error occurred"}), 500

@router.route("/<name>/<type>")
async def get_room_by_name(name,type):
  try:
    room = await StudentService.filter_room(name,type) 
    return jsonify(room) 
  except Exception:
    return jsonify({"error": f"An error occurred"}), 500

@router.route("/login", methods=["POST"])
async def login():
    try:
        login_answer = await StudentService.login()
        if login_answer.status_code == 200: 
            answer = await login_answer.json
            response = await make_response(answer)
            response.status_code = 200
            
            if login_answer.role == Roles.STUDENT.value:
              secret_code = generate_secret_code_student()
              response.headers["x-api-key"] = secret_code
              session["x-api-key"] = secret_code

            elif login_answer.role == Roles.ADMIN.value:
              secret_code = generate_secret_code_admin()
              response.headers["x-api-key"] = secret_code
              session["x-api-key"] = secret_code

            return response  
        
        return login_answer  
    
    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500

@router.route("/book-room", methods=["POST"])
async def book_room():
    try:
        is_student = await is_student()
        if not is_student:
           return jsonify({"error":"Not authorizied"}),401
        
        booking_message = await StudentService.book_room()
        return jsonify(booking_message)
    except Exception:
        return jsonify({"error": "Something went wrong"}), 500

@router.route("/logout", methods=["GET"])
async def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})