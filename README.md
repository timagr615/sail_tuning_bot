# sail_tuning_bot
Бот, помогающий в настройке яхты.
Для поиска в telegram: @sail_tuning_bot
В настоящее время бот находится в разработке.


### Для использования:

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
`BOT_TOKEN` - токен бота в телеграме

`ADMIN_ID` - id владельа токена в телеграме

`weatherapi_key` - api ключ для получения данных о погоде, его можно получить на сайте https://www.weatherapi.com/

`proxy_url` - необязательный параметр. Если хотите использовать proxy, то его следует указать в виде `'http://user:password@ip:port'`

- Запустить бота можно с помощью файла `main.py`
