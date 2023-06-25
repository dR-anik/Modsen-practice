from fastapi import FastAPI
from action import ActionRepository
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from database import list_of_posts

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
    "/search/{query}",
    response_model=list_of_posts,
    description='Returns 20 last posts, that includes query text',
    tags=[
        "Posts"
    ]
)
async def _search_posts(query: str) -> list_of_posts:
    return await ActionRepository.search_posts(query=query)


@app.delete(
    "/post/{post_id}",
    response_class=JSONResponse,
    description='Deletes post from database and index by its ID',
    tags=[
        "Posts"
    ]
)
async def delete_post(post_id: str) -> JSONResponse:
    return await ActionRepository.delete_by_id(post_id=post_id)
