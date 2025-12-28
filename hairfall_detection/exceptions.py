from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger("django")

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        # Unhandled server errors
        logger.error("Unhandled server error", exc_info=exc)
        return Response(
            {"message": "This is a server fault. Please try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Flatten DRF errors with field names
    if isinstance(response.data, dict):
        messages = []
        for key, value in response.data.items():
            # Skip adding key name if it is already "message"
            field_prefix = "" if key == "message" else f"{key}: "
            
            if isinstance(value, list):
                messages.append(f"{field_prefix}{value[0]}")
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, list):
                        messages.append(f"{field_prefix}{subkey}: {subvalue[0]}")
                    else:
                        messages.append(f"{field_prefix}{subkey}: {subvalue}")
            else:
                messages.append(f"{field_prefix}{value}")
        
        response.data = {
            "message": " ".join(messages),
            "status_code": response.status_code
        }

    return response