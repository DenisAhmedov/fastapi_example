from fastapi import FastAPI

from .routers import posts, users

app = FastAPI(title='example app on FastAPI')

app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}