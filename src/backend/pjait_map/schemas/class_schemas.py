from pydantic import BaseModel

class Position(BaseModel):
    x: int
    y: int

class ClassLocation(BaseModel):
    room: str
    file: str
    pos: Position # x and y coordinates on the image

class ClassInfo(BaseModel):
    subject_id: int
    room_id: int
    weekday: int
    start: str # start and end in "hh:mm" format,
    end: str   # so for now they are str

class ScheduleInfo(BaseModel):
    schedule_id: int
    data: ClassInfo
