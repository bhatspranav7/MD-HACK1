from fastapi import APIRouter
from database import notes_collection
from models import DiaryNote

router = APIRouter()


@router.post("/add-note")
def add_note(note: DiaryNote):

    notes_collection.update_one(
        {"user_email": note.user_email, "date": note.date},
        {"$set": {"text": note.text, "tag": note.tag}},
        upsert=True
    )

    return {"message": "Diary note saved"}


@router.put("/update-note")
def update_note(note: DiaryNote):

    notes_collection.update_one(
        {"user_email": note.user_email, "date": note.date},
        {"$set": {"text": note.text, "tag": note.tag}}
    )

    return {"message": "Diary updated"}


@router.get("/search/date")
def search_date(user_email: str, date: str):

    note = notes_collection.find_one(
        {"user_email": user_email, "date": date},
        {"_id": 0}
    )

    return note


@router.get("/search/month")
def search_month(user_email: str, month: str):

    notes = list(notes_collection.find(
        {"user_email": user_email, "date": {"$regex": month}},
        {"_id": 0}
    ))

    return notes


@router.get("/search/tag")
def search_tag(user_email: str, tag: str):

    notes = list(notes_collection.find(
        {"user_email": user_email, "tag": tag},
        {"_id": 0}
    ))

    return notes