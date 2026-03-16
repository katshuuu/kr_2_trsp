"""
Логика аутентификации для заданий 5.1-5.3
"""

import uuid
from typing import Dict, Optional
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from .config import SECRET_KEY, SESSION_MAX_AGE

# Инициализация сериализатора для подписанных токенов
serializer = URLSafeTimedSerializer(SECRET_KEY)

# Хранилище пользователей (в реальном проекте используйте БД)
users_db: Dict[str, Dict[str, str]] = {
    "user123": {
        "password": "password123",
        "user_id": str(uuid.uuid4()),
        "name": "John Doe",
        "email": "john@example.com"
    },
    "alice": {
        "password": "alice2024",
        "user_id": str(uuid.uuid4()),
        "name": "Alice Smith",
        "email": "alice@example.com"
    }
}

def authenticate_user(username: str, password: str) -> Optional[Dict[str, str]]:
    """
    Проверка учетных данных пользователя
    
    Args:
        username: имя пользователя
        password: пароль
    
    Returns:
        Данные пользователя или None если аутентификация не удалась
    """
    if username in users_db and users_db[username]["password"] == password:
        return users_db[username]
    return None

def get_user_by_id(user_id: str) -> Optional[Dict[str, str]]:
    """
    Поиск пользователя по ID
    
    Args:
        user_id: идентификатор пользователя
    
    Returns:
        Данные пользователя или None если не найден
    """
    for user_data in users_db.values():
        if user_data["user_id"] == user_id:
            return user_data
    return None

def create_session_token(user_id: str) -> str:
    """
    Создание подписанного токена сессии (задания 5.2, 5.3)
    
    Args:
        user_id: идентификатор пользователя
    
    Returns:
        Подписанный токен
    """
    return serializer.dumps(user_id)

def create_extended_session_token(user_id: str, timestamp: float) -> str:
    """
    Создание расширенного токена сессии с временем (задание 5.3)
    
    Args:
        user_id: идентификатор пользователя
        timestamp: временная метка
    
    Returns:
        Подписанный токен с данными сессии
    """
    session_data = {
        "user_id": user_id,
        "last_activity": timestamp
    }
    return serializer.dumps(session_data)

def verify_session_token(token: str) -> Optional[str]:
    """
    Проверка токена сессии (задания 5.1, 5.2)
    
    Args:
        token: токен для проверки
    
    Returns:
        user_id или None если токен недействителен
    """
    try:
        return serializer.loads(token, max_age=SESSION_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None

def verify_extended_session_token(token: str) -> Optional[Dict]:
    """
    Проверка расширенного токена сессии (задание 5.3)
    
    Args:
        token: токен для проверки
    
    Returns:
        Данные сессии или None если токен недействителен
    """
    try:
        return serializer.loads(token, max_age=SESSION_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None