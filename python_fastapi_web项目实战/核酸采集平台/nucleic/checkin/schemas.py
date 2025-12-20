from pydantic import BaseModel
from typing import Optional, List
from person.schemas import Person

class CheckIn(BaseModel):
    id: Optional[int] = None
    bqbh: str
    bqxh: int
    cjdd: Optional[str]
    cjry: Optional[int] = None
    person_id: Optional[int]
    
    class Config:
        orm_mode = True

class CheckInResponse(CheckIn, Person):
    pass