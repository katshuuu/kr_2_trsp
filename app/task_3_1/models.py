from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    """
    Поля:
    - name: Имя пользователя (обязательно)
    - email: Email пользователя (обязательно, с валидацией формата)
    - age: Возраст (опционально, должно быть положительным)
    - is_subscribed: Подписка на рассылку (опционально)
    """
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=50,
        description="Имя пользователя",
        example="Alice"
    )
    email: EmailStr = Field(
        ...,
        description="Email пользователя",
        example="alice@example.com"
    )
    age: Optional[int] = Field(
        None,
        gt=0,
        le=150,
        description="Возраст пользователя",
        example=30
    )
    is_subscribed: Optional[bool] = Field(
        False,
        description="Подписка на новостную рассылку",
        example=True
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice",
                "email": "alice@example.com",
                "age": 30,
                "is_subscribed": True
            }
        }