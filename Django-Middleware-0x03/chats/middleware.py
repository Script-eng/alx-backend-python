# chats/middleware.py

import logging
import time
from datetime import datetime, time as dt_time
from django.http import HttpResponseForbidden
from django.core.cache import cache

# --- HELPER FUNCTION ---
# A helper function to reliably get the client's IP address.
def get_client_ip(request):
    """
    Get the client's real IP address from the request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# --- MIDDLEWARE CLASS 1: Request Logging ---
# This middleware logs every request to a file.

# Configure the logger to write to 'requests.log'.
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        
        response = self.get_response(request)
        return response


# --- MIDDLEWARE CLASS 2: Time-based Access Restriction ---
# This middleware restricts access to certain hours of the day.

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access to the admin panel at any time.
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # Define the allowed time window (9 AM to 6 PM / 18:00).
        start_time = dt_time(9, 0)
        end_time = dt_time(18, 0)
        current_time = datetime.now().time()

        # Check if the current time is outside the allowed window.
        if not (start_time <= current_time <= end_time):
            return HttpResponseForbidden("Access is restricted to between 9 AM and 6 PM.")
            
        # If within the allowed hours, process the request.
        response = self.get_response(request)
        return response


# --- MIDDLEWARE CLASS 3: Rate Limiting (Named as per instructions) ---
# This middleware limits the number of POST requests per IP address.

class OffensiveLanguageMiddleware:
    # Class-level configuration for the rate limit.
    REQUEST_LIMIT = 5  # Max requests
    TIME_WINDOW = 60   # In seconds

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # This rate-limiting logic only applies to POST requests.
        if request.method != 'POST':
            return self.get_response(request)

        ip_address = get_client_ip(request)
        if not ip_address:
            # Cannot rate-limit without an IP, so let it pass.
            return self.get_response(request)
        
        # Create a unique cache key for the IP address.
        cache_key = f"rate_limit_{ip_address}"
        
        # Get the history of request timestamps from the cache.
        request_history = cache.get(cache_key, [])
        
        current_timestamp = time.time()
        
        # Filter out old timestamps to create a "sliding window".
        valid_requests = [t for t in request_history if t > current_timestamp - self.TIME_WINDOW]
        
        # Check if the limit has been exceeded.
        if len(valid_requests) >= self.REQUEST_LIMIT:
            return HttpResponseForbidden("Rate limit exceeded. Please try again later.")
            
        # Add the current request's timestamp and save it back to the cache.
        valid_requests.append(current_timestamp)
        cache.set(cache_key, valid_requests, self.TIME_WINDOW + 5)
        
        # If the check passes, allow the request to continue.
        response = self.get_response(request)
        return response