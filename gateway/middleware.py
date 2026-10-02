import time
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from gateway.config import gateway_settings
from collections import defaultdict

logger = logging.getLogger("asas.gateway")
rate_limit_store = defaultdict(list)

async def gateway_rate_limit(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    rate_limit_store[client_ip] = [t for t in rate_limit_store[client_ip] if now - t < 60]
    if len(rate_limit_store[client_ip]) >= gateway_settings.RATE_LIMIT_PER_MINUTE:
        return JSONResponse(status_code=429, content={"error": "rate_limit_exceeded"})
    rate_limit_store[client_ip].append(now)
    return await call_next(request)

async def gateway_logging(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Gateway error: {e}", exc_info=True)
        return JSONResponse(status_code=502, content={"error": "bad_gateway"})
    finally:
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - {process_time:.4f}s")
