from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from app.models.shcedules import ActivityType

class Roles(Enum):
	STUDENT = "student"
	ADMIN = "admin"


class UserSchema(BaseModel):
	name: str = Field(...,min_length=2,max_length=50)
	surname: str = Field(...,min_length=2,max_length=50)
	email: EmailStr
	phone_number: str
	role: Roles
	group_name: str = Field(...,min_length=2)
	secret_code:str

class BookingNotification(BaseModel):
  room_name: str
  start: str
  end: str
  date:str
  capacity: int
  activity: ActivityType
  group_name: str

class CancelRoom(BaseModel):
	room_name: str
	group_name: str
	description: str

class LoginUser(BaseModel):
	secret_code:str
	name:str

class MeetingRooms(Enum):
	VADER = "vader"
	SIRIUS = "sirius"
	PROXIMA = "proxima"