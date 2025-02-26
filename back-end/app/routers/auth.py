from quart import Blueprint,make_response,session,jsonify
from app.services.auth_service import AuthService
from app.utils.util_functions import generate_secret_code_admin,generate_secret_code_student
from app.schemas.student import Roles

router = Blueprint("Auth",__name__,url_prefix = "/auth")

@router.route("/login", methods=["POST"])
async def login():
    try:
      login_answer = await AuthService.login()
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

@router.route("/logout", methods=["GET"])
async def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})