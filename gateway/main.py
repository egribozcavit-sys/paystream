import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gateway.config import gateway_settings
from gateway.middleware import gateway_rate_limit, gateway_logging
from gateway.routes import router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("asas.gateway")

app = FastAPI(title="A.S.A.S Cloud Gateway", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=gateway_settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.middleware("http")(gateway_logging)
app.middleware("http")(gateway_rate_limit)

app.include_router(router)

@app.get("/")
async def root():
    return {"service": "A.S.A.S Cloud Gateway", "version": "1.0.0", "status": "operational"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=gateway_settings.GATEWAY_HOST, port=gateway_settings.GATEWAY_PORT)
