# Архитектура AI Browser Agent

## Обзор системы

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Interface                        │
│                      (cli.py, examples.py)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                      AI Agent Layer                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  AdvancedAIAgent / AIAgent                           │   │
│  │  - Task execution logic                             │   │
│  │  - Tool calling and parsing                         │   │
│  │  - Conversation history management                  │   │
│  │  - Security checks for destructive actions          │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌────▼──────────┐ ┌──▼──────────────┐
│ BrowserControl │ │ContextManager │ │  ErrorHandler   │
│  (browser_     │ │ (context_      │ │  (error_        │
│   controller   │ │  manager.py)   │ │   handler.py)   │
│   .py)         │ │                │ │                 │
│                │ │ - Token mgmt   │ │ - Retry logic   │
│ - Navigate     │ │ - Content      │ │ - Error recovery│
│ - Click        │ │   compression  │ │ - History track │
│ - Type         │ │ - Element      │ │                 │
│ - Scroll       │ │   formatting   │ │                 │
│ - Extract      │ │                │ │                 │
│ - Screenshot   │ │                │ │                 │
└───────┬────────┘ └────────────────┘ └──────────────────┘
        │
┌───────▼────────────────────────────────────────────────────┐
│                  Playwright Browser                         │
│              (Chromium, non-headless mode)                  │
└────────────────────────────────────────────────────────────┘
        │
┌───────▼────────────────────────────────────────────────────┐
│                    Web Browser                              │
│              (Visible to user in real-time)                 │
└────────────────────────────────────────────────────────────┘
```

## Компоненты

### 1. CLI Interface (`cli.py`)
- Интерактивный режим для взаимодействия с агентом
- Поддержка команд (task, screenshot, url, help, exit)
- Обработка пользовательского ввода

### 2. AI Agent (`ai_agent.py` / `advanced_agent.py`)
**Основная логика:**
- Получение задачи от пользователя
- Анализ состояния страницы
- Генерация инструкций через Claude API
- Парсинг tool calls из ответа
- Выполнение инструментов
- Управление историей диалога
- Проверка безопасности для деструктивных действий

**Tool Calling:**
```
Agent → Claude API → Tool calls (XML format)
↓
Parse tool calls
↓
Execute tools (click, type, navigate, etc.)
↓
Get results
↓
Send results back to Claude
```

### 3. Browser Controller (`browser_controller.py`)
**Управление браузером:**
- Запуск/закрытие Chromium
- Навигация по URL
- Клики по элементам
- Ввод текста
- Прокрутка страницы
- Извлечение содержимого страницы
- Получение интерактивных элементов
- Скриншоты

**Селекторы:**
- Автоматическое определение CSS селекторов
- Поддержка ID, классов, тегов
- Фильтрация видимых элементов

### 4. Context Manager (`context_manager.py`)
**Оптимизация контекста:**
- Оценка количества токенов
- Сжатие содержимого страницы
- Форматирование элементов для контекста
- Управление историей сообщений
- Предотвращение превышения лимита токенов

**Стратегия сжатия:**
1. Удаление скриптов и стилей
2. Удаление пустых строк
3. Ограничение количества элементов
4. Усечение длинного текста

### 5. Error Handler (`error_handler.py`)
**Обработка ошибок:**
- Retry logic для неудачных действий
- Поиск альтернативных селекторов
- Обработка таймаутов
- История ошибок
- Адаптивное поведение

## Поток выполнения

```
1. User Input (task)
   ↓
2. Initialize Agent & Browser
   ↓
3. Loop (max 15-20 iterations):
   a. Get page state
      - Current URL
      - Page content (compressed)
      - Interactive elements
   
   b. Create context
      - Compress content to fit token limit
      - Format elements for readability
      - Include action history
   
   c. Call Claude API
      - Send page state + task
      - Receive response with tool calls
   
   d. Parse tool calls
      - Extract tool name and parameters
      - Validate parameters
   
   e. Security check
      - If destructive action → ask user
      - If approved → execute
   
   f. Execute tools
      - Navigate, click, type, scroll, etc.
      - Handle errors with retry logic
   
   g. Get results
      - Send results back to Claude
      - Update conversation history
   
   h. Check completion
      - If task done → return result
      - Else → continue loop

4. Close browser
```

## Tool Calling Format

Claude возвращает инструменты в XML формате:

```xml
<tool_use id="tool_1" name="navigate">
{"url": "https://example.com"}
</tool_use>

<tool_use id="tool_2" name="click">
{"selector": "button.submit"}
</tool_use>

<tool_use id="tool_3" name="type">
{"selector": "input#email", "text": "user@example.com"}
</tool_use>
```

## Безопасность

**Деструктивные действия:**
- submit, delete, remove, pay, checkout, purchase, confirm

**Процесс проверки:**
1. Агент хочет выполнить действие
2. Система проверяет, деструктивно ли оно
3. Если да → запрашивает подтверждение у пользователя
4. Пользователь может одобрить (y) или отклонить (n)
5. Результат отправляется обратно агенту

## Оптимизация контекста

**Проблема:** Claude API имеет лимит контекста (8000 токенов)

**Решение:**
1. Сжатие содержимого страницы
   - Удаление HTML тегов
   - Удаление пустых строк
   - Ограничение длины

2. Фильтрация элементов
   - Показываем только видимые элементы
   - Ограничиваем количество (15-20)
   - Показываем только релевантные

3. Управление историей
   - Отслеживаем использование токенов
   - Удаляем старые сообщения при необходимости

## Обработка ошибок

**Типы ошибок:**
1. Click failed → поиск альтернативного селектора
2. Navigation failed → повтор с задержкой
3. Timeout → ожидание и повтор
4. Invalid selector → предложение альтернативы

**Retry strategy:**
- Max retries: 3
- Delay между попытками: 1-2 секунды
- Логирование всех ошибок

## Производительность

**Оптимизации:**
- Асинхронное выполнение (asyncio)
- Минимальные задержки между действиями
- Параллельное извлечение информации
- Кэширование состояния браузера

**Ограничения:**
- Max iterations: 15-20 на задачу
- Max tokens: 8000 на контекст
- Timeout на элементы: 5 секунд
