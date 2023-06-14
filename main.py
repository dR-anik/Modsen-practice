from fastapi import FastAPI

app = FastAPI(
    title="Modsen App"
)
@app.get('/')
def print():
    print('Hello')