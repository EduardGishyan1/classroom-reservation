from app.database.connection import schedule_collection
from app.schemas.student import MeetingRooms

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
    async def filter_room(name: str | None, room_type: str | None):
        all_rooms = await StudentService.get_all_rooms()
        filtered_rooms = {}

        for room_name, room_list in all_rooms.items():
            is_meeting_room = room_name.lower() in {room.value.lower() for room in MeetingRooms}
            category = "MeetingRoom" if is_meeting_room else "Classroom"

            if name is None and room_type is None:
                filtered_rooms[room_name] = {
                    "category": category,
                    "schedules": room_list
                }
        
            elif name and room_type:
                if name.lower() == room_name.lower() and category.lower() == room_type.lower():
                    filtered_rooms[room_name] = {
                        "category": category,
                        "schedules": room_list
                    }
        
            elif name:
                if name.lower() == room_name.lower():
                    filtered_rooms[room_name] = {
                        "category": category,
                        "schedules": room_list
                    }
        
            elif room_type:
                if category.lower() == room_type.lower():
                    filtered_rooms[room_name] = {
                        "category": category,
                        "schedules": room_list
                    }

        return filtered_rooms