import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    BROWSER_CONFIG = {
        "headless": False,
        "args": ["--no-sandbox", "--disable-setuid-sandbox"]
    }
    
    AGENT_CONFIG = {
        "max_iterations": 20,
        "max_retries": 3,
        "timeout": 30000,
        "wait_between_actions": 0.3
    }
    
    CONTEXT_CONFIG = {
        "max_tokens": 8000,
        "token_buffer": 500,
        "max_page_content": 2000,
        "max_elements": 15
    }
    
    DESTRUCTIVE_ACTIONS = {
        "submit", "delete", "remove", "pay", 
        "checkout", "purchase", "confirm", "send"
    }
    
    @classmethod
    def validate(cls):
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not set in .env file")
        return True
