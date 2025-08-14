from fastapi import FastAPI
from app.routes import books, users, admin

app = FastAPI(title="Student Library Management System",
              description="Modular, thread-safe student library API",
              version="1.0")

app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}
