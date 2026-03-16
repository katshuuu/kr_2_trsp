from fastapi import APIRouter, HTTPException, Query, Path, status  # Добавлен Path
from typing import Optional, List
from .data import sample_products

router = APIRouter()

@router.get(
    "/products/search",
    response_model=List[dict],
    summary="Поиск продуктов",
    description="Поиск продуктов по ключевому слову и категории"
)
async def search_products(
    keyword: str = Query(
        ..., 
        description="Ключевое слово для поиска",
        example="phone"
    ),
    category: Optional[str] = Query(
        None,
        description="Категория для фильтрации",
        example="Electronics"
    ),
    limit: int = Query(
        10,
        description="Максимальное количество результатов",
        ge=1,
        le=100,
        example=5
    )
):
    """
    Задание 3.2: Поиск продуктов
    
    **Параметры запроса:**
    - **keyword**: ключевое слово для поиска (обязательно)
    - **category**: категория для фильтрации (опционально)
    - **limit**: максимальное количество результатов (по умолчанию 10)
    
    **Возвращает:** массив продуктов, соответствующих критериям поиска
    """
    results = []
    
    for product in sample_products:
        # Проверяем наличие ключевого слова в названии (регистронезависимо)
        if keyword.lower() in product["name"].lower():
            # Если указана категория, проверяем соответствие
            if category:
                if product["category"].lower() == category.lower():
                    results.append(product)
            else:
                results.append(product)
    
    # Ограничиваем количество результатов
    return results[:limit]

@router.get(
    "/product/{product_id}",
    response_model=dict,
    summary="Получение продукта по ID",
    description="Возвращает информацию о продукте по его идентификатору"
)
async def get_product(
    product_id: int = Path(  # Исправлено: Query -> Path
        ..., 
        description="Идентификатор продукта",
        example=123,
        ge=1  # Добавлена валидация: product_id должен быть >= 1
    )
):
    """
    Задание 3.2: Получение продукта по ID
    
    **Параметры пути:**
    - **product_id**: идентификатор продукта (целое число, >= 1)
    
    **Возвращает:** информацию о продукте
    
    **Возможные ошибки:**
    - **404**: продукт с указанным ID не найден
    """
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with id {product_id} not found"
    )