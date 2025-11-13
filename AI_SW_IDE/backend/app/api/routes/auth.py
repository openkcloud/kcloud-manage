import datetime

from fastapi import APIRouter, HTTPException, status, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt

from app.schemas.login import LoginResponse, UserCreate, LoginRequest, RefreshTokenRequest, UserBase
from app.models.user import User
from app.db.dependencies import get_db 
from app.utils.auth import verify_password, create_access_token, hash_password, decode_refresh_token

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    token_data = {"sub": user.email, "role": user.role}
    access_token = create_access_token(
        data=token_data,
        expires_delta=datetime.timedelta(hours=10)
    )
    
    refresh_token = create_access_token(
        data=token_data,
        expires_delta=datetime.timedelta(days=7)
    )
    
    user_info = {
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "department": user.department,
    }
    
    return LoginResponse(
        success=True,
        user=UserBase(**user_info),
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/refresh", response_model=LoginResponse)
def refresh_token(request: RefreshTokenRequest):
    """
    클라이언트가 보낸 refresh token을 검증하고,
    새로운 access token을 발급합니다.
    """
    try:
        payload = decode_refresh_token(request.refresh_token)
        email = payload.get("sub")
        role = payload.get("role")
        if email is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # 새로운 access token 발급 (60분 만료)
    new_access_token = create_access_token(
        data={"sub": email, "role": role},
        expires_delta=datetime.timedelta(minutes=60)
    )
    
    # 여기서는 동일하게 user 정보는 재사용한다고 가정 (실제 DB 조회 필요할 수도 있음)
    user_info = {
        "email": email,
        "name": "User Name",       # 실제 사용자 정보로 대체
        "role": role,
        "department": "Department" # 실제 사용자 정보로 대체
    }
    
    return LoginResponse(**user_info, success=True, token=new_access_token)

    
@router.post("/create_user")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # 이미 같은 이메일의 사용자가 있는지 확인
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    # 비밀번호 해싱
    hashed_pw = hash_password(user_data.password)
    
    user = User(
        email=user_data.email,
        hashed_password=hashed_pw,  # 해싱된 비밀번호 저장
        role=user_data.role,          # 필요에 따라 기본값 설정 가능
        name=user_data.name,
        department=user_data.department,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"success": True, "user": user.email}