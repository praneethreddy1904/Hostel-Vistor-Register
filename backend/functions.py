from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, timedelta, timezone
import jwt  # pyright: ignore[reportMissingImports]
from argon2 import PasswordHasher   # pyright: ignore[reportMissingImports]
from argon2.exceptions import VerifyMismatchError   # pyright: ignore[reportMissingImports]

ph = PasswordHasher()
DB_PATH = "visitors.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

ACCESS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

Base = declarative_base()

class users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class Visitors(Base):
    __tablename__ = "visitors"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    visitor_name = Column(String, nullable=False)
    student_name = Column(String, nullable=False)
    room_no = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    visit_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

Base.metadata.create_all(engine)


# --------register-----------
def register_user(username:str, email:str , password:str):
    session = Session(engine)
    user_exists = session.query(users).filter_by(email=email).first()
    if user_exists is not None:
        session.close()
        return False
    user = users(username=username, email=email, hashed_password=ph.hash(password))
    session.add(user)
    session.commit()
    response = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }
    session.close()
    return response


#-----------login-----------

def verify_login(username, email, password):
    session = Session(engine)

    user = session.query(users).filter_by(email=email).first()

    if user is None:
        session.close()
        return False

    try:
        ph.verify(user.hashed_password, password)

    except VerifyMismatchError:
        session.close()
        return False

    user_id = user.id
    user_name = user.username
    user_email = user.email

    session.close()

    access_token = create_token(user_id, user_name, user_email, "access")
    refresh_token = create_token(user_id, user_name, user_email, "refresh")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

# ----------token-------------
def create_token(user_id, username, email, token_type):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
 
    payload = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "token_type": token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time)
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token
  
def verify_token(token, token_type):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        return False
    
    if payload["token_type"] == token_type:
        return payload["user_id"]
    return False

def refresh_access_token(token):

    try:
        payload = jwt.decode(jwt=token,key=SECRET_KEY,algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        return False

    if payload["token_type"] != "refresh":
        return False

    access_token = create_token(
        payload["user_id"],
        payload["username"],
        payload["email"],
        "access"
    )
    return {
        "access_token": access_token
    }


# --------visitors-----------
def get_all_visitors(user_id):
    session = Session(engine)

    visitors = session.query(Visitors).filter(Visitors.user_id == user_id).all()

    response = []

    for visitor in visitors:
        response.append({
            "id": visitor.id,
            "visitor_name": visitor.visitor_name,
            "student_name": visitor.student_name,
            "room_no": visitor.room_no,
            "purpose": visitor.purpose,
            "visit_date": visitor.visit_date,
            "created_at": visitor.created_at
        })

    session.close()
    return response

def add_visitor(user_id, visitor_name, student_name, room_no, purpose, visit_date):
    session = Session(engine)

    visitor = Visitors(
        user_id=user_id,
        visitor_name=visitor_name,
        student_name=student_name,
        room_no=room_no,
        purpose=purpose,
        visit_date=visit_date
    )

    session.add(visitor)
    session.commit()

    response = {
        "id": visitor.id,
        "user_id": visitor.user_id,
        "visitor_name": visitor.visitor_name,
        "student_name": visitor.student_name,
        "room_no": visitor.room_no,
        "purpose": visitor.purpose,
        "visit_date": visitor.visit_date,
        "created_at": visitor.created_at
    }

    session.close()
    return response