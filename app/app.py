import aiohttp
from loguru import logger
from fastapi import FastAPI, Request, Response, HTTPException

app = FastAPI(debug=True)

@app.api_route("/{path:path}", methods=["GET", "POST", "DELETE", "PUT", "PATCH"])
async def proxy(request: Request, path: str):
    if not path.startswith("v1"):
        return Response("Welcome to OpenAI Proxy")

    headers = dict(request.headers)
    auth_key = headers.get("authorization")
    if not auth_key:
        raise HTTPException(status_code=401, detail="Authorization key is required")

    target_url = f"https://api.openai.com/{path}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                method=request.method,
                url=target_url,
                headers={
                    "Authorization": headers.get("authorization"),
                    "Content-Type": "application/json"
                },
                data=await request.body() if request.method != "GET" else None,
            ) as response:
                content = await response.read()
                return Response(
                    content=content,
                    status_code=response.status,
                    headers=dict(response.headers)
                )
        except Exception as e:
            logger.error(f"Error during proxy forwarding: {e}")
            return Response(f"Proxy error: {str(e)}", status_code=500)
