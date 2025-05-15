from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.database.db import get_session
from app.database.models import User, UserCreate, UserRead, UserUpdate, UserAudit
from app.utils.security import hash_password, encrypt_secret, verify_password
from app.utils.auth import get_current_user
from app.utils.jwt import create_access_token

router = APIRouter()

@router.get(
    "/users", response_model=list[UserRead],
    responses={
        401: {
            "description": "Unauthorized - Token JWT ausente ou inválido",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticated"}
                }
            }
        },
    }
)
def list_users(
        session:Session = Depends(get_session),
        current_user:User = Depends(get_current_user)
    ):
    if current_user.role == "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access restricted to administrators.")
    users = session.exec(select(User)).all()
    return users

@router.get("/users/{user_id}", response_model=UserRead)
def get_user(
        user_id:UUID, session:Session = Depends(get_session),
        current_user:User = Depends(get_current_user)
    ):
    user = session.get(User, user_id)
    if current_user.role == "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores.")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
        user_data:UserCreate,
        session:Session = Depends(get_session),
    ):
    user = User(**user_data.model_dump())
    user.password = hash_password(user.password)
    session.add(user)
    try:
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail already registered.") from exc

@router.patch("/users/{user_id}", response_model=UserRead)
def partial_update_user(
        user_id:UUID, user_data:UserUpdate,
        session:Session = Depends(get_session),
        current_user:User = Depends(get_current_user)
    ):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    data = user_data.model_dump(exclude_unset=True)
    if "password" in data:
        data["password"] = hash_password(data["password"])
    if "bybit_api_secret" in data:
        if data["bybit_api_secret"] is not None:
            data["bybit_api_secret"] = encrypt_secret(data["bybit_api_secret"])
    for key, value in data.items():
        old_value = getattr(user, key)
        if old_value != value:
            audit = UserAudit(
                user_id=user.id,
                field_changed=key,
                old_value=str(old_value) if old_value is not None else None,
                new_value=str(value) if value is not None else None,
                changed_by=current_user.id
            )
            session.add(audit)
        setattr(user, key, value)
    user.updated_at = datetime.now(timezone.utc)
    try:
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError as exc:
        session.rollback()
        error_message = str(exc.orig)
        if "UNIQUE constraint failed: user.email" in error_message:
            detail = "E-mail já cadastrado."
        elif "UNIQUE constraint failed: user.bybit_api_key" in error_message:
            detail = "Essa Bybit API Key já está em uso."
        else:
            detail = f"Erro de integridade: {error_message}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from exc

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_id:UUID,
        session:Session = Depends(get_session),
        current_user = Depends(get_current_user)
        ):
    if current_user.role == "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access restricted to administrators.")
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    session.delete(user)
    session.commit()

@router.post("/users/login")
def login(
        form_data:OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session),
    ):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
