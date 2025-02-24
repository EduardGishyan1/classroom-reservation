from quart import jsonify, request, websocket
from app.database.connection import schedule_collection, user_collection
from app.schemas.student import MeetingRooms, LoginUser

active_connections = set()

class StudentService:
    @staticmethod
    async def get_all_rooms():
      all_schedules = await schedule_collection.find().to_list(length=None)
      room_info = {}

      for schedule in all_schedules:
        room_name = schedule["rooms"]["name"]

        room = {
            "start": schedule.get("start"),
            "end": schedule.get("end"),
            "group_name": schedule.get("group_name")
        }

        if room_name not in room_info:
            room_info[room_name] = []
        
        room_info[room_name].append(room)
    
      return room_info

    @staticmethod
    async def filter_room(name: str, room_type: str):
        all_rooms = await StudentService.get_all_rooms()
        filtered_rooms = {}

        for room_name, room_list in all_rooms.items():
            is_meeting_room = room_name.lower() in {room.value.lower() for room in MeetingRooms}
            category = "MeetingRoom" if is_meeting_room else "Classroom"
            if name.lower() == room_name.lower() and category.lower() == room_type.lower():
                filtered_rooms[room_name] = {
                    "category": category,
                    "schedules": room_list
                }

        return filtered_rooms
    
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
      
    async def book_room():
        admin = {"role": "admin"}
        existing_admins = await user_collection.find(admin).to_list(length=None)

        for conn in list(active_connections): 
            try:
                await conn.send_json({"message": "Hello, room booked!"})
            except Exception as e:
                print(f"Error sending message: {e}")
                active_connections.remove(conn)  

        return {"message": "Room booked successfully!"}

    @staticmethod
    async def handle_websocket():
        conn = websocket._get_current_object()
        active_connections.add(conn)
        try:
            while True:
                await websocket.receive()  
        except:
            pass
        finally:
            active_connections.remove(conn)  