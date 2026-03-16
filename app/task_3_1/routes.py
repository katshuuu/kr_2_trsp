from fastapi import APIRouter, HTTPException, status
from .models import UserCreate

router = APIRouter()

@router.post(
    "/create_user",
    response_model=UserCreate,
    status_code=status.HTTP_200_OK,
    summary="Создание пользователя",
    description="Принимает данные пользователя и возвращает их после валидации",
    responses={
        200: {
            "description": "Успешное создание пользователя",
            "content": {
                "application/json": {
                    "example": {
                        "name": "Alice",
                        "email": "alice@example.com",
                        "age": 30,
                        "is_subscribed": True
                    }
                }
            }
        },
        422: {
            "description": "Ошибка валидации данных"
        }
    }
)
async def create_user(user: UserCreate):
    """
    Задание 3.1: Создание пользователя
    
    **Параметры запроса:**
    - **name**: имя пользователя (обязательно, от 1 до 50 символов)
    - **email**: email пользователя (обязательно, проверка формата)
    - **age**: возраст (опционально, должно быть > 0 и < 150)
    - **is_subscribed**: подписка на рассылку (опционально, по умолчанию false)
    
    **Возвращает:** те же данные после валидации
    """
    return user