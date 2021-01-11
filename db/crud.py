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


def get_sails(db: Session):
    return db.query(models.Sail).all()


def get_sails_by_wind(db: Session, wind: float):
    sails = get_sails(db)
    return [s for s in sails if s.wind_min <= wind <= s.wind_max]


def create_tuning(db: Session, message: types.Message, tuning: dict):
    current_user = message['from']
    user = get_user(db, current_user.id)
    '''tuning['user_id'] = user.id
    db_tuning = models.Tuning(**tuning)'''

    db_tuning = models.Tuning(
        user_id=user.id,
        boat=tuning['boat'],
        sail_firm=tuning['sail_firm'],
        sail_model=tuning['sail_model'],
        place=tuning['place'],
        wind=tuning['wind'],
        gusts=tuning['gusts'],
        wave_height=tuning['wave_height'],
        wave_length=tuning['wave_length'],
        crew_weight=tuning['crew_weight'],
        mast_rake=tuning['mast_rake'],
        prebend=tuning['prebend'],
        tension=tuning['tension'],
        mast_step=tuning['mast_step'],
        chocks=tuning['chocks'],
        spreraders_leng=tuning['spreraders_leng'],
        quality=tuning['quality'],
        description=tuning['description'],
    )
    db.add(db_tuning)
    db.commit()
    db.refresh(db_tuning)
    return db_tuning


def find_tuning_by_id(db: Session, tuning_id: int):
    tuning = db.query(models.Tuning).filter(models.Tuning.id == tuning_id).scalar()
    return tuning


def delete_tuning_by_id(db: Session, tuning_id: int):
    db.query(models.Tuning).filter(models.Tuning.id == tuning_id).delete(synchronize_session=False)
    db.commit()


def find_tunings_by_filter(db: Session, filt_name, filt_value, telegram_id: int):
    data = []
    user = get_user(db, telegram_id)
    tunings = db.query(models.Tuning).filter(models.Tuning.user_id == user.id)

    if filt_name == 'sail_model':
        tunings = tunings.filter(models.Tuning.sail_model == filt_value)
    elif filt_name == 'location':
        tunings = tunings.filter(models.Tuning.place == filt_value)
    elif filt_name == 'qualities':
        tunings = tunings.filter(models.Tuning.quality == filt_value)

    for tuning in tunings:
        data.append([tuning.boat, tuning.sail_firm, tuning.sail_model, tuning.place, tuning.wind,
                     tuning.gusts, tuning.id])
    return data
