#!/usr/bin/env python3
"""
Debate Crew - Main Application
An agentic debate system using CrewAI framework
"""

# TODO: The entire system has many static topics. We want to make it interactive. Frequently use agents to generate topics. 

import os
import sys
from typing import Dict, Any, List
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table

# Import our agents
from agents.topic_selector import TopicSelectorAgent
from agents.debator import DebatorAgent
from agents.critique import CritiqueAgent

# Load environment variables
load_dotenv()

class DebateCrew:
    def __init__(self):
        self.console = Console()
        self.topic_selector = TopicSelectorAgent()
        self.debator = DebatorAgent()
        self.critique = CritiqueAgent()
        
        self.current_topic = ""
        self.current_stance = ""
        self.debate_history = []
        self.is_debate_active = False
        
    def display_welcome(self):
        """Display welcome message and system overview."""
        welcome_text = Text()
        welcome_text.append("🎭 Debate Crew - Agentic Debate System\n\n", style="bold blue")
        welcome_text.append("Welcome to the intelligent debate system designed to teach through interactive debates!\n\n", style="green")
        welcome_text.append("This system features three specialized agents:\n", style="yellow")
        welcome_text.append("• Topic Selector: Helps you discover engaging debate topics\n", style="cyan")
        welcome_text.append("• Debator: Engages in comprehensive, educational debates\n", style="cyan")
        welcome_text.append("• Critique: Analyzes debate quality and provides scoring\n", style="cyan")
        
        self.console.print(Panel(welcome_text, title="Welcome to Debate Crew", border_style="blue"))
    
    def check_environment(self) -> bool:
        """Check if the environment is properly configured."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.console.print("[red]Error: OPENAI_API_KEY not found in environment variables![/red]")
            self.console.print("Please set your OpenAI API key in the .env file.")
            return False
        return True
    
    def topic_discovery_phase(self) -> bool:
        """Interactive topic discovery phase using agent-driven approach."""
        self.console.print("\n[bold yellow]Phase 1: Topic Discovery[/bold yellow]")
        self.console.print("Let's find the perfect debate topic for you!\n")
        
        # Get user input
        user_input = Prompt.ask(
            "What topic would you like to debate, or what are your interests?",
            default="I'm not sure, help me discover a topic"
        )
        
        # Use the Topic Selector agent to generate topics
        self.console.print("\n[cyan]Topic Selector Agent is researching and generating topics...[/cyan]")
        
        try:
            # Get topics from the agent
            suggested_topics = self.topic_selector.generate_topics(user_input)
            
            if not suggested_topics:
                self.console.print("[red]Error: Could not generate topics. Please try again.[/red]")
                return False
            
            # Display agent-generated topics
            self.console.print("\n[green]Here are some suggested debate topics:[/green]")
            for i, topic in enumerate(suggested_topics, 1):
                self.console.print(f"{i}. {topic}")
            
            # Let user select or suggest their own topic
            choice = Prompt.ask(
                "\nSelect a topic number, or type 'custom' for your own topic",
                choices=[str(i) for i in range(1, len(suggested_topics) + 1)] + ["custom"],
                default="1"
            )
            
            if choice == "custom":
                self.current_topic = Prompt.ask("Enter your debate topic")
            else:
                self.current_topic = suggested_topics[int(choice) - 1]
            
            self.console.print(f"\n[green]Selected topic: {self.current_topic}[/green]")
            
            # Determine stance
            self.console.print("\n[bold]Now let's determine your stance:[/bold]")
            stance_choice = Prompt.ask(
                f"Do you want to debate FOR or AGAINST: '{self.current_topic}'?",
                choices=["for", "against"],
                default="for"
            )
            
            self.current_stance = stance_choice
            self.console.print(f"[green]You will be debating {stance_choice.upper()} the topic![/green]")
            
            # Confirm start
            start_debate = Confirm.ask("\nReady to start the debate?", default=True)
            if not start_debate:
                self.console.print("[yellow]Debate cancelled. Goodbye![/yellow]")
                return False
            
            return True
            
        except Exception as e:
            self.console.print(f"[red]Error during topic discovery: {e}[/red]")
            return False
    

    
    def debate_phase(self):
        """Main debate phase with all three agents working together."""
        self.console.print("\n[bold yellow]Phase 2: Active Debate[/bold yellow]")
        self.console.print(f"Topic: {self.current_topic}")
        self.console.print(f"Your stance: {self.current_stance.upper()}\n")
        
        # Initialize debate
        opening_statement = self.debator.initialize_debate(self.current_topic, self.current_stance)
        self.console.print(Panel(f"[bold]Debator Agent:[/bold]\n{opening_statement}", 
                               title="Opening Statement", border_style="green"))
        
        self.debate_history.append(f"Debator: {opening_statement}")
        
        # Initialize critique agent
        self.critique.current_topic = self.current_topic
        self.critique.reset_scores()
        
        self.is_debate_active = True
        round_count = 1
        
        while self.is_debate_active:
            self.console.print(f"\n[bold cyan]--- Round {round_count} ---[/bold cyan]")
            
            # Get user's argument
            user_argument = Prompt.ask("\n[bold]Your argument[/bold] (or type 'exit' to end debate)")
            
            if user_argument.lower() in ['exit', 'quit', 'end']:
                self.is_debate_active = False
                break
            
            # Analyze user's argument
            user_analysis = self.critique.analyze_argument(user_argument, "user", 
                                                         f"Round {round_count} of debate on {self.current_topic}")
            self.critique.update_scores(user_analysis, "user")
            
            self.debate_history.append(f"User: {user_argument}")
            
            # Display critique feedback
            self.console.print(f"\n[dim]Critique: {user_analysis['feedback']}[/dim]")
            
            # Generate debator's response
            debator_response = self.debator.build_argument(user_argument)
            self.console.print(Panel(f"[bold]Debator Agent:[/bold]\n{debator_response}", 
                                   title="Response", border_style="blue"))
            
            self.debate_history.append(f"Debator: {debator_response}")
            
            # Analyze debator's response
            debator_analysis = self.critique.analyze_argument(debator_response, "debator",
                                                            f"Round {round_count} response")
            self.critique.update_scores(debator_analysis, "debator")
            
            # Track exchange quality
            exchange_quality = self.critique.track_debate_quality((user_argument, debator_response))
            
            # Display current scores
            self.display_current_scores()
            
            round_count += 1
            
            # Check if user wants to continue
            if round_count > 3:  # After 3 rounds, ask if they want to continue
                continue_debate = Confirm.ask(f"\nContinue for more rounds?", default=True)
                if not continue_debate:
                    self.is_debate_active = False
    
    def display_current_scores(self):
        """Display current debate scores."""
        scores = self.critique.get_current_scores()
        
        table = Table(title="Current Debate Scores")
        table.add_column("Participant", style="cyan")
        table.add_column("Argument Quality", style="green")
        table.add_column("Evidence Use", style="green")
        table.add_column("Logical Structure", style="green")
        table.add_column("Total", style="bold green")
        
        for participant, score_data in scores.items():
            table.add_row(
                participant.title(),
                str(score_data["argument_quality"]),
                str(score_data["evidence_use"]),
                str(score_data["logical_structure"]),
                str(score_data["total"])
            )
        
        self.console.print(table)
    
    def final_evaluation_phase(self):
        """Final evaluation and feedback phase."""
        self.console.print("\n[bold yellow]Phase 3: Final Evaluation[/bold yellow]")
        
        # Get final evaluation
        final_eval = self.critique.final_evaluation(self.debate_history)
        
        # Display final results
        self.console.print(Panel(
            f"[bold]Overall Quality:[/bold] {final_eval['overall_quality']}\n"
            f"[bold]Educational Value:[/bold] {final_eval['educational_value']}\n\n"
            f"[bold]Your Strengths:[/bold]\n" + "\n".join(f"• {s}" for s in final_eval['user_strengths']) + "\n\n"
            f"[bold]Areas for Improvement:[/bold]\n" + "\n".join(f"• {a}" for a in final_eval['improvement_areas']),
            title="Final Evaluation", border_style="green"
        ))
        
        # Display final scores
        self.display_current_scores()
        
        # Provide recommendations
        self.console.print("\n[bold cyan]Recommendations for Future Debates:[/bold cyan]")
        recommendations = [
            "Practice providing more specific evidence and examples",
            "Work on addressing counter-arguments more directly",
            "Focus on building stronger logical connections between points",
            "Consider the opposing viewpoint more thoroughly"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            self.console.print(f"{i}. {rec}")
    
    def run(self):
        """Main application loop."""
        self.display_welcome()
        
        if not self.check_environment():
            return
        
        try:
            while True:
                # Topic discovery phase
                if not self.topic_discovery_phase():
                    break
                
                # Debate phase
                self.debate_phase()
                
                # Final evaluation
                self.final_evaluation_phase()
                
                # Ask if user wants another debate
                another_debate = Confirm.ask("\nWould you like to start another debate?", default=False)
                if not another_debate:
                    self.console.print("\n[green]Thank you for using Debate Crew! Goodbye![/green]")
                    break
                
                # Reset for new debate
                self.debate_history = []
                self.current_topic = ""
                self.current_stance = ""
                self.is_debate_active = False
                
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Debate interrupted. Goodbye![/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]An error occurred: {e}[/red]")

def main():
    """Main entry point."""
    debate_crew = DebateCrew()
    debate_crew.run()

if __name__ == "__main__":
    main() 