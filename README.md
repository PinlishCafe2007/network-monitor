# 🌐 Network Status Monitor

Система мониторинга доступности веб-ресурсов в реальном времени со сбором статистики.

## 🚀 Особенности

- **📊 Мониторинг в реальном времени** - автоматические проверки каждые 30 секунд
- **📈 Детальная статистика** - uptime, время ответа, история проверок
- **🎯 Визуальный дашборд** - цветовая индикация статусов
- **⚡ Легковесность** - минимальные требования к ресурсам

## 🛠 Технологии

- **Backend**: FastAPI, Python, SQLite
- **Frontend**: Svelte, JavaScript
- **База данных**: SQLite для хранения истории
- **Мониторинг**: HTTP-запросы с таймаутом

## 📡 API Документация

### `GET /status`
Возвращает текущий статус всех ресурсов

**Ответ:**
json
[
  {
    "name": "Google",
    "url": "https://google.com", 
    "status": true,
    "response_time": 150.25,
    "error": null
  }
]
### `GET /stats`
Возвращает статистику по всем проверкам

Ответ:

json
[
  {
    "name": "Google",
    "uptime": 99.5,
    "avg_time": 120.3,
    "total_checks": 150
  }
]
# 🏃‍♂️ Быстрый старт
Установка и запуск
bash
## Клонировать репозиторий
git clone https://github.com/PinlishCafe2007/network-monitor.git
cd network-monitor

## Установить зависимости
pip install -r requirements.txt

## Запустить сервер
python main.py
Запуск фронтенда
bash
## В отдельном терминале
cd frontend
npm install
npm run dev
# 📊 Мониторируемые ресурсы
По умолчанию отслеживаются:

🌐 Google - https://google.com

💻 GitHub - https://github.com

🎥 RuTube - https://rutube.ru

🔧 Swagger UI - https://petstore.swagger.io

# 🎯 Использование
Запустите сервер мониторинга

Откройте веб-интерфейс http://localhost:5173

Наблюдайте за статусом ресурсов в реальном времени

Анализируйте статистику на вкладке "Статистика"

### 📄 Лицензия
MIT License

