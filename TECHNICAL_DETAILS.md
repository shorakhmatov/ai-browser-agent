# Технические детали реализации

## Выбор технологий

### Playwright vs Selenium vs Puppeteer
**Выбран Playwright** потому что:
- Асинхронный API (asyncio)
- Лучше обработка современных веб-приложений
- Встроенная поддержка скриншотов и видео
- Кроссплатформенность
- Лучше производительность

### Claude 3.5 Sonnet vs GPT-4
**Выбран Claude** потому что:
- Лучше работает с tool calling
- Более надежен в следовании инструкциям
- Лучше обработка контекста
- Более предсказуемое поведение

## Архитектура Tool Calling

### Формат инструментов
```python
# Агент отправляет инструменты в XML формате
<tool_use id="tool_1" name="click">
{"selector": "button.submit"}
</tool_use>

# Система парсит и выполняет
tool_calls = parse_tool_calls(response)
for tool_call in tool_calls:
    result = execute_tool(tool_call.name, tool_call.input)
```

### Парсинг инструментов
```python
import re
pattern = r'<tool_use id="([^"]+)" name="([^"]+)">(.*?)</tool_use>'
matches = re.findall(pattern, response_text, re.DOTALL)

for tool_id, tool_name, tool_input in matches:
    input_data = json.loads(tool_input.strip())
    tool_calls.append({
        "id": tool_id,
        "name": tool_name,
        "input": input_data
    })
```

## Управление контекстом

### Оценка токенов
```python
def estimate_tokens(text: str) -> int:
    # Примерная оценка: 1 токен = 4 слова
    return len(text.split()) // 4 + 1
```

### Сжатие контента
```python
def compress_page_content(content: str, max_tokens: int = 2000):
    # 1. Удаляем пустые строки
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    
    # 2. Фильтруем скрипты и стили
    lines = [l for l in lines if not any(
        kw in l.lower() for kw in ['script', 'style', 'meta']
    )]
    
    # 3. Ограничиваем количество строк
    result = '\n'.join(lines)
    
    # 4. Усекаем если нужно
    if estimate_tokens(result) > max_tokens:
        words = result.split()
        words = words[:max_tokens * 4]
        result = ' '.join(words)
    
    return result
```

## Обработка ошибок

### Retry логика
```python
async def execute_with_retry(tool_name, tool_input, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await execute_tool(tool_name, tool_input)
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
```

### Поиск альтернативных селекторов
```python
async def find_alternative_selector(original_selector, browser):
    elements = await browser.get_interactive_elements()
    
    for elem in elements:
        # Ищем элемент с похожим текстом или типом
        if (original_selector in elem['selector'] or 
            original_selector in elem['text']):
            return elem['selector']
    
    return None
```

## Безопасность

### Проверка деструктивных действий
```python
DESTRUCTIVE_ACTIONS = {
    "submit", "delete", "remove", "pay", 
    "checkout", "purchase", "confirm"
}

async def check_destructive_action(tool_name, tool_input):
    if tool_name == "click":
        selector = tool_input.get("selector", "").lower()
        for action in DESTRUCTIVE_ACTIONS:
            if action in selector:
                return True
    return False
```

### Запрос подтверждения
```python
if is_destructive:
    user_input = input(
        f"⚠️ Agent wants to: {tool_name}({tool_input})\n"
        f"Allow? (y/n): "
    )
    if user_input.lower() != 'y':
        # Отправляем результат агенту
        agent_history.append({
            "role": "user",
            "content": "User rejected this action. Try different approach."
        })
```

## Асинхронное выполнение

### Event Loop
```python
async def main():
    agent = AdvancedAIAgent(api_key)
    await agent.initialize()
    
    try:
        result = await agent.execute_task(task)
    finally:
        await agent.close()

asyncio.run(main())
```

### Параллельные операции
```python
# Одновременное получение информации
async def get_page_state():
    url_task = browser.get_current_url()
    content_task = browser.extract_text_content()
    elements_task = browser.get_interactive_elements()
    
    url, content, elements = await asyncio.gather(
        url_task, content_task, elements_task
    )
    
    return {"url": url, "content": content, "elements": elements}
```

