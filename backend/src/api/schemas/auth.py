from pydantic import BaseModel, EmailStr
import uuid


class AuthRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    nome: str
    papel: str = "obra"
    obra_id: uuid.UUID | None = None


class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
