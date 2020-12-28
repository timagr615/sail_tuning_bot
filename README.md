# sail_tuning_bot
Бот, помогающий в настройке яхты.

## Для использования:

- git clone https://github.com/timagr615/sail_tuning_bot.git
- pip install -r requirements.txt
- Создать файл `config.py` в корневой директории с следующим содержанием:

```python
    from logger.logger import BaseLogger

    BOT_TOKEN = ''
    proxy_url = ''
    ADMIN_ID = int()
    weatherapi_url = 'http://api.weatherapi.com/v1'
    weatherapi_key = ''

    SKIP_UPDATES = True
    DEBUG = True
    LOGFILE = True

    logger = BaseLogger(DEBUG, LOGFILE)
```
