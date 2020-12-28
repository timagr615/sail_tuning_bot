def current_weather_format(forecast):
    location = forecast['location']
    current = forecast['current']
    location_text = 'Место: ' + location['name'] + '\n' + 'Регион: ' + location['region'] + '\n' + 'Страна: ' + \
                    location['country'] + '\n' + 'Широта: ' + str(location['lat']) + '; ' + 'Долгота: ' + str(
        location['lon']) + '\n' + 'Текущее время: ' + location['localtime']

    wind_kt = round(current['wind_kph']*0.54, 1)
    gusts_kt = round(current['gust_kph']*0.54, 1)
    current_text = 'Текущие погодные условия для данного места: \n' + 'Температура: ' + str(
        current['temp_c']) + u'°C' + '\n' + 'Ветер: ' + str(wind_kt) + 'kt \n' + 'Порывы ветра: ' + str(
        gusts_kt) + 'kt \n' + 'Направление ветра: ' + current['wind_dir'] + ' ' + str(
        current['wind_degree']) + u'°' + '\n'

    return [location_text, current_text, location]
