from pydantic import BaseModel


class UserSignup(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class ForgotPassword(BaseModel):
    email: str


class ResetPassword(BaseModel):
    email: str
    otp: str
    new_password: str


class DiaryNote(BaseModel):
    user_email: str
    date: str
    text: str
    tag: str