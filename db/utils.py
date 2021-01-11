from db.crud import *
from config import *


def show_all_personal_tunings(db: Session, telegram_id: int):
    user = get_user(db, telegram_id)
    tunings = user.tuning
    data = []
    for tuning in tunings:
        data.append([tuning.boat, tuning.sail_firm, tuning.sail_model, tuning.place, tuning.wind,
                     tuning.gusts, tuning.id])
    return data


def show_personal_tuning(db: Session, telegram_id: int):
    user = get_user(db, telegram_id)
    sail_models = []
    locations = []
    qualities = []
    data = {'user': user.telegram_id}
    for tuning in user.tuning:

        if tuning.sail_model not in sail_models:
            sail_models.append(tuning.sail_model)
        loc = tuning.place
        if loc not in locations:
            locations.append(loc)
        if tuning.quality not in qualities:
            qualities.append(tuning.quality)
        data = {
            'sail_models': sail_models,
            'locations': locations,
            'qualities': qualities,
            'success': True,
        }

    if not data.get('success'):
        data['success'] = False
    logger.write(data)
    return data


def choice_filters_for_tuning(data: dict):
    filters = list()
    if len(data['sail_models']) > 1:
        filters.append('По модели паруса')
    if len(data['locations']) > 1:
        filters.append('По месту')
    if len(data['qualities']) > 1:
        filters.append('По качеству завала')
    return filters


def find_personal_tunings_by_filter(db: Session, filters: str, user_id: int):
    data = show_personal_tuning(db, user_id)
    if filters == 'По модели паруса':
        return data['sail_models']
    elif filters == 'По месту':
        return data['locations']
    elif filters == 'По качеству завала':
        return data['qualities']

