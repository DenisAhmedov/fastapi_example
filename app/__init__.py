from fastapi import FastAPI

from .routers import posts_router, users_router, token_router

app = FastAPI(title='example app on FastAPI')

app.include_router(posts_router)
app.include_router(users_router)
app.include_router(token_router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}