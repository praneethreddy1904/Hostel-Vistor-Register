
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import functions
from pydantic import BaseModel,Field
from datetime import date


app = FastAPI()


# -------- CORS --------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)


# -------- Pydantic Models --------

class RegisterData(BaseModel):
    username: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class LoginData(BaseModel):
    username: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class VisitorData(BaseModel):
    visitor_name: str = Field(min_length=1)
    student_name: str = Field(min_length=1)
    room_no: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    visit_date: date


# -------- 1. Register User --------

@app.post("/register")
def register_user(data: RegisterData):
    if not functions.register_user(username=data.username, password=data.password, email=data.email):
        raise HTTPException(status_code=409, detail="Email already exists")
    return {"message": "User registered successfully"}

# -------- 2. Login --------


@app.post("/login")
def login(data: LoginData):
    tokens = functions.verify_login(username=data.username, password=data.password,email=data.email)
    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return tokens

# -------- 3. Refresh Token --------

@app.post("/refresh")
def refresh(refresh_token: str = Header(None)):
    response = functions.refresh_access_token(refresh_token)
    if not response:
        raise HTTPException(status_code=401,detail="Invalid or expired refresh token.")
    return response


# -------- 4. Get All Visitors --------

@app.get("/visitors")
def get_all_visitors(token: str = Header(None)):
    user_id = functions.verify_token(token=token,token_type="access")
    if not user_id:
        raise HTTPException(status_code=401,detail="Invalid or expired access token.")
    return functions.get_all_visitors(user_id)


# -------- 5. Add Visitor --------

@app.post("/visitors")
def add_visitor(data: VisitorData, token: str = Header(None)):
    user_id = functions.verify_token(token=token,token_type="access")
    if not user_id:
        raise HTTPException(status_code=401,detail="Invalid or expired access token.")
    response = functions.add_visitor(
        user_id,
        data.visitor_name,
        data.student_name,
        data.room_no,
        data.purpose,
        data.visit_date
    )
    return response
