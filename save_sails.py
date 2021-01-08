from db import crud
from db.database import SessionLocal


with open("dbb", "r") as file:

    for line in file:
        data = line.split(',')[1:]
        data[-1] = data[-1].replace('\n', '')
        if data[0] == 'firm':
            continue
        sail = {
            'firm': data[0],
            'model': data[1],
            'wind_min': float(data[2]),
            'wind_max': float(data[3]),
            'mast_rake': float(data[4]),
            'prebend': int(data[5]),
            'tension': data[6],
            'mast_step': int(data[7]),
            'chocks': data[8],
            'spreraders_leng': int(data[9])
        }
        db = SessionLocal()
        crud.create_sail(db, sail)
        db.close()
