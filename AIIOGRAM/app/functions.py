from aiogram import F, types, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import aiohttp
import app.keyboards as kb
import requests

async def get_city(lat: float, lng: float) -> str:
    url = f"https://api.rasp.yandex.net/v3.0/nearest_settlement/"
    params = {
        "apikey": "c1d59a90-15f5-4a17-a0af-9bc00b62252c",
        "lat": f"{lat}",
        "lng": f"{lng}",
        "distance": "20",
        "format": "json",
    }
    
    async with aiohttp.ClientSession() as session:
        try:                        
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                city_name = data.get('title', 'Невозможно определить город')
                return city_name
        except aiohttp.ClientError as e:
            print(f"Ошибка при получении данных: {str(e)}")

async def get_city_code(city: str) -> str:
    url = f"https://api.rasp.yandex.net/v3.0/stations_list/"
    params = {
        "apikey": "c1d59a90-15f5-4a17-a0af-9bc00b62252c",
        "lang": "ru_RU",
        "format": "json"
    }
    
    async with aiohttp.ClientSession() as session:
        try:                        
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json(content_type='text/html')
                for country in data.get('countries', []):
                    for region in country.get('regions', []):
                        for settlement in region.get('settlements', []):
                            if settlement.get('title', '').lower() == city.lower():
                                return settlement.get('codes', {}).get('yandex_code')
 
        except aiohttp.ClientError as e:
            print(f"Ошибка при получении данных: {str(e)}")
       
            
async def get_flights(code_from: str, code_to: str, date: str) -> list:
    url = f"https://api.rasp.yandex.net/v3.0/search/"
    params = {
        "apikey": "c1d59a90-15f5-4a17-a0af-9bc00b62252c",
        "from": f"{code_from}",
        "to": f"{code_to}",
        "date": f"{date}",
        "lang": "ru_RU",
        "format": "json"
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                if response.status == 404:
                    return []
                response.raise_for_status()
                data = await response.json()
                flights = []
                for segment in data.get('segments', []):
                    thread = segment.get('thread', {})
                    carrier = thread.get('carrier', {})
                    fromm = segment.get('from', {})
                    to = segment.get('to', {})
                    flights.append({
                        'title': carrier.get('title', 'Не указано'),
                        'number': thread.get('number', 'Не указано'),
                        'transport_type': thread.get('transport_type', 'Не указано'),
                        'fromm': fromm.get('title', 'Не указано'),
                        'to': to.get('title', 'Не указано'),
                        'duration': segment.get('duration', 'Не указано'),
                        'departure': segment.get('departure', 'Не указано'),
                        'arrival': segment.get('arrival', 'Не указано'),
                    })
                return flights
        except aiohttp.ClientError as e:
            print(f"Ошибка при получении рейсов: {str(e)}")
            return []
        

async def get_city_suggestion(city: str) -> str:
    url = f"https://suggest-maps.yandex.ru/v1/suggest"
    params = {
        "text": f"{city}",
        "lang": "ru_RU",
        "types": "locality",
        "results": "1",
        "apikey": "0eb13864-496e-4de2-8fe4-5e6541938414"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                data = await response.json()
                suggestions = data.get('results', [])
                if suggestions:
                    suggested_city = suggestions[0]['title']['text']
                    if suggested_city.lower() != city.lower():
                        return suggested_city
                return "none"
        except Exception as e:
            print(f"Ошибка: {e}")
            return "Произошла ошибка при обработке запроса."
      
        
async def get_weather(city_from: float) -> str:
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": f"{city_from}",
        "appid": "99717b305e34d6118e6d81a7acb01431",
        "lang": "ru",
        "units": "metric"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                if response.status == 404:
                    return []
                response.raise_for_status()
                data = await response.json()
                return {
                    "lon": data.get("coord", {}).get("lon", ""),
                    "lat": data.get("coord", {}).get("lat", ""),
                    "temp": data.get("main", {}).get("temp", ""),
                    "feels_like": data.get("main", {}).get("feels_like", ""),
                    "description": data.get("weather", [{}])[0].get("description", ""),
                    "icon": data.get("weather", [{}])[0].get("icon", ""),
                }
        except aiohttp.ClientError as e:
            print(f"Ошибка при получении погоды: {str(e)}")
            return {}
        
async def get_attractions(city_name: str, lat: float, lon: float) -> list[dict]:
    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": "tourism.attraction",
        "filter": f"circle:{lon},{lat},80000",
        "apiKey": "d548c5ed24604be6a9dd0d989631f783",
        "lang": "ru"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()

    attractions = []
    for feature in data.get("features", []):
        prop = feature.get("properties", {})
        attractions.append({
            "name": prop.get("datasource").get("raw").get("name:ru") or prop.get("name"),
            "address": prop.get("address_line2") or prop.get("formatted"),
            "country_code": prop.get("country_code")
        })
    return attractions

async def get_currency(code: str):
    url = f"https://restcountries.com/v3.1/alpha/{code}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 404:
                    return {}
                response.raise_for_status()
                data = await response.json()
                currencies = data[0].get("currencies", {})
                code = list(currencies.keys())[0]
                return code
        except aiohttp.ClientError as e:
            print(f"Ошибка при получении валюты: {str(e)}")
            return {}

async def convert_currency(currency: str):  
    API_KEY = '3b397dbbf9bfdbeec1d2a4c2'
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{currency}/RUB/1"
    async with aiohttp.ClientSession() as session:      
        try:
            async with session.get(url) as response:
                if response.status == 404:
                    return {}
                response.raise_for_status()
                data = await response.json()
                return {
                    "base_code": data.get("base_code", ""),
                    "conversion_result": data.get("conversion_result", "")
                }                           
        except aiohttp.ClientError as e:
            print(f"Ошибка при получении курса: {str(e)}")
            return {}