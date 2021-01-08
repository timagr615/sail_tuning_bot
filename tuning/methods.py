from db import models
from db.crud import get_sails_by_wind
from db.database import SessionLocal


def choice_tuning(sail_firm: str, sail_model: str, wind_speed: float):
    db = SessionLocal()

    for sail in get_sails_by_wind(db, wind_speed):
        if sail.firm == sail_firm and sail.model == sail_model:

            tuning = {'Фирма': sail.firm,
                      'Модель паруса': sail.model,
                      'Ветер': wind_speed,
                      'Ветер завала': str(sail.wind_min)+'-'+str(sail.wind_max),
                      'Завал': sail.mast_rake,
                      'Пребенд': sail.prebend,
                      'Натяжение на штаге': sail.tension,
                      'Дырка в степсе': sail.mast_step,
                      'Упор': sail.chocks,
                      'Длина краспиц': sail.spreraders_leng
                      }
            db.close()
            return tuning
