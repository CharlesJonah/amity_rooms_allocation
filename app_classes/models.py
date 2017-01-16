import os
import sys
from sqlalchemy import Column,Integer, String,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PersonModel(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(250), nullable=False)
    role = Column(String(250), nullable=False)
    wants_accomodation = Column(String(250), nullable=False)
    office_allocated = Column(String(250))
    living_space_allocated = Column(String(250))

class LivingSpaceModel(Base):
    __tablename__ = 'living_space'
    id = Column(Integer, primary_key = True, autoincrement = True)
    room_name = Column(String(250), nullable=False)
    allocated_members = Column(String(250))
    room_type = Column(String(100), nullable=False)
    capacity =Column(Integer)

class OfficeModel(Base):
    __tablename__ = 'offices'
    id = Column(Integer, primary_key = True, autoincrement = True)
    room_name = Column(String(250), nullable=False)
    allocated_members = Column(String(250))
    room_type = Column(String(100), nullable=False)
    capacity =Column(Integer)
def create_db(db_name):
    engine = create_engine('sqlite:///' + db_name)
    Base.metadata.create_all(engine)
    return engine
