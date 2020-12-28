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
