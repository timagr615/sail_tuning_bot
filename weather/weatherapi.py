import aiohttp


class WeatherApi:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    async def api_call(self, session, api_method: str, params: dict = None):
        url = '/'.join([self.api_url, api_method])
        async with session.get(url=url, params=params) as response:
            assert response.status == 200
            return await response.json()


class WeatherApiV1(WeatherApi):
    def __init__(self, api_url_v1, api_key):
        WeatherApi.__init__(self, api_url_v1, api_key)

    # Текущая погода, q - название города, либо геопозиция
    async def current(self, q: str):
        async with aiohttp.ClientSession() as session:
            api_method = 'current.json'
            params = {'key': self.api_key, 'q': q}
            response = await self.api_call(session, api_method, params)
            return response
