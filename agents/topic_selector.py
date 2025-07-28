from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class TopicSelectorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=float(os.getenv("TEMPERATURE", "0.7"))
        )
        
        self.agent = Agent(
            role="Topic Discovery Specialist",
            goal="Help users discover and select engaging debate topics through interactive questioning",
            backstory="""You are an expert at helping people discover debate topics that match their interests, 
            background, and learning goals. You ask insightful questions to understand their interests, 
            experience level, and what they hope to learn from debating.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def discover_topic(self, user_input: str = "") -> Dict[str, Any]:
        """
        Interactively discover a debate topic through questioning.
        
        Args:
            user_input: Initial user input (optional)
            
        Returns:
            Dict containing topic, stance, and user preferences
        """
        task_description = f"""
        Help the user discover a debate topic. If they provided initial input: "{user_input}"
        
        Follow this process:
        1. If they mentioned a specific topic, ask clarifying questions about their stance
        2. If they're unsure, ask about their interests, background, or current studies
        3. If they mention having a resume/portfolio, offer to analyze it for topic suggestions
        4. Once a topic is identified, ask if they want to debate FOR or AGAINST it
        5. Confirm their choice and explain why this topic will be good for learning
        
        Be conversational and engaging. Ask one question at a time and wait for responses.
        """
        
        # This would be implemented as an interactive process
        # For now, return a structured response
        return {
            "topic": "Sample Topic",
            "stance": "for",
            "user_preferences": {},
            "discovery_questions": []
        }
    
    def analyze_resume_portfolio(self, content: str) -> list:
        """
        Analyze resume or portfolio content to suggest debate topics.
        
        Args:
            content: Resume or portfolio text
            
        Returns:
            List of suggested debate topics
        """
        analysis_prompt = f"""
        Analyze this resume/portfolio content and suggest 3-5 debate topics that would be relevant:
        
        {content}
        
        Consider:
        - Their field of study/work
        - Current trends in their industry
        - Controversial topics in their domain
        - Topics that would help them develop critical thinking
        
        Return only the topic names, one per line.
        """
        
        # This would use the LLM to analyze and suggest topics
        return ["Topic 1", "Topic 2", "Topic 3"]
    
    def confirm_stance(self, topic: str) -> str:
        """
        Confirm whether the user wants to debate for or against the topic.
        
        Args:
            topic: The selected debate topic
            
        Returns:
            "for" or "against"
        """
        stance_prompt = f"""
        The user has selected the topic: "{topic}"
        
        Ask them whether they want to debate FOR or AGAINST this topic.
        Explain that debating against their natural inclination can be more educational.
        
        Wait for their response and return their choice.
        """
        
        # This would be interactive
        return "for"  # Default for demo
    
    def allow_exit(self) -> bool:
        """
        Check if the user wants to exit the debate.
        
        Returns:
            True if user wants to exit, False otherwise
        """
        exit_prompt = """
        Ask the user if they want to continue with the debate or exit.
        If they choose to exit, thank them and end the session.
        """
        
        # This would be interactive
        return False  # Default for demo 