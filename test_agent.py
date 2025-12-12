import asyncio
import os
from dotenv import load_dotenv
from advanced_agent import AdvancedAIAgent


async def test_basic_navigation():
    """Test basic navigation"""
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return
    
    agent = AdvancedAIAgent(api_key)
    await agent.initialize()
    
    try:
        print("\n" + "="*60)
        print("Test 1: Basic Navigation")
        print("="*60)
        
        task = "Navigate to python.org and take a screenshot"
        result = await agent.execute_task(task)
        print(f"Result: {result}")
        
    finally:
        await agent.close()


async def test_element_interaction():
    """Test element interaction"""
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return
    
    agent = AdvancedAIAgent(api_key)
    await agent.initialize()
    
    try:
        print("\n" + "="*60)
        print("Test 2: Element Interaction")
        print("="*60)
        
        task = "Go to example.com and find all links on the page"
        result = await agent.execute_task(task)
        print(f"Result: {result}")
        
    finally:
        await agent.close()


async def test_text_extraction():
    """Test text extraction"""
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return
    
    agent = AdvancedAIAgent(api_key)
    await agent.initialize()
    
    try:
        print("\n" + "="*60)
        print("Test 3: Text Extraction")
        print("="*60)
        
        task = "Navigate to wikipedia.org and extract the main heading"
        result = await agent.execute_task(task)
        print(f"Result: {result}")
        
    finally:
        await agent.close()


async def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("AI Browser Agent - Test Suite")
    print("="*60)
    
    tests = [
        ("Basic Navigation", test_basic_navigation),
        ("Element Interaction", test_element_interaction),
        ("Text Extraction", test_text_extraction),
    ]
    
    for test_name, test_func in tests:
        try:
            await test_func()
        except Exception as e:
            print(f"Test failed: {e}")
        
        await asyncio.sleep(2)
    
    print("\n" + "="*60)
    print("All tests completed")
    print("="*60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        if test_name == "navigation":
            asyncio.run(test_basic_navigation())
        elif test_name == "interaction":
            asyncio.run(test_element_interaction())
        elif test_name == "extraction":
            asyncio.run(test_text_extraction())
        elif test_name == "all":
            asyncio.run(run_all_tests())
        else:
            print("Unknown test. Available: navigation, interaction, extraction, all")
    else:
        print("Usage: python test_agent.py [navigation|interaction|extraction|all]")
