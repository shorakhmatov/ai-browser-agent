import logging
from typing import Optional, Dict, Any
import asyncio

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Обработчик ошибок с логикой повтора и восстановления"""
    
    def __init__(self):
        self.retry_count = 0
        self.max_retries = 3
        self.last_error = None
        self.error_history = []

    async def handle_click_error(self, selector: str, browser) -> bool:
        """Обработать ошибку клика"""
        self.retry_count += 1
        
        if self.retry_count > self.max_retries:
            logger.error(f"Превышено максимальное количество попыток для селектора: {selector}")
            return False
        
        logger.warning(f"Ошибка клика для {selector}, повтор... ({self.retry_count}/{self.max_retries})")
        
        await asyncio.sleep(1)
        
        try:
            elements = await browser.get_interactive_elements()
            for elem in elements:
                if selector in elem.get('selector', '') or selector in elem.get('text', ''):
                    logger.info(f"Найден альтернативный селектор: {elem['selector']}")
                    return True
        except Exception as e:
            logger.error(f"Ошибка поиска альтернативного селектора: {e}")
        
        return False

    async def handle_navigation_error(self, url: str, browser) -> bool:
        """Обработать ошибку навигации"""
        self.retry_count += 1
        
        if self.retry_count > self.max_retries:
            logger.error(f"Превышено максимальное количество попыток для URL: {url}")
            return False
        
        logger.warning(f"Ошибка навигации для {url}, повтор... ({self.retry_count}/{self.max_retries})")
        
        await asyncio.sleep(2)
        return True

    async def handle_timeout_error(self, element: str, browser) -> bool:
        """Обработать ошибку таймаута"""
        logger.warning(f"Таймаут ожидания элемента: {element}")
        
        current_url = await browser.get_current_url()
        logger.info(f"Текущий URL: {current_url}")
        
        await asyncio.sleep(1)
        return True

    def record_error(self, error_type: str, details: str):
        """Записать ошибку в историю"""
        error_record = {
            "type": error_type,
            "details": details
        }
        self.error_history.append(error_record)
        self.last_error = error_record
        logger.error(f"Ошибка записана: {error_type} - {details}")

    def get_error_summary(self) -> str:
        """Получить резюме ошибок"""
        if not self.error_history:
            return "Ошибок не записано"
        
        summary = f"Всего ошибок: {len(self.error_history)}\n"
        for i, error in enumerate(self.error_history[-5:], 1):
            summary += f"{i}. {error['type']}: {error['details']}\n"
        
        return summary

    def reset(self):
        """Сбросить счетчики"""
        self.retry_count = 0
        self.last_error = None
