from datetime import timedelta

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from database.db import get_db

from schemas.auth_schema import (
    UserSignup,
    UserLogin,
    UserResponse
)

from schemas.token_schema import (
    Token
)

from security.jwt_handler import (
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

from security.dependencies import (
    get_current_user
)

from services.user_service import (
    create_user,
    authenticate_user
)

router = APIRouter()


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(
    request: UserSignup,
    db: Session = Depends(get_db)
):

    user = create_user(
        db=db,
        name=request.name,
        email=request.email,
        password=request.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered."
        )

    return user


@router.post(
    "/login",
    response_model=Token
)
def login(
    request: UserLogin,
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db=db,
        email=request.email,
        password=request.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        data={
            "user_id": user.id,
            "email": user.email
        },
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.get(
    "/me",
    response_model=UserResponse
)
def me(
    current_user=Depends(get_current_user)
):

    return current_user