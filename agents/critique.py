from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class CritiqueAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=float(os.getenv("TEMPERATURE", "0.7"))
        )
        
        self.agent = Agent(
            role="Debate Critique Specialist",
            goal="Analyze debate quality and provide constructive feedback with scoring",
            backstory="""You are an expert debate judge and educator with extensive experience in evaluating 
            debate quality, argument structure, and educational value. You provide fair, constructive feedback 
            that helps students improve their critical thinking and argumentation skills.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        self.debate_scores = {
            "user": {"argument_quality": 0, "evidence_use": 0, "logical_structure": 0, "total": 0},
            "debator": {"argument_quality": 0, "evidence_use": 0, "logical_structure": 0, "total": 0}
        }
        self.feedback_history = []
        self.current_topic = ""
    
    def analyze_argument(self, argument: str, speaker: str, context: str = "") -> Dict[str, Any]:
        """
        Analyze the quality of a specific argument.
        
        Args:
            argument: The argument to analyze
            speaker: "user" or "debator"
            context: Additional context about the debate
            
        Returns:
            Dict containing analysis scores and feedback
        """
        analysis_prompt = f"""
        Analyze this debate argument:
        
        Speaker: {speaker}
        Argument: "{argument}"
        Context: {context}
        
        Evaluate on these criteria (1-10 scale):
        1. Argument Quality: Clarity, persuasiveness, relevance
        2. Evidence Use: Facts, statistics, examples, expert opinions
        3. Logical Structure: Coherence, reasoning, flow
        
        Provide:
        - Scores for each criterion
        - Specific feedback on strengths and weaknesses
        - Suggestions for improvement
        - Overall assessment
        """
        
        # This would use the LLM to analyze the argument
        scores = {
            "argument_quality": 7,
            "evidence_use": 6,
            "logical_structure": 8,
            "total": 7
        }
        
        feedback = f"Good argument structure with room for improvement in evidence presentation."
        
        return {
            "scores": scores,
            "feedback": feedback,
            "suggestions": ["Add more specific examples", "Strengthen evidence with statistics"]
        }
    
    def update_scores(self, analysis: Dict[str, Any], speaker: str):
        """
        Update the running scores for a speaker.
        
        Args:
            analysis: The analysis results from analyze_argument
            speaker: "user" or "debator"
        """
        if speaker in self.debate_scores:
            scores = analysis["scores"]
            self.debate_scores[speaker]["argument_quality"] = scores["argument_quality"]
            self.debate_scores[speaker]["evidence_use"] = scores["evidence_use"]
            self.debate_scores[speaker]["logical_structure"] = scores["logical_structure"]
            self.debate_scores[speaker]["total"] = scores["total"]
    
    def provide_mid_debate_feedback(self) -> str:
        """
        Provide feedback during the middle of the debate.
        
        Returns:
            Constructive feedback for both participants
        """
        feedback_prompt = f"""
        Based on the current debate scores:
        User: {self.debate_scores['user']}
        Debator: {self.debate_scores['debator']}
        
        Provide constructive mid-debate feedback that:
        1. Acknowledges strengths of both participants
        2. Identifies areas for improvement
        3. Encourages continued engagement
        4. Maintains educational focus
        
        Keep it encouraging and actionable.
        """
        
        # This would use the LLM to generate feedback
        return "Both participants are showing strong engagement. Consider adding more specific evidence to strengthen arguments."
    
    def final_evaluation(self, debate_history: List[str]) -> Dict[str, Any]:
        """
        Provide a final evaluation of the entire debate.
        
        Args:
            debate_history: Complete history of the debate
            
        Returns:
            Comprehensive final evaluation
        """
        evaluation_prompt = f"""
        Provide a final evaluation of this debate:
        
        Topic: {self.current_topic}
        Debate History: {debate_history}
        Final Scores: {self.debate_scores}
        
        Include:
        1. Overall debate quality assessment
        2. Strengths of each participant
        3. Areas for improvement
        4. Educational value achieved
        5. Recommendations for future debates
        6. Final scores and rankings
        
        Be comprehensive but constructive.
        """
        
        # This would use the LLM to generate the final evaluation
        return {
            "overall_quality": "Good",
            "user_strengths": ["Clear communication", "Engaged participation"],
            "debator_strengths": ["Strong argument structure", "Good evidence use"],
            "improvement_areas": ["More specific examples", "Better counter-arguments"],
            "educational_value": "High - good critical thinking development",
            "final_scores": self.debate_scores
        }
    
    def track_debate_quality(self, argument_pair: Tuple[str, str]) -> Dict[str, Any]:
        """
        Track the quality of a debate exchange between user and debator.
        
        Args:
            argument_pair: Tuple of (user_argument, debator_response)
            
        Returns:
            Analysis of the exchange quality
        """
        user_arg, debator_resp = argument_pair
        
        exchange_analysis = f"""
        Analyze this debate exchange:
        
        User: "{user_arg}"
        Debator: "{debator_resp}"
        
        Evaluate:
        1. How well the debator responded to the user's points
        2. Whether the exchange moved the debate forward
        3. Quality of argument development
        4. Educational value of the exchange
        
        Provide scores and feedback.
        """
        
        # This would use the LLM to analyze the exchange
        return {
            "exchange_quality": 8,
            "response_adequacy": 7,
            "argument_development": 8,
            "educational_value": 9,
            "feedback": "Good exchange that developed the argument well."
        }
    
    def identify_logical_fallacies(self, argument: str) -> List[str]:
        """
        Identify potential logical fallacies in an argument.
        
        Args:
            argument: The argument to analyze
            
        Returns:
            List of identified logical fallacies
        """
        fallacy_prompt = f"""
        Analyze this argument for logical fallacies:
        "{argument}"
        
        Look for:
        - Ad hominem attacks
        - Straw man arguments
        - False dilemmas
        - Appeal to authority
        - Hasty generalizations
        - Other common fallacies
        
        Return any identified fallacies with brief explanations.
        """
        
        # This would use the LLM to identify fallacies
        return []  # No fallacies found in this example
    
    def suggest_improvements(self, argument: str, speaker: str) -> List[str]:
        """
        Suggest specific improvements for an argument.
        
        Args:
            argument: The argument to improve
            speaker: "user" or "debator"
            
        Returns:
            List of specific improvement suggestions
        """
        improvement_prompt = f"""
        Suggest improvements for this argument by {speaker}:
        "{argument}"
        
        Consider:
        1. Evidence and examples
        2. Logical structure
        3. Clarity and persuasiveness
        4. Counter-argument preparation
        
        Provide specific, actionable suggestions.
        """
        
        # This would use the LLM to generate suggestions
        return [
            "Add specific statistics to support your claim",
            "Address potential counter-arguments more directly",
            "Provide concrete examples to illustrate your point"
        ]
    
    def get_current_scores(self) -> Dict[str, Any]:
        """Get the current debate scores."""
        return self.debate_scores.copy()
    
    def reset_scores(self):
        """Reset all scores for a new debate."""
        self.debate_scores = {
            "user": {"argument_quality": 0, "evidence_use": 0, "logical_structure": 0, "total": 0},
            "debator": {"argument_quality": 0, "evidence_use": 0, "logical_structure": 0, "total": 0}
        }
        self.feedback_history = [] 