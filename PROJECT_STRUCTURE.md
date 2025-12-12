# Структура проекта AI Browser Agent

```
ai-browser-agent/
├── README.md                          # Главная документация
├── QUICK_START.md                     # Быстрый старт (5 минут)
├── ARCHITECTURE.md                    # Архитектура системы
├── TECHNICAL_DETAILS.md               # Технические детали реализации
├── USAGE_EXAMPLES.md                  # Примеры использования
├── DEPLOYMENT.md                      # Развертывание и использование
├── FEATURES.md                        # Полный список функций
├── TROUBLESHOOTING.md                 # Решение проблем
├── CONTRIBUTING.md                    # Внесение вклада
├── CHANGELOG.md                       # История изменений
├── LICENSE                            # MIT лицензия
├── PROJECT_STRUCTURE.md               # Этот файл
│
├── requirements.txt                   # Зависимости Python
├── .env.example                       # Пример конфигурации
├── .gitignore                         # Git ignore файл
│
├── Основные компоненты:
│   ├── main.py                        # Главная точка входа
│   ├── cli.py                         # CLI интерфейс
│   ├── config.py                      # Конфигурация
│   │
│   ├── ai_agent.py                    # Базовый AI агент
│   ├── advanced_agent.py              # Продвинутый AI агент
│   │
│   ├── browser_controller.py          # Управление браузером (Playwright)
│   ├── context_manager.py             # Управление контекстом
│   ├── error_handler.py               # Обработка ошибок
│
├── Примеры и тесты:
│   ├── examples.py                    # Примеры использования
│   ├── test_agent.py                  # Тесты агента
│
├── Скрипты запуска:
│   ├── run.bat                        # Запуск на Windows
│   ├── run.sh                         # Запуск на Linux/Mac
│
└── .github/
    └── workflows/
        └── tests.yml                  # GitHub Actions CI/CD
```

## Описание файлов

### Документация

| Файл | Назначение |
|------|-----------|
| README.md | Главная документация с быстрым стартом |
| QUICK_START.md | 5-минутный гайд для начинающих |
| ARCHITECTURE.md | Подробное описание архитектуры системы |
| TECHNICAL_DETAILS.md | Технические детали реализации |
| USAGE_EXAMPLES.md | Примеры использования с кодом |
| DEPLOYMENT.md | Инструкции по развертыванию |
| FEATURES.md | Полный список функций и возможностей |
| TROUBLESHOOTING.md | Решение распространенных проблем |
| CONTRIBUTING.md | Как внести вклад в проект |
| CHANGELOG.md | История версий и изменений |

### Основной код

| Файл | Назначение |
|------|-----------|
| main.py | Главная точка входа приложения |
| cli.py | Интерактивный CLI интерфейс |
| config.py | Конфигурация приложения |
| ai_agent.py | Базовая реализация AI агента |
| advanced_agent.py | Продвинутая реализация с дополнительными функциями |
| browser_controller.py | Управление браузером через Playwright |
| context_manager.py | Оптимизация контекста для API |
| error_handler.py | Обработка ошибок и retry логика |

### Примеры и тесты

| Файл | Назначение |
|------|-----------|
| examples.py | Примеры использования агента |
| test_agent.py | Тесты для проверки функциональности |

### Конфигурация

| Файл | Назначение |
|------|-----------|
| requirements.txt | Зависимости Python |
| .env.example | Пример переменных окружения |
| .gitignore | Файлы для игнорирования Git |

### Скрипты запуска

| Файл | Назначение |
|------|-----------|
| run.bat | Автоматический запуск на Windows |
| run.sh | Автоматический запуск на Linux/Mac |

## Классы и модули

### BrowserController (browser_controller.py)

```python
class BrowserController:
    async def launch()              # Запуск браузера
    async def close()               # Закрытие браузера
    async def navigate(url)         # Переход на URL
    async def click(selector)       # Клик по элементу
    async def type_text(selector, text)  # Ввод текста
    async def scroll(direction, amount)  # Прокрутка
    async def get_page_content()    # Получить HTML
    async def extract_text_content()    # Получить текст
    async def get_interactive_elements()  # Получить элементы
    async def wait_for_element(selector)  # Ожидание элемента
    async def get_current_url()     # Получить URL
    async def take_screenshot(path)  # Скриншот
```

