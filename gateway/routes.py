from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
from gateway.config import gateway_settings

router = APIRouter()

async def proxy_request(request: Request, path: str):
    async with httpx.AsyncClient(timeout=gateway_settings.TIMEOUT_SECONDS) as client:
        try:
            body = await request.body()
            headers = dict(request.headers)
            headers.pop("host", None)
            
            response = await client.request(
                method=request.method,
                url=f"{gateway_settings.BACKEND_URL}{path}",
                headers=headers,
                content=body
            )
            
            return JSONResponse(
                status_code=response.status_code,
                content=response.json(),
                headers=dict(response.headers)
            )
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="gateway_timeout")
        except httpx.ConnectError:
            raise HTTPException(status_code=502, detail="bad_gateway")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_auth(request: Request, path: str):
    return await proxy_request(request, f"/auth/{path}")

@router.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_users(request: Request, path: str):
    return await proxy_request(request, f"/users/{path}")

@router.api_route("/accounts/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_accounts(request: Request, path: str):
    return await proxy_request(request, f"/accounts/{path}")

@router.api_route("/transactions/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_transactions(request: Request, path: str):
    return await proxy_request(request, f"/transactions/{path}")
