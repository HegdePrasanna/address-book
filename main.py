from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.openapi.utils import get_openapi
import json

import models
from database import engine
from routers import address_book
app = FastAPI()


app.include_router(address_book.addr_router, prefix="/api")
app.include_router(address_book.near_by_locations, prefix="/api")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Address Book",
        version="0.0.1",
        summary="Address Book API",
        # description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    openapi_schema["info"]["x-api-response-time"] = {
        "description": "Response time in seconds",
        "type": "number",
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Create db table
models.Base.metadata.create_all(engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8100)
