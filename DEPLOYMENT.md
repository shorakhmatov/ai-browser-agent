# Развертывание и использование

## Локальное развертывание

### Требования
- Python 3.8+
- Anthropic API ключ
- 500MB свободного места (для браузера)

### Установка

```bash
# 1. Клонируем репозиторий
git clone https://github.com/yourusername/ai-browser-agent.git
cd ai-browser-agent

# 2. Создаем виртуальное окружение
python -m venv venv

# Windows
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate

# 3. Устанавливаем зависимости
pip install -r requirements.txt

# 4. Устанавливаем браузер
playwright install chromium

# 5. Настраиваем .env
cp .env.example .env
# Добавляем ANTHROPIC_API_KEY в .env
```

### Запуск

```bash
# Интерактивный режим
python cli.py

# Одна задача
python cli.py "ваша задача"

# Примеры
python examples.py

# Тесты
python test_agent.py all
```

## Docker развертывание

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "cli.py"]
```

### Запуск в Docker

```bash
docker build -t ai-browser-agent .
docker run -it --env-file .env ai-browser-agent
```

## Облачное развертывание

### AWS Lambda (не рекомендуется)
Lambda имеет ограничения на размер и время выполнения, не подходит для этого проекта.

### Google Cloud Run (не рекомендуется)
Требует headless браузер, но задача требует видимого браузера.

### Heroku (не рекомендуется)
Не поддерживает GUI приложения.

### VPS (рекомендуется)

1. **Арендуем VPS** (DigitalOcean, Linode, AWS EC2)
   - Ubuntu 20.04+
   - 2GB RAM минимум
   - 1 CPU

2. **Подключаемся по SSH**
   ```bash
   ssh root@your_server_ip
   ```

3. **Устанавливаем зависимости**
   ```bash
   apt-get update
   apt-get install -y python3 python3-pip git
   ```

4. **Клонируем репозиторий**
   ```bash
   git clone https://github.com/yourusername/ai-browser-agent.git
   cd ai-browser-agent
   ```

5. **Устанавливаем приложение**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

6. **Настраиваем .env**
   ```bash
   nano .env
   # Добавляем ANTHROPIC_API_KEY
   ```

7. **Запускаем в screen/tmux**
   ```bash
   screen -S agent
   python cli.py
   # Ctrl+A+D для выхода из screen
   ```

## Использование через API

### REST API обертка

```python
from flask import Flask, request, jsonify
from advanced_agent import AdvancedAIAgent
import asyncio
import os

app = Flask(__name__)

@app.route('/api/task', methods=['POST'])
def execute_task():
    data = request.json
    task = data.get('task')
    
    if not task:
        return jsonify({'error': 'Task required'}), 400
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    agent = AdvancedAIAgent(api_key)
    
    async def run():
        await agent.initialize()
        try:
            result = await agent.execute_task(task)
            return result
        finally:
            await agent.close()
    
    result = asyncio.run(run())
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

### Использование API

```bash
curl -X POST http://localhost:5000/api/task \
  -H "Content-Type: application/json" \
  -d '{"task": "найти цену на amazon.com"}'
```

## Мониторинг и логирование

### Логирование в файл

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
```

### Мониторинг процесса

```bash
# Проверка статуса
ps aux | grep cli.py

# Просмотр логов
tail -f agent.log

# Остановка процесса
pkill -f cli.py
```

## Безопасность

### Защита API ключа
- Никогда не коммитьте .env файл
- Используйте переменные окружения
- Ограничивайте доступ к серверу

### Защита браузера
- Запускайте в изолированной среде
- Используйте firewall
- Ограничивайте доступ к портам

### Логирование
- Логируйте все действия агента
- Сохраняйте скриншоты для аудита
- Мониторьте использование API

## Производительность

### Оптимизация
- Используйте SSD для быстрого доступа
- Выделите достаточно RAM (минимум 2GB)
- Оптимизируйте сетевое соединение

### Масштабирование
- Для нескольких задач используйте очередь (Celery, RQ)
- Запускайте несколько экземпляров агента
- Используйте load balancer

## Решение проблем

### Браузер не запускается
```bash
playwright install --with-deps
```

### Ошибки памяти
- Увеличьте RAM на сервере
- Закрывайте браузер после каждой задачи
- Используйте процесс очистки памяти

### Медленное выполнение
- Проверьте интернет соединение
- Увеличьте timeout значения
- Используйте более мощный сервер
