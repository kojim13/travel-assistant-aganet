from dotenv import load_dotenv
from graph.assistant_graph import assistant_graph
from graph.state import AssistantState


load_dotenv()  

def format_message(role: str, content: str) -> str:
    """Format a message for display."""
    return f"\n{role.upper()}: {content}\n"

def main():
    print("Travel Assistant is ready. Type 'exit' to quit.")
    print("------------------------------------------------")
    
    
    state = AssistantState(input="")
    
    while True:
        
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
            
        state.input = user_input
        
        # Add user message to history
        state.add_message("user", user_input)
        
        #try:
        # Process through the graph
        response = assistant_graph.invoke(state)
    
        # Handle the response based on its type
        if isinstance(response, dict):
            # If response is a dictionary, extract the output
            output = response.get('output', '')
        else:
            # If response is a state object, use its output
            output = response.output if hasattr(response, 'output') else str(response)
        
        # Add assistant response to history
        state.add_message("assistant", output)
        
        
        print(format_message("assistant", output))
            
       #except Exception as e:
            # error_message = f"I encountered an error: {str(e)}"
            # state.add_message("assistant", error_message)
            # print(format_message("assistant", error_message))

if __name__ == "__main__":
    main()
