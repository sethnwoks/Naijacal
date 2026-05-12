from django.core.cache import cache

ANONYMOUS_PARSE_LIMIT = 5
USER_PARSE_LIMIT = 50
WINDOW_SECONDS = 60 * 60 * 12

def get_client_fingerprint(request):
    """
    Creates a unique-ish key based on IP and Browser info.
    Makes basic IP-spoofing slightly harder to execute.
    """
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "unknown")
    
    user_agent = request.META.get("HTTP_USER_AGENT", "unknown")
    return f"{ip}:{user_agent}"

def check_anonymous_parse_limit(request):
    """
    Checks if the current request is within the allowed quota.
    Handles both anonymous (IP+UA) and authenticated (User ID) limits.
    """
    if request.user.is_authenticated:
        cache_key = f"user_parse_count:{request.user.id}"
        limit = USER_PARSE_LIMIT
    else:
        fingerprint = get_client_fingerprint(request)
        cache_key = f"anonymous_parse_count:{fingerprint}"
        limit = ANONYMOUS_PARSE_LIMIT

    current_count = cache.get(cache_key, 0)

    if current_count >= limit:
        return {
            "allowed": False,
            "remaining_trials": 0,
        }

    cache.set(
        cache_key,
        current_count + 1,
        timeout=WINDOW_SECONDS,
    )

    return {
        "allowed": True,
        "remaining_trials": max(limit - (current_count + 1), 0),
    }
