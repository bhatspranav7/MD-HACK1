from fastapi import FastAPI
from auth import router as auth_router
from diary import router as diary_router

app = FastAPI(title="Personal Diary API")


@app.get("/")
def home():
    return {"message": "Diary API running"}


app.include_router(auth_router)
app.include_router(diary_router)