import requests
from config import API_KEY
from constants import CITY, ENDPOINT, LANG, UNITS
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title='Weather app')
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/weather/", response_class=HTMLResponse)
def get_weather(request: Request, city: str = CITY, lang: str = LANG, units: str = UNITS):
    query_text = f'{ENDPOINT}?q={city}&lang={lang}&APPID={API_KEY}&units={units}'

    try:
        response = requests.get(query_text).json()

        if response:
            description = response.get('weather')[0].get('description').capitalize()
            weather_main = response.get('main')
            temperature = round(weather_main.get('temp'))
            feels_like = round(weather_main.get('feels_like'))
            humidity = weather_main.get('humidity')
            wind_speed = round(response.get('wind').get('speed'))
            return templates.TemplateResponse(
                'weather.html',
                {
                    'request': request,
                    'city': response.get('name'),
                    'description': description,
                    'temperature': temperature,
                    'feels_like': feels_like,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                }
            )
        else:
            return {'Не удалось получить данные о погоде.'}
    except requests.RequestException:
        return {'message': 'Ошибка при выполнении запроса к API погоды.'}