### AIAgent (ai_agent.py)

```python
class AIAgent:
    async def initialize()          # Инициализация
    async def close()               # Закрытие
    async def execute_task(task)    # Выполнить задачу
    
    # Приватные методы
    def _compress_content(content)  # Сжатие контента
    async def _get_page_state()     # Получить состояние страницы
    async def _parse_tool_calls(response)  # Парсинг инструментов
    async def _execute_tool(name, input)   # Выполнить инструмент
    async def _check_destructive_action()  # Проверка безопасности
```

### AdvancedAIAgent (advanced_agent.py)

Расширенная версия AIAgent с дополнительными возможностями:
- Лучшая обработка ошибок
- Более гибкая система инструментов
- Улучшенное управление контекстом
- Более подробное логирование

### ContextManager (context_manager.py)

```python
class ContextManager:
    def estimate_tokens(text)       # Оценить токены
    def compress_page_content(content)  # Сжать контент
    def format_elements_for_context(elements)  # Форматировать элементы
    def create_page_summary(url, content, elements)  # Создать резюме
    def estimate_conversation_tokens(messages)  # Оценить токены диалога
    def should_trim_history(messages)  # Нужно ли обрезать историю
```

### ErrorHandler (error_handler.py)

```python
class ErrorHandler:
    async def handle_click_error(selector, browser)  # Обработка ошибки клика
    async def handle_navigation_error(url, browser)  # Обработка ошибки навигации
    async def handle_timeout_error(element, browser)  # Обработка таймаута
    def record_error(error_type, details)  # Записать ошибку
    def get_error_summary()         # Получить резюме ошибок
    def reset()                     # Сбросить счетчики
```

### CLI (cli.py)

```python
class AgentCLI:
    async def initialize()          # Инициализация
    async def close()               # Закрытие
    async def run_interactive()     # Интерактивный режим
    async def run_single_task(task) # Одна задача
```

## Инструменты агента

Агент может использовать следующие инструменты:

### Навигация
- `navigate(url)` - переход на URL

### Взаимодействие с элементами
- `click(selector)` - клик по элементу
- `type(selector, text)` - ввод текста
- `scroll(direction, amount)` - прокрутка страницы
- `wait(seconds)` - ожидание
- `wait_for_element(selector, timeout)` - ожидание элемента

### Извлечение информации
- `extract_text()` - получить текст страницы
- `get_elements()` - получить интерактивные элементы
- `get_url()` - получить текущий URL

### Другое
- `screenshot(path)` - сделать скриншот

## Поток данных

```
User Input
    ↓
CLI / main.py
    ↓
AdvancedAIAgent
    ↓
├─ ContextManager (сжатие контента)
├─ BrowserController (управление браузером)
├─ ErrorHandler (обработка ошибок)
└─ Anthropic API (Claude)
    ↓
Tool Calls (XML)
    ↓
BrowserController (выполнение)
    ↓
Results
    ↓
User Output
```

## Зависимости

```
playwright==1.40.0          # Управление браузером
anthropic==0.25.0          # Claude API
python-dotenv==1.0.0       # Переменные окружения
pydantic==2.5.0            # Валидация данных
```

## Переменные окружения

```
ANTHROPIC_API_KEY=sk-ant-...  # API ключ Anthropic
```

## Конфигурация (config.py)

```python
ANTHROPIC_API_KEY          # API ключ
BROWSER_CONFIG             # Конфигурация браузера
AGENT_CONFIG               # Конфигурация агента
CONTEXT_CONFIG             # Конфигурация контекста
DESTRUCTIVE_ACTIONS        # Список опасных действий
```

## Версионирование

- **v1.0.0** - Начальный релиз
- **v1.1.0** - Планируется (улучшения)
- **v1.2.0** - Планируется (новые функции)

## Лицензия

MIT License - смотрите LICENSE файл
