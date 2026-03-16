"""
Конфигурация для заданий 5.1-5.3
"""

import os

# Секретный ключ для подписи токенов
# В продакшене должен храниться в переменных окружения
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production-123!@#")

# Время жизни сессии в секундах (5 минут)
SESSION_MAX_AGE = 300

# Время для продления сессии в секундах (3 минуты)
SESSION_REFRESH_THRESHOLD = 180