# Debate Crew - Agentic Debate System

An intelligent debate system built with CrewAI that teaches students through interactive debates.

## Requirements

- Python 3.11.9 or higher
- OpenAI API key

## Features

- **Topic Selector Agent**: Helps users discover and select debate topics through interactive questioning
- **Debator Agent**: Engages in comprehensive debates with strong arguments and counter-arguments
- **Critique Agent**: Analyzes debate quality and provides scoring for both participants

## Setup

1. Ensure you have Python 3.11.9 or higher installed:
```bash
python --version
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp env_example.txt .env
```

4. Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the debate system:
```bash
python main.py
```

Or run the demo to see how the system works:
```bash
python demo.py
```

Test the system to ensure everything is working:
```bash
python test_system.py
```

## System Architecture

### Topic Selector Agent
- Interactively asks questions to help users discover debate topics
- Can analyze resumes/portfolios to suggest relevant topics
- Determines user's stance (for/against) on the selected topic
- Allows users to exit the debate at any time

### Debator Agent
- Builds comprehensive arguments based on the selected topic and stance
- Maintains focus on the debate topic
- Understands and responds to human arguments
- Provides well-structured counter-arguments

### Critique Agent
- Analyzes the quality of arguments from both sides
- Tracks debate scores and provides feedback
- Evaluates argument structure, evidence, and logical flow
- Maintains running score throughout the debate

## Demo

The `demo.py` script provides a quick demonstration of how the three agents work together:

- **Topic Selection**: Shows how the Topic Selector agent suggests relevant debate topics
- **Debate Round**: Demonstrates a single debate exchange with analysis
- **Final Evaluation**: Shows the critique and scoring system

Run the demo with:
```bash
python demo.py
```

## Project Structure

```
debate-crew/
├── agents/
│   ├── __init__.py
│   ├── topic_selector.py
│   ├── debator.py
│   └── critique.py
├── main.py
├── demo.py
├── test_system.py
├── requirements.txt
├── env_example.txt
└── README.md 