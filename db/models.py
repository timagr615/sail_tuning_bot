from sqlalchemy import Column, Integer, String, Float
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer)
    firstname = Column(String)
    lastname = Column(String)


class Sail(Base):
    __tablename__ = "sails"
    id = Column(Integer, primary_key=True, index=True)
    firm = Column(String)
    model = Column(String)
    wind_min = Column(Float)
    wind_max = Column(Float)
    mast_rake = Column(Float)
    prebend = Column(Integer)
    tension = Column(String)
    mast_step = Column(Integer)
    chocks = Column(String)
    spreraders_leng = Column(Integer)
