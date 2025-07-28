from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv
from typing import List

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
    
    def generate_topics(self, user_input: str) -> List[str]:
        """
        Generate debate topics based on user input using the agent.
        
        Args:
            user_input: User's interests or topic preferences
            
        Returns:
            List of suggested debate topics
        """
        try:
            # Create a task for the agent to generate topics
            task_description = f"""
            Based on the user's input: "{user_input}"
            
            Generate 5 engaging debate topics that would be suitable for educational debate.
            
            Consider:
            1. Current events and trending issues
            2. Controversial topics that have clear arguments on both sides
            3. Topics relevant to the user's interests
            4. Educational value and learning potential
            5. Age-appropriate and accessible topics
            
            If the user is unsure or asks for help, suggest topics from current events, 
            technology trends, social issues, education, environment, or health.
            
            Return exactly 5 topics as a list of strings, each starting with "Should" or "Is" or "Are".
            Make sure topics are current, relevant, and debatable.
            """
            
            # Use the agent to generate topics
            response = self.agent.execute_task(task_description)
            
            # Parse the response to extract topics
            # The agent should return a list of topics
            if isinstance(response, list):
                return response[:5]  # Ensure we get exactly 5 topics
            elif isinstance(response, str):
                # If response is a string, try to parse it
                lines = response.strip().split('\n')
                topics = []
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith('Should') or line.startswith('Is') or line.startswith('Are')):
                        topics.append(line)
                return topics[:5]
            else:
                # Fallback to default topics if parsing fails
                return self._get_default_topics()
                
        except Exception as e:
            print(f"Error generating topics: {e}")
            return self._get_default_topics()
    
    def _get_default_topics(self) -> List[str]:
        """Fallback default topics if agent fails."""
        return [
            "Should social media platforms be regulated more strictly?",
            "Is remote work better than office work?",
            "Should college education be free?",
            "Are electric vehicles the future of transportation?",
            "Should artificial intelligence be regulated?"
        ]
    
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