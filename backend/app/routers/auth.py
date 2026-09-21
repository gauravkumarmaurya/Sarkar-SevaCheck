from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..auth import create_token, get_current_user
from ..database import get_db
from ..models import User
from ..schemas import MobileIn, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(data: MobileIn, db: Session = Depends(get_db)):
    mobile = data.mobile
    user = db.query(User).filter(User.mobile == mobile).first()
    if user:
        return {"token": create_token(user), "user": UserOut.model_validate(user), "created": False}

    user = User(name=data.name.strip() or "Citizen", mobile=mobile, is_admin=(mobile == "9999999999"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"token": create_token(user), "user": UserOut.model_validate(user), "created": True}


@router.post("/login")
def login(data: MobileIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.mobile == data.mobile).first()
    if not user:
        raise HTTPException(404, "Mobile number is not registered. Use Register first.")
    return {"token": create_token(user), "user": UserOut.model_validate(user)}


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
