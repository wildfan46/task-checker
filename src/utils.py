from datetime import datetime, timezone
try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:
    ZoneInfo = None


def local_to_utc(local_dt: datetime, tz_name: str = "America/Chicago"):
    """Convert a naive local datetime to an aware UTC datetime.

    Uses zoneinfo when available; falls back to assuming local_dt is
    already UTC-compatible if zoneinfo is missing.
    """
    if ZoneInfo is not None:
        local = local_dt.replace(tzinfo=ZoneInfo(tz_name))
        return local.astimezone(timezone.utc)
    # fallback: assume local_dt is in UTC-ish (- not ideal).
    return local_dt.replace(tzinfo=timezone.utc)
