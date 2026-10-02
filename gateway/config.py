from pydantic import BaseSettings
from typing import List

class GatewaySettings(BaseSettings):
    GATEWAY_HOST: str = "0.0.0.0"
    GATEWAY_PORT: int = 8080
    BACKEND_URL: str = "http://localhost:8000"
    RATE_LIMIT_PER_MINUTE: int = 1000
    TIMEOUT_SECONDS: int = 30
    CORS_ORIGINS: List[str] = ["*"]
    class Config:
        env_file = ".env.gateway"

gateway_settings = GatewaySettings()
