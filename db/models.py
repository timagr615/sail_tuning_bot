from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer)
    firstname = Column(String)
    lastname = Column(String)
    tuning = relationship('Tuning')


class Tuning(Base):
    __tablename__ = "tunings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    boat = Column(String)
    sail_firm = Column(String)
    sail_model = Column(String)
    place = Column(String)
    wind = Column(Float)
    gusts = Column(Float)
    wave_height = Column(Float)
    wave_length = Column(String)
    crew_weight = Column(Float)
    mast_rake = Column(Float)
    prebend = Column(Integer)
    tension = Column(Float)
    mast_step = Column(Integer)
    chocks = Column(String)
    spreraders_leng = Column(Integer)
    quality = Column(Integer)
    description = Column(String)


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
