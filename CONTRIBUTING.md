# Внесение вклада в AI Browser Agent

## Как начать

1. Форкируйте репозиторий
2. Создайте ветку для вашей функции (`git checkout -b feature/amazing-feature`)
3. Коммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Пушьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## Требования к коду

### Стиль кода
- Используйте PEP 8
- Максимальная длина строки: 100 символов
- Используйте type hints где возможно

### Тестирование
- Добавляйте тесты для новых функций
- Убедитесь, что все тесты проходят
- Покрытие кода должно быть > 80%

### Документация
- Обновляйте README если нужно
- Добавляйте docstrings к функциям
- Документируйте новые инструменты

## Процесс разработки

1. **Создание issue** - опишите проблему или функцию
2. **Обсуждение** - получите обратную связь
3. **Разработка** - реализуйте решение
4. **Тестирование** - убедитесь, что всё работает
5. **Pull Request** - отправьте на review

## Добавление новых инструментов

### Пример: Добавление нового инструмента

```python
# В ai_agent.py добавьте:

async def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
    # ... существующий код ...
    
    elif tool_name == "new_tool":
        param = tool_input.get("param")
        result = await self.browser.new_method(param)
        return f"New tool executed: {result}"
```

### Пример: Добавление метода браузера

```python
# В browser_controller.py добавьте:

async def new_method(self, param: str) -> str:
    """Description of the method"""
    try:
        # Реализация
        result = await self.page.evaluate(f"...")
        logger.info(f"Method executed: {result}")
        return result
    except Exception as e:
        logger.error(f"Method failed: {e}")
        raise
```

## Отчеты об ошибках

При создании issue включите:
- Описание проблемы
- Шаги для воспроизведения
- Ожидаемое поведение
- Фактическое поведение
- Версия Python и OS
- Логи ошибок

## Запросы функций

При создании запроса функции включите:
- Описание функции
- Примеры использования
- Возможные реализации
- Преимущества для пользователей

## Код Review

При review кода мы проверяем:
- Качество кода
- Соответствие стилю
- Наличие тестов
- Документация
- Производительность

## Лицензия

Внося вклад, вы соглашаетесь, что ваш код будет лицензирован под MIT License.
