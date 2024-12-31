from starlette.requests import Request

async def access_control(request: Request, call_next):

    ip = request.headers['x-forwarded-for'] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip

    headers = request.headers
    url = request.url.path

