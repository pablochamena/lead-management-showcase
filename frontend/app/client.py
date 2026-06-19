import os
import httpx

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")

# Centralized HTTP Async Client configuration
client = httpx.AsyncClient(base_url=BACKEND_URL, timeout=10.0)
