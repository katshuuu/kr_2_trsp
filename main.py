# -*- coding: utf-8 -*-
import json
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from app.task_3_1.routes import router as task_3_1_router
from app.task_3_2.routes import router as task_3_2_router
from app.task_5_1_2_3.routes import router as task_5_router
from app.task_5_4_5.routes import router as headers_router

app = FastAPI(
    title="Контрольная работа по FastAPI",
    description="API с заданиями 3.1, 3.2, 5.1-5.5",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Заглушки для иконок
@app.get("/favicon.ico")
@app.get("/apple-touch-icon.png")
@app.get("/apple-touch-icon-precomposed.png")
async def ignore_icons():
    return Response(status_code=204)

# Подключение маршрутов
app.include_router(task_3_1_router, tags=["Задание 3.1 - Пользователи"])
app.include_router(task_3_2_router, tags=["Задание 3.2 - Продукты"])
app.include_router(task_5_router, prefix="/auth", tags=["Задания 5.1-5.3 - Аутентификация"])
app.include_router(headers_router, tags=["Задания 5.4-5.5 - Заголовки"])

@app.get("/")
async def root():
    """
    Root endpoint with information about available endpoints
    """
    return {
        "message": "Control Work on FastAPI",
        "student": "Shustalova Ekaterina Mikhailovna",
        "group": "EFBO-01-24",
        "documentation": "/docs",
        "endpoints": {
            "task_3.1": {
                "create_user": "POST /create_user - Create user"
            },
            "task_3.2": {
                "get_product": "GET /product/{id} - Get product by ID",
                "search_products": "GET /products/search - Search products"
            },
            "task_5.1-5.3": {
                "login": "POST /auth/login - Login",
                "login_v2": "POST /auth/login_v2 - Improved login",
                "user": "GET /auth/user - User profile",
                "profile": "GET /auth/profile - Profile with session extension"
            },
            "task_5.4-5.5": {
                "headers_simple": "GET /headers_simple - Simple headers",
                "headers": "GET /headers - Headers via Pydantic",
                "info": "GET /info - Info with headers"
            }
        }
    }
    """
    Корневой маршрут с информацией о доступных эндпоинтах
    """
    response_data = {
        "message": "Контрольная работа по FastAPI",
        "student": "Шусталова Екатерина Михайловна",
        "group": "ЭФБО-01-24",
        "documentation": "/docs",
        "endpoints": {
            "task_3.1": {
                "create_user": "POST /create_user - Создание пользователя"
            },
            "task_3.2": {
                "get_product": "GET /product/{id} - Получение продукта по ID",
                "search_products": "GET /products/search - Поиск продуктов"
            },
            "task_5.1-5.3": {
                "login": "POST /auth/login - Вход в систему",
                "login_v2": "POST /auth/login_v2 - Улучшенный вход",
                "user": "GET /auth/user - Профиль пользователя",
                "profile": "GET /auth/profile - Профиль с продлением сессии"
            },
            "task_5.4-5.5": {
                "headers_simple": "GET /headers_simple - Простые заголовки",
                "headers": "GET /headers - Заголовки через Pydantic",
                "info": "GET /info - Информация с заголовками"
            }
        }
    }
    
    # Явно устанавливаем кодировку
    json_str = json.dumps(response_data, ensure_ascii=False)
    return JSONResponse(content=json.loads(json_str))