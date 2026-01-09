from datetime import datetime, timezone, timedelta

def time_ago(created_at):
    """
    Returns a human-readable relative time string like '2m', '1h', '1D'
    """
    now = datetime.now(timezone.utc)

    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    diff = now - created_at

    seconds = diff.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24

    if seconds < 60:
        return f"{int(seconds)}s"
    elif minutes < 60:
        return f"{int(minutes)}m"
    elif hours < 24:
        return f"{int(hours)}h"
    else:
        return f"{int(days)}d"
    
def is_user_online(user):
    if not user.last_seen:
        return False
    return datetime.utcnow() - user.last_seen < timedelta(minutes=5)
