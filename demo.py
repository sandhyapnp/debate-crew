#!/usr/bin/env python3
"""
Demo script for the Debate Crew system
Shows how the three agents work together
"""

import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from agents.topic_selector import TopicSelectorAgent
from agents.debator import DebatorAgent
from agents.critique import CritiqueAgent

load_dotenv()
console = Console()

def demo_topic_selection():
    """Demo the topic selection process."""
    console.print("\n[bold yellow]=== Topic Selection Demo ===[/bold yellow]")
    
    topic_selector = TopicSelectorAgent()
    
    # Simulate topic discovery
    console.print("User input: 'I'm interested in technology and education'")
    
    # Simulate topic suggestions
    suggested_topics = [
        "Should coding be mandatory in schools?",
        "Is online learning as effective as traditional education?",
        "Should social media be banned in schools?",
        "Are video games beneficial for learning?",
        "Should AI tools be allowed in academic work?"
    ]
    
    console.print("\n[green]Topic Selector Agent suggests:[/green]")
    for i, topic in enumerate(suggested_topics, 1):
        console.print(f"{i}. {topic}")
    
    # Simulate user selection
    selected_topic = suggested_topics[0]
    stance = "for"
    
    console.print(f"\n[blue]Selected: {selected_topic}[/blue]")
    console.print(f"[blue]Stance: {stance.upper()}[/blue]")
    
    return selected_topic, stance

def demo_debate_round(topic, stance, user_argument):
    """Demo a single debate round."""
    console.print(f"\n[bold cyan]=== Debate Round Demo ===[/bold cyan]")
    console.print(f"Topic: {topic}")
    console.print(f"User stance: {stance.upper()}")
    
    # Initialize agents
    debator = DebatorAgent()
    critique = CritiqueAgent()
    
    # User's argument
    console.print(f"\n[bold]User Argument:[/bold] {user_argument}")
    
    # Analyze user's argument
    user_analysis = critique.analyze_argument(user_argument, "user", "Demo round")
    console.print(f"\n[dim]Critique Analysis:[/dim] {user_analysis['feedback']}")
    
    # Debator's response
    debator_response = debator.build_argument(user_argument)
    console.print(f"\n[bold]Debator Response:[/bold] {debator_response}")
    
    # Analyze debator's response
    debator_analysis = critique.analyze_argument(debator_response, "debator", "Demo round")
    console.print(f"\n[dim]Critique Analysis:[/dim] {debator_analysis['feedback']}")
    
    # Display scores
    console.print("\n[bold]Current Scores:[/bold]")
    console.print(f"User - Argument Quality: {user_analysis['scores']['argument_quality']}")
    console.print(f"User - Evidence Use: {user_analysis['scores']['evidence_use']}")
    console.print(f"User - Logical Structure: {user_analysis['scores']['logical_structure']}")
    console.print(f"Debator - Argument Quality: {debator_analysis['scores']['argument_quality']}")
    console.print(f"Debator - Evidence Use: {debator_analysis['scores']['evidence_use']}")
    console.print(f"Debator - Logical Structure: {debator_analysis['scores']['logical_structure']}")

def demo_final_evaluation():
    """Demo the final evaluation process."""
    console.print("\n[bold yellow]=== Final Evaluation Demo ===[/bold yellow]")
    
    critique = CritiqueAgent()
    
    # Simulate final evaluation
    final_eval = {
        "overall_quality": "Good",
        "user_strengths": ["Clear communication", "Good engagement", "Logical thinking"],
        "debator_strengths": ["Strong argument structure", "Good evidence use", "Educational approach"],
        "improvement_areas": ["More specific examples", "Better counter-arguments", "Stronger evidence"],
        "educational_value": "High - excellent critical thinking development",
        "final_scores": {
            "user": {"argument_quality": 7, "evidence_use": 6, "logical_structure": 8, "total": 7},
            "debator": {"argument_quality": 8, "evidence_use": 8, "logical_structure": 9, "total": 8}
        }
    }
    
    console.print(Panel(
        f"[bold]Overall Quality:[/bold] {final_eval['overall_quality']}\n"
        f"[bold]Educational Value:[/bold] {final_eval['educational_value']}\n\n"
        f"[bold]User Strengths:[/bold]\n" + "\n".join(f"• {s}" for s in final_eval['user_strengths']) + "\n\n"
        f"[bold]Areas for Improvement:[/bold]\n" + "\n".join(f"• {a}" for a in final_eval['improvement_areas']),
        title="Final Evaluation", border_style="green"
    ))

def main():
    """Run the demo."""
    console.print(Panel(
        Text("🎭 Debate Crew Demo\n\nThis demo shows how the three agents work together:\n"
             "• Topic Selector: Discovers debate topics\n"
             "• Debator: Engages in educational debates\n"
             "• Critique: Analyzes and scores debate quality", 
             style="bold blue"),
        title="Debate Crew System Demo", 
        border_style="blue"
    ))
    
    # Demo topic selection
    topic, stance = demo_topic_selection()
    
    # Demo debate round
    sample_user_argument = "Coding should be mandatory because it teaches logical thinking and problem-solving skills that are valuable in any career."
    demo_debate_round(topic, stance, sample_user_argument)
    
    # Demo final evaluation
    demo_final_evaluation()
    
    console.print("\n[green]Demo completed! This shows how the three agents collaborate to create an educational debate experience.[/green]")

if __name__ == "__main__":
    main() 