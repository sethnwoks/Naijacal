from django.core.cache import cache

ANONYMOUS_PARSE_LIMIT = 5
ANONYMOUS_PARSE_WINDOW_SECONDS = 60 * 60 * 12


def get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def check_anonymous_parse_limit(request):
    if request.user.is_authenticated:
        return {
            "allowed": True,
            "remaining_trials": None,
        }

    client_ip = get_client_ip(request)
    cache_key = f"anonymous_parse_count:{client_ip}"
    current_count = cache.get(cache_key, 0)

    if current_count >= ANONYMOUS_PARSE_LIMIT:
        return {
            "allowed": False,
            "remaining_trials": 0,
        }

    cache.set(
        cache_key,
        current_count + 1,
        timeout=ANONYMOUS_PARSE_WINDOW_SECONDS,
    )

    return {
        "allowed": True,
        "remaining_trials": max(ANONYMOUS_PARSE_LIMIT - (current_count + 1), 0),
    }
