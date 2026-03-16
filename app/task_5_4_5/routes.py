from fastapi import APIRouter, HTTPException, Request, Response, Depends, status
from datetime import datetime
from .models import CommonHeaders

router = APIRouter()

# ========== Задание 5.4 ==========

@router.get(
    "/headers_simple",
    summary="Получение заголовков (задание 5.4)",
    description="Простое извлечение заголовков User-Agent и Accept-Language"
)
async def get_headers_simple(request: Request):
    """
    Задание 5.4: Простое извлечение заголовков
    
    Извлекает заголовки User-Agent и Accept-Language из запроса.
    
    **Возможные ошибки:**
    - **400**: отсутствуют обязательные заголовки
    """
    user_agent = request.headers.get("user-agent")
    accept_language = request.headers.get("accept-language")
    
    if not user_agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing User-Agent header"
        )
    
    if not accept_language:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Accept-Language header"
        )
    
    # Дополнительная проверка формата Accept-Language
    if not validate_accept_language_format(accept_language):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Accept-Language format"
        )
    
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }

def validate_accept_language_format(value: str) -> bool:
    """
    Вспомогательная функция для валидации формата Accept-Language
    """
    if not value:
        return False
    
    # Простейшая проверка - должен содержать запятые и точки с запятой
    if ',' not in value:
        return False
    
    return True

# ========== Задание 5.5 ==========

@router.get(
    "/headers",
    summary="Получение заголовков через Pydantic (задание 5.5)",
    description="Извлечение заголовков с использованием модели CommonHeaders"
)
async def get_headers_pydantic(headers: CommonHeaders = Depends()):
    """
    Задание 5.5: Получение заголовков через Pydantic модель
    
    Использует модель CommonHeaders для автоматического извлечения
    и валидации заголовков.
    """
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }

@router.get(
    "/info",
    summary="Информация с заголовками (задание 5.5)",
    description="Возвращает информацию и заголовки с серверным временем"
)
async def get_info(response: Response, headers: CommonHeaders = Depends()):
    """
    Задание 5.5: Расширенный маршрут с дополнительной информацией
    
    Возвращает:
    - Сообщение
    - Заголовки запроса
    - Добавляет заголовок X-Server-Time с текущим серверным временем
    """
    # Добавляем серверное время в заголовки ответа
    current_time = datetime.now()
    response.headers["X-Server-Time"] = current_time.isoformat()
    
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        },
        "server_time": current_time.isoformat()
    }