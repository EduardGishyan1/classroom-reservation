from quart import Blueprint, jsonify

from app.services.student import StudentService

router = Blueprint("students",__name__,url_prefix="/classrooms")

@router.route("/",methods = ["GET"])
async def get_rooms():
  try:
    rooms = await StudentService.get_all_rooms()
    return jsonify(rooms)
  
  except Exception:
    return jsonify({"error": f"An error occurred"}), 500

@router.route("/<type>", methods=["GET"])
@router.route("/<type>/<name>", methods=["GET"])
async def get_room_by_name(name = None,type = None):
  try:
    room = await StudentService.filter_room(name,type) 
    return jsonify(room) 
  except Exception:
    return jsonify({"error": f"An error occurred"}), 500
