from fastapi import APIRouter, HTTPException, Request, Response, status, Depends
from .models import LoginRequest, UserResponse, SessionData
from .auth import (
    authenticate_user, get_user_by_id, create_session_token,
    create_extended_session_token, verify_session_token,
    verify_extended_session_token
)
from .config import SESSION_MAX_AGE, SESSION_REFRESH_THRESHOLD
import time
from datetime import datetime

router = APIRouter()

# ========== Задание 5.1 ==========

@router.post(
    "/login",
    summary="Вход в систему (задание 5.1)",
    description="Аутентификация пользователя и установка session_token cookie"
)
async def login(login_data: LoginRequest, response: Response):
    """
    Задание 5.1: Вход в систему
    
    Принимает имя пользователя и пароль. При успешной аутентификации
    устанавливает cookie session_token.
    
    **Параметры:**
    - **username**: имя пользователя
    - **password**: пароль
    
    **Возвращает:** сообщение об успешном входе и устанавливает cookie
    """
    user = authenticate_user(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Создаем простой токен (без подписи для задания 5.1)
    # В реальном проекте так делать нельзя!
    session_token = user["user_id"]
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=SESSION_MAX_AGE,
        secure=False,  # В продакшене должно быть True для HTTPS
        samesite="lax"
    )
    
    return {"message": "Login successful (basic auth)"}

@router.get(
    "/user",
    response_model=UserResponse,
    summary="Профиль пользователя (задание 5.1)",
    description="Защищенный маршрут, требующий аутентификации"
)
async def get_user(request: Request):
    """
    Задание 5.1: Защищенный маршрут
    
    Требует наличия действительного session_token в cookie.
    Возвращает информацию о пользователе.
    
    **Возможные ошибки:**
    - **401**: отсутствует или недействителен session_token
    """
    session_token = request.cookies.get("session_token")
    
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized - No session token"
        )
    
    # Для задания 5.1 просто проверяем, что такой user_id существует
    user = get_user_by_id(session_token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized - Invalid session"
        )
    
    return {
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"]
    }

# ========== Задание 5.2 ==========

@router.post(
    "/login_v2",
    summary="Вход в систему с подписью (задание 5.2)",
    description="Аутентификация с использованием подписанного session_token"
)
async def login_v2(login_data: LoginRequest, response: Response):
    """
    Задание 5.2: Вход в систему с подписью
    
    Использует itsdangerous для создания подписанного токена.
    
    **Параметры:**
    - **username**: имя пользователя
    - **password**: пароль
    
    **Возвращает:** сообщение об успешном входе и устанавливает подписанный cookie
    """
    user = authenticate_user(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Создаем подписанный токен
    session_token = create_session_token(user["user_id"])
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=SESSION_MAX_AGE,
        secure=False,
        samesite="lax"
    )
    
    return {"message": "Login successful (signed token)"}

# ========== Задание 5.3 ==========

@router.post(
    "/login_v3",
    summary="Вход в систему с временем (задание 5.3)",
    description="Аутентификация с расширенными данными сессии"
)
async def login_v3(login_data: LoginRequest, response: Response):
    """
    Задание 5.3: Вход в систему с временем последней активности
    
    Создает токен, содержащий user_id и timestamp последней активности.
    """
    user = authenticate_user(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Создаем расширенный токен с текущим временем
    current_time = time.time()
    session_token = create_extended_session_token(user["user_id"], current_time)
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=SESSION_MAX_AGE,
        secure=False,
        samesite="lax"
    )
    
    return {
        "message": "Login successful (extended session)",
        "login_time": datetime.fromtimestamp(current_time).isoformat()
    }

@router.get(
    "/profile",
    summary="Профиль с автоматическим продлением (задание 5.3)",
    description="Защищенный маршрут с автоматическим продлением сессии"
)
async def get_profile(request: Request, response: Response):
    """
    Задание 5.3: Защищенный маршрут с продлением сессии
    
    Проверяет сессию и автоматически продлевает её при необходимости:
    - Если прошло < 3 минут: сессия не продлевается
    - Если прошло 3-5 минут: сессия продлевается
    - Если прошло > 5 минут: сессия завершается
    
    **Возможные ошибки:**
    - **401**: сессия истекла или недействительна
    """
    session_token = request.cookies.get("session_token")
    
    if not session_token:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Session expired"}
    
    # Проверяем токен
    session_data = verify_extended_session_token(session_token)
    
    if not session_data:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid session"}
    
    # Извлекаем данные
    user_id = session_data.get("user_id")
    last_activity = session_data.get("last_activity")
    
    if not user_id or not last_activity:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid session data"}
    
    # Проверяем время
    current_time = time.time()
    time_since_activity = current_time - last_activity
    
    # Если прошло больше 5 минут - сессия истекла
    if time_since_activity > SESSION_MAX_AGE:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Session expired"}
    
    # Находим пользователя
    user = get_user_by_id(user_id)
    
    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "User not found"}
    
    # Продление сессии если прошло от 3 до 5 минут
    if SESSION_REFRESH_THRESHOLD <= time_since_activity < SESSION_MAX_AGE:
        # Обновляем время последней активности
        new_session_token = create_extended_session_token(user_id, current_time)
        
        response.set_cookie(
            key="session_token",
            value=new_session_token,
            httponly=True,
            max_age=SESSION_MAX_AGE,
            secure=False,
            samesite="lax"
        )
        
        return {
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "last_activity": datetime.fromtimestamp(last_activity).isoformat(),
            "session_refreshed": True,
            "new_expiry": datetime.fromtimestamp(current_time + SESSION_MAX_AGE).isoformat()
        }
    
    # Если прошло меньше 3 минут - просто возвращаем данные
    return {
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"],
        "last_activity": datetime.fromtimestamp(last_activity).isoformat(),
        "session_refreshed": False,
        "time_until_expiry": SESSION_MAX_AGE - time_since_activity
    }