from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from action import ActionRepository

app = FastAPI(
    title="Modsen App"
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@ app.on_event("startup")
async def on_startup():
    await ActionRepository.startup()


@app.get(
    "/search/{query}"
)
async def _search_posts(query: str):
    return await ActionRepository.search_posts(query=query)


@app.delete(
    "/post/{post_id}"
)
async def delete_post(post_id: str):
    return await ActionRepository.delete_by_id(post_id=post_id)
