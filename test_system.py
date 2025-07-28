#!/usr/bin/env python3
"""
Test script for the Debate Crew system
Verifies that all agents can be initialized and basic functionality works
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import our agents
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.topic_selector import TopicSelectorAgent
from agents.debator import DebatorAgent
from agents.critique import CritiqueAgent

load_dotenv()

def test_python_version():
    """Test that the correct Python version is being used."""
    print("Testing Python version...")
    
    version = sys.version_info
    required_version = (3, 11, 9)
    
    if version >= required_version:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print(f"Required: Python 3.11.9 or higher")
        return False

def test_agent_initialization():
    """Test that all agents can be initialized."""
    print("Testing agent initialization...")
    
    try:
        # Test Topic Selector Agent
        print("✓ Initializing Topic Selector Agent...")
        topic_selector = TopicSelectorAgent()
        print("✓ Topic Selector Agent initialized successfully")
        
        # Test Debator Agent
        print("✓ Initializing Debator Agent...")
        debator = DebatorAgent()
        print("✓ Debator Agent initialized successfully")
        
        # Test Critique Agent
        print("✓ Initializing Critique Agent...")
        critique = CritiqueAgent()
        print("✓ Critique Agent initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Error initializing agents: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of each agent."""
    print("\nTesting basic functionality...")
    
    try:
        # Test Topic Selector
        topic_selector = TopicSelectorAgent()
        topic_info = topic_selector.discover_topic("technology")
        print("✓ Topic Selector basic functionality works")
        
        # Test Debator
        debator = DebatorAgent()
        opening = debator.initialize_debate("Test topic", "for")
        print("✓ Debator basic functionality works")
        
        # Test Critique
        critique = CritiqueAgent()
        analysis = critique.analyze_argument("Test argument", "user", "Test context")
        print("✓ Critique basic functionality works")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in basic functionality: {e}")
        return False

def test_environment():
    """Test that the environment is properly configured."""
    print("Testing environment configuration...")
    
    # Check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✓ OpenAI API key is configured")
        return True
    else:
        print("✗ OpenAI API key not found")
        print("Please set your OpenAI API key in the .env file")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Debate Crew System\n")
    
    # Test Python version
    version_ok = test_python_version()
    
    if not version_ok:
        print("\n⚠️  Python version not compatible. Please upgrade to Python 3.11.9 or higher.")
        return
    
    # Test environment
    env_ok = test_environment()
    
    if not env_ok:
        print("\n⚠️  Environment not properly configured. Some tests may fail.")
        print("Please set up your .env file with your OpenAI API key.")
    
    # Test agent initialization
    init_ok = test_agent_initialization()
    
    # Test basic functionality
    func_ok = test_basic_functionality()
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"Python Version: {'✓' if version_ok else '✗'}")
    print(f"Environment Configuration: {'✓' if env_ok else '✗'}")
    print(f"Agent Initialization: {'✓' if init_ok else '✗'}")
    print(f"Basic Functionality: {'✓' if func_ok else '✗'}")
    
    if version_ok and env_ok and init_ok and func_ok:
        print("\n🎉 All tests passed! The system is ready to use.")
        print("Run 'python main.py' to start the debate system.")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")
    
    print("="*50)

if __name__ == "__main__":
    main() 