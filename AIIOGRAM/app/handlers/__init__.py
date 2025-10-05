from . import start, city_from, city_to, flights, weather, attractions, currency

routers = [
    start.router,
    city_from.router,
    city_to.router,
    flights.router,
    weather.router,
    attractions.router,
    currency.router,
]
