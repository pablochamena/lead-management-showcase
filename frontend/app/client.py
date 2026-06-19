import os
import httpx
from typing import Optional, Any
from nicegui import ui

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")

# Centralized HTTP Async Client with proper timeouts
client = httpx.AsyncClient(base_url=BACKEND_URL, timeout=5.0)

async def api_request(method: str, url: str, **kwargs) -> Optional[Any]:
    """
    Centralized HTTP request helper.
    Intercepts connection errors, timeouts, and API responses, showing NiceGUI notifications.
    """
    try:
        response = await client.request(method, url, **kwargs)
        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 204:
            return True
        else:
            # Handle client/server response errors (400, 404, 409, 422, etc.)
            detail = "Unknown error"
            try:
                detail = response.json().get("detail", str(response.text))
            except Exception:
                detail = response.text
            
            ui.notify(
                f"Error ({response.status_code}): {detail}",
                type="warning",
                position="top-right"
            )
            return None
    except (httpx.ConnectError, httpx.ConnectTimeout):
        ui.notify(
            "Backend connection error: The server is currently unreachable. Please verify it is running.",
            type="negative",
            position="top-right",
            close_button=True,
            timeout=10
        )
        return None
    except httpx.HTTPError as e:
        ui.notify(
            f"Network error: {str(e)}",
            type="negative",
            position="top-right"
        )
        return None
