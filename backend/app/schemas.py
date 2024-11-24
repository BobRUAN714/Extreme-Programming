from typing import List, Optional
from pydantic import BaseModel

class ContactInfoBase(BaseModel):
    info_type: str
    value: str

class ContactInfoCreate(ContactInfoBase):
    pass

class ContactInfo(ContactInfoBase):
    id: int
    contact_id: int

    class Config:
        orm_mode = True

class ContactBase(BaseModel):
    name: str
    is_favorite: bool = False

class ContactCreate(ContactBase):
    info: List[ContactInfoCreate] = []

class Contact(ContactBase):
    id: int
    info: List[ContactInfo] = []

    class Config:
        orm_mode = True