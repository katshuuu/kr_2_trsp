from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class LoginRequest(BaseModel):
    """
    Модель запроса на вход
    """
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Имя пользователя",
        example="user123"
    )
    password: str = Field(
        ...,
        min_length=6,
        description="Пароль",
        example="password123"
    )

class UserResponse(BaseModel):
    """
    Модель ответа с информацией о пользователе
    """
    user_id: str = Field(..., description="Уникальный идентификатор пользователя")
    name: str = Field(..., description="Имя пользователя")
    email: str = Field(..., description="Email пользователя")

class SessionData(BaseModel):
    """
    Модель данных сессии (для задания 5.3)
    """
    user_id: str = Field(..., description="ID пользователя")
    last_activity: float = Field(..., description="Время последней активности (timestamp)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "last_activity": 1715000400.0
            }
        }