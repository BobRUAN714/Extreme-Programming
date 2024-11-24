from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .database import Base

# 联系人信息关联表
contact_info = Table(
    'contact_info',
    Base.metadata,
    Column('contact_id', Integer, ForeignKey('contacts.id')),
    Column('info_type', String),
    Column('value', String)
)

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_favorite = Column(Boolean, default=False)
    info = relationship("ContactInfo", back_populates="contact")

class ContactInfo(Base):
    __tablename__ = "contact_infos"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    info_type = Column(String)
    value = Column(String)
    contact = relationship("Contact", back_populates="info")