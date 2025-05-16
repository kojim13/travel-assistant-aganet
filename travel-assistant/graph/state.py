from pydantic import BaseModel
from pydantic import Field
from typing import List, Dict, Any, Annotated
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage
from langgraph.graph.message import add_messages

class AssistantState(BaseModel):
    """State management for the travel assistant."""
    input: str
    output: str = ""
    route: str = ""
    plan: Dict[str, str] = Field(default_factory=dict)
    next_steps: List[str] = None
    next_step: str = None
    sub_output: Dict[str, str] = Field(default_factory=dict)
    messages: Annotated[List[AnyMessage], add_messages] = Field(default_factory=list)
    summary_output: str = ""

    
    

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        # Truncate content if too long
        if len(content) > 1000:
            content = content[:500] + "..."
            
        message_class = HumanMessage if role == "user" else AIMessage
        self.messages.append(
            message_class(content=content)
        )
        
    
    
    def get_recent_messages(self) -> List[HumanMessage | AIMessage]:
        """Get the n most recent messages for context."""
        
        if not self.messages:
            return
        
        
        human_messages = [msg for msg in self.messages if msg.type == "human"] if self.messages else []
        
        
        ai_messages = [msg for msg in self.messages if msg.type == "ai"] if self.messages else []
        last_ai = [ai_messages[-1]] if ai_messages else []
        
        # Combine human messages with last AI message to maintain conversation history and follow up questions
        context_messages = human_messages + last_ai
        return context_messages 
 
    
    def get_context(self) -> str:
        """Get the current context including recent messages."""
        recent_messages = self.get_recent_messages()
        if len(recent_messages) == 1:
            return self.input
        
        context = f"Previous conversation about {self.route}:\n"
        for msg in recent_messages:
            context += f"{msg.type.upper()}: {msg.content}\n"
        context += f"\nCurrent question: {self.input}"
        
        return context
       

         