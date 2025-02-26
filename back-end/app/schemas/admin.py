from pydantic import BaseModel, Field
from typing import Optional

class Admin(BaseModel):
  name: str = Field(...,min_length=2,max_length=50)
  srname: str = Field(...,min_length=2,max_length=50)

class BookRoom(BaseModel):
  room_name: str
  start: str
  end: str
  date:str
  capacity: int
  activity: str
  group_name: str
  is_fixed: bool

class CancelBooking(BaseModel):
  room_name: str
  start: str
  end: str

class DeleteStudent(BaseModel):
  email: Optional[str] = None
  phone_number: Optional[str] = None