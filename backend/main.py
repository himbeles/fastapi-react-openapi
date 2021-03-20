from typing import Optional

from fastapi import FastAPI
from fastapi.routing import APIRoute
import uvicorn

import json

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}



# generate OpenAPI JSON file

def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.
    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


use_route_names_as_operation_ids(app)
with open("./openapi.json", "w") as fp:
    json.dump(app.openapi(), fp=fp)


def main():
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)