import requests


def get_pirate_forecast(key: str, lat: str, lon: str, date=None):
    endpoint = (
        f"https://api.pirateweather.net/forecast/{key}/{lat},{lon}"
    ) if not date else (
        f"https://api.pirateweather.net/forecast/{key}/{lat},{lon},{date}"
    )
    params = {"units": "us", "exclude": "minutely,alerts,flags"}
    try:
        r = requests.get(endpoint, params=params)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None
