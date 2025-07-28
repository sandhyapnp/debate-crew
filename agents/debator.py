from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

load_dotenv()

class DebatorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=float(os.getenv("TEMPERATURE", "0.7"))
        )
        
        self.agent = Agent(
            role="Expert Debator",
            goal="Engage in comprehensive, educational debates with strong arguments and counter-arguments",
            backstory="""You are a master debator with years of experience in competitive debating and teaching. 
            You excel at building compelling arguments, understanding opposing viewpoints, and helping students 
            develop critical thinking skills through structured debate.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        self.debate_history = []
        self.current_topic = ""
        self.current_stance = ""
    
    def initialize_debate(self, topic: str, stance: str) -> str:
        """
        Initialize the debate with the selected topic and stance.
        
        Args:
            topic: The debate topic
            stance: "for" or "against" the topic
            
        Returns:
            Opening statement for the debate
        """
        self.current_topic = topic
        self.current_stance = stance
        
        opening_prompt = f"""
        You are debating the topic: "{topic}"
        Your stance is: {stance.upper()}
        
        Provide a compelling opening statement that:
        1. Clearly states your position
        2. Introduces 2-3 key arguments you'll develop
        3. Sets a respectful and educational tone
        4. Invites the opponent to respond
        
        Keep it concise but impactful (2-3 paragraphs max).
        """
        
        # This would use the LLM to generate the opening statement
        return f"I'm ready to debate {stance} the topic: '{topic}'. Let's begin with a thoughtful discussion."
    
    def build_argument(self, user_argument: str = "") -> str:
        """
        Build a comprehensive argument in response to the user's input.
        
        Args:
            user_argument: The user's argument or statement
            
        Returns:
            A well-structured counter-argument or supporting argument
        """
        context = f"""
        Debate Topic: {self.current_topic}
        Your Stance: {self.current_stance.upper()}
        
        Previous arguments in this debate:
        {self._format_debate_history()}
        
        User's latest argument: "{user_argument}"
        """
        
        argument_prompt = f"""
        {context}
        
        Build a compelling argument that:
        1. Acknowledges the user's points respectfully
        2. Provides strong evidence and reasoning for your position
        3. Addresses potential counter-arguments
        4. Maintains focus on the core topic
        5. Uses clear, logical structure
        
        Structure your response with:
        - A brief acknowledgment of their points
        - Your main argument with supporting evidence
        - A question or challenge to continue the debate
        
        Keep it educational and constructive.
        """
        
        # This would use the LLM to generate the argument
        return f"I understand your perspective on {self.current_topic}. Let me build on that with additional considerations..."
    
    def respond_to_counter(self, counter_argument: str) -> str:
        """
        Respond to a counter-argument from the user.
        
        Args:
            counter_argument: The user's counter-argument
            
        Returns:
            A response that addresses the counter-argument
        """
        response_prompt = f"""
        The user has provided this counter-argument: "{counter_argument}"
        
        Your stance is: {self.current_stance.upper()}
        Topic: {self.current_topic}
        
        Respond by:
        1. Acknowledging the validity of their points
        2. Providing additional evidence or reasoning
        3. Addressing any logical fallacies or weak points
        4. Maintaining a respectful, educational tone
        5. Moving the debate forward constructively
        
        Keep your response focused and well-structured.
        """
        
        # This would use the LLM to generate the response
        return f"That's an interesting counter-point. Let me address that by considering..."
    
    def provide_evidence(self, claim: str) -> str:
        """
        Provide evidence to support a specific claim.
        
        Args:
            claim: The claim that needs supporting evidence
            
        Returns:
            Evidence and reasoning to support the claim
        """
        evidence_prompt = f"""
        You need to provide evidence for this claim: "{claim}"
        
        In the context of debating {self.current_stance} the topic: {self.current_topic}
        
        Provide:
        1. Relevant facts and statistics
        2. Expert opinions or studies
        3. Real-world examples
        4. Logical reasoning
        
        Make sure the evidence directly supports your stance.
        """
        
        # This would use the LLM to generate evidence
        return f"Here's compelling evidence to support that claim: [Evidence would be generated here]"
    
    def summarize_position(self) -> str:
        """
        Provide a summary of the current debate position.
        
        Returns:
            A summary of the key arguments and current state
        """
        summary_prompt = f"""
        Summarize the current state of the debate:
        Topic: {self.current_topic}
        Your Stance: {self.current_stance.upper()}
        
        Include:
        1. Key arguments made so far
        2. Evidence presented
        3. Current position strength
        4. Areas that need more development
        
        Keep it concise but comprehensive.
        """
        
        # This would use the LLM to generate the summary
        return f"Let me summarize our discussion on {self.current_topic}..."
    
    def _format_debate_history(self) -> str:
        """Format the debate history for context."""
        if not self.debate_history:
            return "No previous arguments yet."
        
        formatted = []
        for i, entry in enumerate(self.debate_history, 1):
            formatted.append(f"{i}. {entry}")
        
        return "\n".join(formatted)
    
    def add_to_history(self, argument: str, speaker: str):
        """Add an argument to the debate history."""
        self.debate_history.append(f"{speaker}: {argument}") 