from pymongo import MongoClient

MONGO_URL = "mongodb+srv://diaryuser:Diary123@cluster0.aribf9f.mongodb.net/diary_app?retryWrites=true&w=majority"

client = MongoClient(MONGO_URL)

db = client["diary_app"]

users_collection = db["users"]
notes_collection = db["diary_notes"]
otp_collection = db["otp_codes"]