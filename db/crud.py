from aiogram import types
from sqlalchemy.orm import Session
from . import models


def get_user(db: Session, telegram_id: int):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, message: types.Message):
    current_user = message['from']
    if not current_user.last_name:
        current_user.last_name = ''
    if not get_user(db, current_user.id):
        db_user = models.User(telegram_id=current_user.id,
                              firstname=current_user.first_name,
                              lastname=current_user.last_name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


def create_sail(db: Session, sail: dict):
    db_sail = models.Sail(
        firm=sail['firm'],
        model=sail['model'],
        wind_min=sail['wind_min'],
        wind_max=sail['wind_max'],
        mast_rake=sail['mast_rake'],
        prebend=sail['prebend'],
        tension=sail['tension'],
        mast_step=sail['mast_step'],
        chocks=sail['chocks'],
        spreraders_leng=sail['spreraders_leng']
    )
    db.add(db_sail)
    db.commit()
    db.refresh(db_sail)
    return db_sail
