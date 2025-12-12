import asyncio
from typing import Optional, Dict, List, Any
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BrowserController:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None

    async def launch(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        logger.info("Browser launched")

    async def close(self):
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("Browser closed")

    async def navigate(self, url: str):
        await self.page.goto(url, wait_until="domcontentloaded")
        logger.info(f"Navigated to {url}")

    async def click(self, selector: str):
        try:
            await self.page.click(selector)
            logger.info(f"Clicked: {selector}")
            await asyncio.sleep(0.5)
        except Exception as e:
            logger.error(f"Click failed: {e}")
            raise

    async def type_text(self, selector: str, text: str):
        try:
            await self.page.fill(selector, text)
            logger.info(f"Typed in {selector}: {text}")
            await asyncio.sleep(0.3)
        except Exception as e:
            logger.error(f"Type failed: {e}")
            raise

    async def scroll(self, direction: str = "down", amount: int = 3):
        script = f"""
        window.scrollBy(0, {amount * 300 if direction == 'down' else -amount * 300});
        """
        await self.page.evaluate(script)
        logger.info(f"Scrolled {direction}")
        await asyncio.sleep(0.5)

    async def get_page_content(self) -> str:
        content = await self.page.content()
        return content

    async def extract_text_content(self) -> str:
        text = await self.page.evaluate("""
        () => {
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
                    text += trimmed + '\\n';
                }
            }
            return text;
        }
        """)
        return text

    async def get_interactive_elements(self) -> List[Dict[str, Any]]:
        elements = await self.page.evaluate("""
        () => {
            const selectors = [];
            const elements = document.querySelectorAll('button, a, input, select, textarea, [role="button"]');
            
            elements.forEach((el, idx) => {
                const rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    let selector = '';
                    if (el.id) {
                        selector = `#${el.id}`;
                    } else if (el.className) {
                        selector = `.${el.className.split(' ')[0]}`;
                    } else {
                        selector = el.tagName.toLowerCase();
                    }
                    
                    const text = el.textContent.trim().substring(0, 50);
                    const type = el.getAttribute('type') || el.tagName.toLowerCase();
                    const placeholder = el.getAttribute('placeholder') || '';
                    
                    selectors.push({
                        selector: selector,
                        text: text,
                        type: type,
                        placeholder: placeholder,
                        visible: rect.top < window.innerHeight && rect.bottom > 0
                    });
                }
            });
            
            return selectors.slice(0, 50);
        }
        """)
        return elements

    async def wait_for_element(self, selector: str, timeout: int = 5000):
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            logger.info(f"Element appeared: {selector}")
        except Exception as e:
            logger.error(f"Element wait failed: {e}")
            raise

    async def get_current_url(self) -> str:
        return self.page.url

    async def take_screenshot(self, path: str):
        await self.page.screenshot(path=path)
        logger.info(f"Screenshot saved: {path}")

    async def handle_dialog(self, dialog_type: str, response: str = "accept"):
        def handle(dialog):
            if response == "accept":
                asyncio.create_task(dialog.accept())
            else:
                asyncio.create_task(dialog.dismiss())

        self.page.on("dialog", handle)
