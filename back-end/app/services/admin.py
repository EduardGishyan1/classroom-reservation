import aiohttp
import pytz 
from datetime import datetime
from quart import jsonify
from mongoengine import connect

from app.database.connection import user_collection,schedule_collection
from app.models.shcedules import Room, Schedule
from app.models.users import User
from app.schemas.admin import BookRoom, CancelBooking
from app.schemas.student import UserSchema

from quart import websocket
from app.services.active_connections import active_connections

utc_timezone = pytz.UTC  

connect("classrooms", host="mongodb://localhost:27017/classrooms")

class AdminService:
  @staticmethod
  async def get_all_students():
    users = await user_collection.find().to_list(length=None)
    if not users:
      return jsonify({"error":"Student not found"}), 404
    for user in users:
        user["_id"] = str(user["_id"])
    return users
    
  @staticmethod
  async def delete_student(student_info):
    email = student_info.email
    phone_number = student_info.phone_number

    if not email and not phone_number:
      return jsonify({"error": "Name, Email or Phone Number is required"}),400

    try:
      if email:
        user = await user_collection.find_one({"email":email})
        if user:
          user_collection.delete_one({"email":email})
          return jsonify({"message": "Student deleted successfully"}), 200
            
      if phone_number:
        user = await user_collection.find_one({"phone_number":phone_number})
        if user:
          user_collection.delete_one({"phone_number":phone_number})
          return jsonify({"message": "Student deleted successfully"}), 200

      return jsonify({"error": "Student not found"}), 404

    except Exception:
      return jsonify({"error": f"An error occurred"}), 500
    
  @staticmethod
  async def book_room(book_room_info: BookRoom):
    room = Room(name=book_room_info.room_name, capacity=book_room_info.capacity)

    start = datetime.strptime(book_room_info.start, "%H:%M").replace(second=0, microsecond=0)
    end = datetime.strptime(book_room_info.end, "%H:%M").replace(second=0, microsecond=0)

    start = utc_timezone.localize(start)
    end = utc_timezone.localize(end)

    schedule = Schedule(
        rooms=room, start=start, end=end, group_name=book_room_info.group_name, activity=book_room_info.activity
    )
    schedule_dict = schedule.to_dict()
    await schedule_collection.insert_one(schedule_dict)

    return jsonify({"message": "Room booked successfully"})

  @staticmethod
  async def cancel_booking(cancel_room_info: CancelBooking):
    start_time = datetime.strptime(cancel_room_info.start, "%H:%M").replace(second=0, microsecond=0)
    end_time = datetime.strptime(cancel_room_info.end, "%H:%M").replace(second=0, microsecond=0)

    start_time = utc_timezone.localize(start_time)
    end_time = utc_timezone.localize(end_time)

    result = await schedule_collection.delete_one({
        "rooms.name": cancel_room_info.room_name,
        "start": start_time,
        "end": end_time
    })

    if result.deleted_count:
        return jsonify({"message": "Booking deleted successfully"}), 200
    else:
        return jsonify({"error": "No matching booking found"}), 404
    
  @staticmethod
  async def create_student(arguments):
    
    async with aiohttp.ClientSession() as session:
      async with session.get("http://127.0.0.1:5000/gen/secret_code") as response:
        if response.status == 200:
          data = await response.json()
          arguments["secret_code"] = data.get("api_key")  
        else:
          return jsonify({"error": "Failed to generate API key"}), 500

    user = UserSchema(**arguments)
    user_data = user.model_dump() if hasattr(user, "dict") else vars(user)

    user_db = User(**user_data).to_dict()
    await user_collection.insert_one(user_db)
    return {"message":f"user added successfully with name {user.name} and with unique code {user.secret_code}"}
  
  staticmethod
  async def handle_websocket():
        conn = websocket._get_current_object()  # Get current WebSocket connection
        active_connections.add(conn)  # Add connection to active_connections
        try:
            while True:
                message = await websocket.receive()  # Wait for messages from WebSocket
                print(f"Received message: {message}")
                await websocket.send(f"Echo: {message}")  # Echo the received message back
        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            active_connections.remove(conn)