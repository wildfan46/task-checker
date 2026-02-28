from datetime import datetime, timedelta
from typing import Dict, Optional
from utils import local_to_utc


def _today_date_utc():
    return datetime.utcnow().date()


def check_weed_task(
    forecast, project_id: str, section_id: str
) -> Dict:
    """Return candidate list for spot treat weeds (may require lookback)."""
    daily = forecast.get("daily", {}).get("data", [])
    skip = False
    for day in daily[:3]:
        precip = day.get("precipProbability", 0)
        if precip != 0:
            print("Precipitation expected, skipping weed task")
            skip = True
            break
    high = daily[0].get("temperatureHigh", 0)
    if not skip and (55 <= high <= 85):
        return {
            "name": "Spot Treat Weeds",
            "project_id": project_id,
            "section_id": section_id,
            "lookback_days": 21
        }
    else:
        print("Temperature not suitable for weed treatment")
    return None


def check_grilling_task(
    forecast, project_id: str, section_id: str
) -> Dict:
    """Return candidate list for grilling if evening looks good."""
    today = _today_date_utc()
    hourly = forecast.get("hourly", {}).get("data", [])
    evening = [
        h for h in hourly
        if datetime.utcfromtimestamp(h["time"]).date() == today and
        16 <= datetime.utcfromtimestamp(h["time"]).hour <= 20
    ]
    if not evening:
        print("Evening weather forecast not received")
        return None

    avg_temp = sum(h["temperature"] for h in evening) / len(evening)
    max_wind = max(h.get("windSpeed", 0) for h in evening)
    precip = any(h.get("precipProbability", 0) > 0 for h in evening)

    if 45 < avg_temp < 85 and max_wind < 5 and not precip:
        return {
            "name": "Grill dinner tonight",
            "project_id": project_id,
            "section_id": section_id
        }
    else:
        print("Weather not condusive to grilling dinner tonight")
    return None


def check_walk_task(
    forecast, project_id: str, section_id: str
) -> Dict:
    """Return candidate(s) for a walk or general physical activity."""
    today = _today_date_utc()
    hourly = forecast.get("hourly", {}).get("data", [])

    def window_score(start_hour: int, end_hour: int) -> Optional[float]:
        hours = [
            h for h in hourly
            if datetime.utcfromtimestamp(h["time"]).date() == today and
            start_hour <= datetime.utcfromtimestamp(h["time"]).hour <= end_hour
        ]
        if not hours or any(h.get("precipProbability", 0) > 0 for h in hours):
            return None
        temps = [h["temperature"] for h in hours]
        if any(t < 45 or t > 85 for t in temps):
            return None
        avg_temp = sum(temps) / len(temps)
        return abs(avg_temp - 70)

    morning = window_score(9, 11)
    afternoon = window_score(14, 18)

    if morning is None and afternoon is None:
        print("No suitable time windows for a walk today")
        return {
            "name": "Physical Activity of some sort",
            "project_id": project_id,
            "section_id": section_id
        }

    if morning is None:
        chosen = ("afternoon", 14)
    elif afternoon is None:
        chosen = ("morning", 9)
    else:
        chosen = ("morning", 9) if morning <= afternoon else ("afternoon", 14)

    window_name, start_hour = chosen
    due_local = datetime.now().replace(
        hour=start_hour, minute=0, second=0, microsecond=0
    )
    due_utc = local_to_utc(due_local)
    return {
        "name": f"Go for a walk ({window_name})",
        "project_id": project_id,
        "section_id": section_id,
        "due_datetime": due_utc.isoformat()
    }


def check_grass_task(
    forecast, project_id: str, section_id: str
) -> Dict:
    """Return candidate for cutting grass (honor lookback when creating)."""
    today = _today_date_utc()
    # ensure today's forecasted high is above 50°F
    daily = forecast.get("daily", {}).get("data", [])
    today_daily = next(
        (
            d for d in daily
            if datetime.utcfromtimestamp(d["time"]).date() == today
        ),
        None
    )
    if today_daily and today_daily.get("temperatureHigh", 0) <= 50:
        print("Temperature not warm enough to cut grass today")
        return None
    hourly = forecast.get("hourly", {}).get("data", [])
    today_hours = [
        h for h in hourly
        if datetime.utcfromtimestamp(h["time"]).date() == today
    ]
    if any(h.get("precipProbability", 0) > 0 for h in today_hours):
        print("Weather calling for precipitation today")
        return None
    return {
        "name": "Cut Grass",
        "project_id": project_id,
        "section_id": section_id,
        "lookback_days": 5
    }


def check_driveway_snow_task(
    forecast, project_id: str, section_id: str
) -> Dict:
    yesterday = _today_date_utc() - timedelta(days=1)
    hourly = forecast.get("hourly", {}).get("data", [])
    snow_hours = [
        h for h in hourly
        if datetime.utcfromtimestamp(h["time"]).date() == yesterday and
        datetime.utcfromtimestamp(h["time"]).hour >= 17 and
        h.get("precipType") == "snow"
    ]
    if snow_hours:
        return {
            "name": "Clear driveway (snow event last night)",
            "project_id": project_id,
            "section_id": section_id
        }
    else:
        print("No snow in the forecast")
    return None
