# Alto AI Podcast

An AI-powered podcast simulation system featuring intelligent host and guest agents engaging in dynamic conversations.

## Features

- AI Host and Guest agents with distinct personalities and expertise
- Dynamic conversation flow management
- Topic-based discussion generation
- Console-based UI for interaction
- Modular architecture with separate agents, models, and UI components

## Prerequisites

- Python 3.9+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd alto-ai-podcast
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# OR
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
# OR add to your shell profile (.zshrc, .bashrc, etc.):
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
```

## Project Structure

```
alto-ai-podcast/
├── agents/         # AI agent implementations
├── context/        # Conversation context and topics
├── models/         # Data models and state management
├── ui/            # User interface components
└── main.py        # Application entry point
```

## Usage

Run the application:
```bash
python main.py
```

## Dependencies

Key dependencies include:
- pydantic-ai-slim - AI model integration
- fastapi - API framework
- rich - Terminal UI formatting
- gradio - Web UI components
- logfire - Logging system
