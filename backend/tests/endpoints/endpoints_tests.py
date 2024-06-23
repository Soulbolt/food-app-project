from fastapi.testclient import TestClient
from main import app

client = TestClient(
    app,
    base_url="http://127.0.0.1:8000",
    raise_server_exceptions=True,
    app_root_path="/api",
    backend="uvicorn",
    backend_options=None,
    cookies=None,
    extra_environ=None,
    headers=None,
    follow_redirects=True
    )