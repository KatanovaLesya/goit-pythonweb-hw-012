from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database import SessionLocal
from models import User
from schemas import UserCreate, UserOut
from auth_service import get_password_hash, verify_password, create_access_token

from auth_service import get_current_user

from services.email_service import send_email
from auth_service import create_verification_token

from jose import JWTError, jwt
from fastapi import Query
from fastapi import Request
from auth_service import SECRET_KEY, ALGORITHM
from dependencies.roles import admin_required  

from rate_limiter import limiter
from fastapi import UploadFile, File
from services.cloudinary_service import upload_avatar
import os
from services.redis_service import cache_user




router = APIRouter(tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    verification_token = create_verification_token(new_user.email)

    verification_link = f"http://localhost:8000/auth/verify-email?token={verification_token}"

    send_email(
        to_email=new_user.email,
        subject="🎉 Підтвердіть вашу пошту",
        body=f"Привіт, {new_user.username}!\n\nПерейдіть за посиланням для підтвердження вашої електронної адреси:\n{verification_link}"
    )

    return new_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"🔐 Login attempt for: {form_data.username}")
    
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        print("⛔ Email not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password):
        print("⛔ Incorrect password")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        print("⚠️ Email not verified")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified"
        )

    access_token = create_access_token(data={"sub": user.email})

    # Кешуємо користувача
    cache_user(access_token, {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "role": user.role
    })

    print("✅ Token created and user cached")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-email")
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email already verified"}

    user.is_verified = True
    db.commit()
    return {"message": "Email successfully verified!"}

@router.put("/avatar", dependencies=[Depends(admin_required)])
def upload_avatar_route(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contents = file.file.read()
    temp_file = f"temp_{file.filename}"

    with open(temp_file, "wb") as f:
        f.write(contents)

    avatar_url = upload_avatar(temp_file)
    os.remove(temp_file)

    current_user.avatar_url = avatar_url
    db.commit()

    return {"avatar_url": avatar_url}

@router.get("/me", response_model=UserOut)
@limiter.limit("5/minute")
def read_users_me(request: Request, current_user: UserOut = Depends(get_current_user)):
    return current_user
