from quart import jsonify, request
from app.schemas.student import LoginUser
from app.database.connection import user_collection

class AuthService:
    @staticmethod
    async def login():
      try:
        arguments = await request.get_json()
        login_data = LoginUser(**arguments)
        existing_user = await user_collection.find_one({"secret_code": login_data.secret_code, "name": login_data.name})
        if existing_user:
            response = jsonify({"message": "Logged in successfully"})
            response.status_code = 200  
            response.role = existing_user.get("role")
            return response

        response = jsonify({"error": "Invalid credentials"})
        response.status_code = 400
        return response
      
      except Exception as e:
        response = jsonify({"error": f"An error occurred during login: {str(e)}"})
        response.status_code = 500
        return response