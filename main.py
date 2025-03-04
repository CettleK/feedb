from fastapi import FastAPI
from routes import news, auth, user
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, SessionLocal
from contextlib import asynccontextmanager

#venv\Scripts\Activate.bat 
#venv\Scripts\Deactivate.bat
#pip install -r requirements.txt
#python -m uvicorn main:app

# Asynchronous lifespan function replacing @app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        db.execute("SELECT 1")  # Simple query to keep the connection alive
        print("Database connection initialized.")
    except Exception as e:
        print(f"Database connection failed on startup: {e}")
    finally:
        db.close()
    yield  # Allows FastAPI to continue running

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(news.router)
app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
def home():
    return{"message": "FastAPI Backend is Running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)