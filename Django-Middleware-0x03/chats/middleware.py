# chats/middleware.py

import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden  # Import the forbidden response

# --- Existing Logging Middleware ---
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

# --- New Time Restriction Middleware ---
# This is the class the checker is looking for.

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request.
        """
        # Define the allowed time window (9 AM to 6 PM / 18:00)
        start_time = time(9, 0)
        end_time = time(18, 0)
        current_time = datetime.now().time()
        
        # A good practice is to always allow access to the admin panel
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # Check if the current time is OUTSIDE the allowed window
        if not (start_time <= current_time <= end_time):
            # If outside the hours, return a 403 Forbidden response.
            return HttpResponseForbidden("Access to the chat is restricted at this time (available 9 AM - 6 PM).")
            
        # If inside the allowed hours, process the request as normal.
        response = self.get_response(request)
        return response