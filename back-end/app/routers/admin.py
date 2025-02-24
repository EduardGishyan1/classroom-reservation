from quart import Blueprint, request, jsonify
from app.services.admin import AdminService
from app.schemas.admin import DeleteStudent, BookRoom, CancelBooking
from app.utils.check_role import is_admin

router = Blueprint("/admin", __name__, url_prefix="/admin")

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
    booking = await AdminService.book_room(book_room_schema)
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