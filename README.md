# Travel Assistant LLM

A conversational AI travel planning assistant that helps users plan trips by providing recommendations for destinations, packing lists, attractions, and creating comprehensive travel plans.

## Technologies Used

- **LangChain**: Framework for developing applications powered by language models
- **LangGraph**: Used for creating the assistant's workflow as a graph
- **Ollama**: Local LLM integration
- **Python**: Core programming language
- **Pydantic**: Data validation and settings management

## Project Structure

The application is structured as a graph-based state machine with the following components:

- **Router**: Classifies user requests into categories (packing, destination, attractions, planner)
- **Nodes**: Specialized agents for handling different types of travel queries
- **State Management**: Maintains conversation context and plan progress

## Setup Instructions

### Prerequisites

- Python 3.8+
- Ollama installed locally (for LLM)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd travel-assistant-llm
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Make sure Ollama is running locally with the llama3 model:
   ```
   ollama pull llama3
   ollama serve
   ```

### Running the Application

1. Start the travel assistant:
   ```
   python travel-asistant/main.py
   ```

2. Interact with the assistant by typing your travel questions.
   - Ask about destinations: "Where should I go in Europe?"
   - Get packing advice: "What should I pack for Thailand in November?"
   - Learn about attractions: "What are the best things to do in Tokyo?"
   - Plan a complete trip: "Help me plan a 7-day trip to Spain"

3. Type 'exit' or 'quit' to end the session.

## Environment Variables

You can customize the application by setting environment variables in a `.env` file:
LLM_MODEL=llama3