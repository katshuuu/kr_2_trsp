from pydantic import BaseModel, Field, validator
import re

class CommonHeaders(BaseModel):
    """
    Модель для общих заголовков HTTP (Задание 5.5)
    
    Извлекает и валидирует заголовки:
    - User-Agent: информация о клиенте
    - Accept-Language: предпочитаемый язык
    """
    user_agent: str = Field(
        ..., 
        alias="User-Agent",
        description="Заголовок User-Agent",
        example="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    accept_language: str = Field(
        ..., 
        alias="Accept-Language",
        description="Заголовок Accept-Language",
        example="en-US,en;q=0.9,es;q=0.8"
    )
    
    @validator('accept_language')
    def validate_accept_language(cls, v):
        """
        Валидация формата Accept-Language
        
        Пример правильного формата: en-US,en;q=0.9,es;q=0.8
        """
        if not v:
            raise ValueError('Accept-Language header cannot be empty')
        
        # Простая проверка формата
        # Допустимые символы: буквы, цифры, дефис, точка с запятой, запятая, знак равенства
        if not re.match(r'^[a-zA-Z0-9\-;,=\.]+$', v):
            raise ValueError('Invalid Accept-Language format')
        
        # Проверка наличия хотя бы одной языковой метки
        parts = v.split(',')
        if not parts:
            raise ValueError('Accept-Language must contain at least one language tag')
        
        # Проверка первой части (должна быть в формате язык-регион или язык)
        first_part = parts[0].strip()
        if not re.match(r'^[a-zA-Z]{2}(-[a-zA-Z]{2})?$', first_part.split(';')[0]):
            raise ValueError('Invalid language tag format')
        
        return v
    
    class Config:
        allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept-Language": "en-US,en;q=0.9,es;q=0.8"
            }
        }