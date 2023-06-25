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