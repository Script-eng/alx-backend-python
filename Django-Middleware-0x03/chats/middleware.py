# chats/middleware.py

import logging
from datetime import datetime

# Configure a specific logger for requests.
# This will write to a file named 'requests.log'.
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view
        (and later middleware) are called.
        """
        # Determine the user. Use 'Anonymous' if not logged in.
        user = request.user if request.user.is_authenticated else 'Anonymous'
        
        # Log the required information.
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        
        # This passes the request to the next middleware or the view.
        response = self.get_response(request)

        # Code to be executed for each response after the view is called
        # (We don't need to do anything here for this task)

        return response