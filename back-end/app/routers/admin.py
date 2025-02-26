from quart import Blueprint, request, jsonify, websocket
import websockets
from app.services.admin import AdminService
from app.schemas.admin import DeleteStudent, BookRoom, CancelBooking
from app.utils.check_role import is_admin

from app.services.active_connections import active_connections

router = Blueprint("/admin", __name__, url_prefix="/admins")

@router.route("/book-room", methods = ["POST"])
async def book_room():
  admin = await is_admin()
  if not admin:
    return jsonify({"error":"Not authorizied"}),401
  book_room_info = await request.get_json()
  try:
    book_room_schema = BookRoom(**book_room_info)
  except:
    return jsonify({"error":"Enter valid values for booking"}),400
  try:
    book_room_data = book_room_schema.model_dump()
    booking = await AdminService.book_room(book_room_data)
    return booking
  except:
    return jsonify({"error":"something went wrong"}),400
  
@router.route("/cancel-book", methods = ["POST"])
async def cancel_book():
  admin = await is_admin()
  if not admin:
    return jsonify({"error":"Not authorizied"}),401
  booking_data = await request.get_json()
  booking_schema = CancelBooking(**booking_data)
  cancel_result = await AdminService.cancel_booking(booking_schema)
  return cancel_result

@router.route("/students", methods = ["GET"])
async def all_students():
  try:
    admin = await is_admin()
    if not admin:
      return jsonify({"error":"Not authorizied"}),401
    students = await AdminService.get_all_students()
    return students
  except Exception:
    return jsonify({"error": "An error occurred"}), 500

@router.route("/delete-student", methods = ["DELETE"])
async def delete_student():
    try:
      admin = await is_admin()
      if not admin:
        return jsonify({"error":"Not authorizied"}),401
      student_info = await request.get_json()
      student_info_schema = DeleteStudent(**student_info)
    
      delete_student = await AdminService.delete_student(student_info_schema)
      return delete_student
    except Exception:
      return jsonify({"error":"Something went wrong"}),400

@router.route("/create-student", methods = ["POST"])
async def create_student():
  try:
    admin = await is_admin()
    if not admin:
      return jsonify({"error":"Not authorizied"}),401
    
    arguments = await request.get_json()

    new_student = await AdminService.create_student(arguments)
    return jsonify(new_student)
  
  except Exception:
    return jsonify({"error":"An error occurred"}),400

@router.route("/notifications", methods=["GET"])
async def notifications():
    try:
        async with websockets.connect("ws://127.0.0.1:5000/ws") as ws:
            await ws.send("Admin connected!")
            msg = await ws.recv()
            return jsonify({"message": msg})
    except Exception as e:
        return jsonify({"error": "Failed to connect to WebSocket"}), 500
    
@router.websocket("/ws")
async def admin_ws_connection():
    conn = websocket._get_current_object()
    active_connections.add(conn)
    try:
        while True:
            message = await websocket.receive()
            await websocket.send(f"Message received: {message}")
    except Exception as e:
        return jsonify({"error":f"WebSocket error: {e}"})
    finally:
        active_connections.remove(conn)