## Извлечение информации со страницы

### Получение интерактивных элементов
```javascript
// Выполняется в контексте браузера
const elements = document.querySelectorAll(
    'button, a, input, select, textarea, [role="button"]'
);

const selectors = [];
elements.forEach((el, idx) => {
    const rect = el.getBoundingClientRect();
    
    // Проверяем видимость
    if (rect.width > 0 && rect.height > 0) {
        // Генерируем селектор
        let selector = el.id ? `#${el.id}` : 
                      el.className ? `.${el.className.split(' ')[0]}` :
                      el.tagName.toLowerCase();
        
        selectors.push({
            selector: selector,
            text: el.textContent.trim().substring(0, 50),
            type: el.getAttribute('type') || el.tagName.toLowerCase(),
            visible: rect.top < window.innerHeight && rect.bottom > 0
        });
    }
});

return selectors.slice(0, 50);
```

### Извлечение текста
```javascript
// Получение всего видимого текста
const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    null,
    false
);

let text = '';
let node;
while (node = walker.nextNode()) {
    const trimmed = node.textContent.trim();
    if (trimmed && trimmed.length > 0) {
        text += trimmed + '\n';
    }
}

return text;
```

## Управление состоянием браузера

### Persistent Sessions
```python
# Браузер сохраняет состояние между задачами
context = await browser.new_context()
page = await context.new_page()

# Cookies и localStorage сохраняются
await page.goto(url)
# ... выполняем действия ...

# Состояние сохраняется для следующей задачи
```

### Управление памятью
```python
async def close_browser():
    if self.page:
        await self.page.close()
    if self.context:
        await self.context.close()
    if self.browser:
        await self.browser.close()
    if self.playwright:
        await self.playwright.stop()
```

## Логирование и отладка

### Структурированное логирование
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

logger = logging.getLogger(__name__)
logger.info(f"Task started: {task}")
logger.error(f"Error occurred: {error}")
```

### Отладка инструментов
```python
# Логируем все вызовы инструментов
logger.info(f"Executing tool: {tool_name}")
logger.info(f"Input: {json.dumps(tool_input, indent=2)}")
result = await execute_tool(tool_name, tool_input)
logger.info(f"Result: {result[:200]}")
```

## Производительность

### Оптимизации
1. **Кэширование селекторов** - запоминаем найденные селекторы
2. **Параллельное извлечение** - одновременно получаем несколько данных
3. **Минимальные задержки** - используем минимально необходимые паузы
4. **Сжатие контента** - уменьшаем размер отправляемых данных

### Метрики
```python
import time

start_time = time.time()
result = await agent.execute_task(task)
elapsed = time.time() - start_time

print(f"Task completed in {elapsed:.2f} seconds")
print(f"Iterations: {agent.task_state['iterations']}")
print(f"Actions taken: {len(agent.task_state['actions_taken'])}")
```

## Тестирование

### Unit тесты
```python
import pytest

@pytest.mark.asyncio
async def test_browser_navigation():
    controller = BrowserController()
    await controller.launch()
    
    try:
        await controller.navigate("https://example.com")
        url = await controller.get_current_url()
        assert "example.com" in url
    finally:
        await controller.close()
```

### Integration тесты
```python
@pytest.mark.asyncio
async def test_agent_task_execution():
    agent = AdvancedAIAgent(api_key)
    await agent.initialize()
    
    try:
        result = await agent.execute_task("Navigate to example.com")
        assert "example.com" in result.lower() or "success" in result.lower()
    finally:
        await agent.close()
```

## Масштабирование

### Использование очереди задач
```python
from celery import Celery

app = Celery('agent')

@app.task
async def execute_agent_task(task_description):
    agent = AdvancedAIAgent(api_key)
    await agent.initialize()
    
    try:
        result = await agent.execute_task(task_description)
        return result
    finally:
        await agent.close()
```

### Параллельное выполнение
```python
import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

tasks = [
    "Find price on amazon.com",
    "Find price on ebay.com",
    "Find price on walmart.com"
]

results = executor.map(lambda t: asyncio.run(execute_task(t)), tasks)
```
