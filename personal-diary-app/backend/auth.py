from fastapi import APIRouter, HTTPException
from database import users_collection, otp_collection
from models import UserSignup, UserLogin, ForgotPassword, ResetPassword
from passlib.context import CryptContext
from jose import jwt
import re
import random

router = APIRouter()

SECRET_KEY = "diary_secret_key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Password validation
def validate_password(password: str):

    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must contain uppercase letter")

    if not re.search(r"[0-9]", password):
        raise HTTPException(status_code=400, detail="Password must contain number")

    if not re.search(r"[!@#$%^&*]", password):
        raise HTTPException(status_code=400, detail="Password must contain special symbol")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


# SIGNUP
@router.post("/signup")
def signup(user: UserSignup):

    validate_password(user.password)

    existing_user = users_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)

    users_collection.insert_one({
        "email": user.email,
        "password": hashed
    })

    return {"message": "User created successfully"}


# LOGIN
@router.post("/login")
def login(user: UserLogin):

    existing_user = users_collection.find_one({"email": user.email})

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = jwt.encode({"email": user.email}, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "message": "Login successful",
        "token": token
    }


# FORGOT PASSWORD (Generate OTP)
@router.post("/forgot-password")
def forgot_password(data: ForgotPassword):

    user = users_collection.find_one({"email": data.email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = str(random.randint(100000, 999999))

    otp_collection.update_one(
        {"email": data.email},
        {"$set": {"otp": otp}},
        upsert=True
    )

    return {
        "message": "OTP generated",
        "otp": otp
    }


# RESET PASSWORD
@router.post("/reset-password")
def reset_password(data: ResetPassword):

    record = otp_collection.find_one({"email": data.email})

    if not record or record["otp"] != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    validate_password(data.new_password)

    hashed = hash_password(data.new_password)

    users_collection.update_one(
        {"email": data.email},
        {"$set": {"password": hashed}}
    )

    return {"message": "Password reset successful"}