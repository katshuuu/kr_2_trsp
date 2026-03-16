from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class UserCreate(BaseModel):
    """
    Модель для создания пользователя (Задание 3.1)
    
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
    email: str = Field(  # Изменено с EmailStr на str
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
    
    @validator('email')
    def validate_email(cls, v):
        """Ручная валидация email"""
        if not v:
            raise ValueError('Email cannot be empty')
        
        # Простая, но эффективная проверка email
        if '@' not in v:
            raise ValueError('Email must contain @')
        
        local_part, domain = v.rsplit('@', 1)
        
        if not local_part:
            raise ValueError('Email local part cannot be empty')
        
        if '.' not in domain:
            raise ValueError('Email domain must contain a dot')
        
        if len(domain) < 4:  # минимально: a.b
            raise ValueError('Email domain too short')
        
        # Дополнительная проверка через регулярное выражение
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        
        return v.lower()  # возвращаем в нижнем регистре для единообразия
    
    @validator('name')
    def validate_name(cls, v):
        """Дополнительная валидация имени"""
        if not v.strip():
            raise ValueError('Name cannot be empty or only spaces')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice",
                "email": "alice@example.com",
                "age": 30,
                "is_subscribed": True
            }
        }