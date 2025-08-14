from fastapi import FastAPI
from .database import engine, Base
from .routers import users, books

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])
