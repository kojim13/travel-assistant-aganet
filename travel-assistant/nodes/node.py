from langchain_ollama import OllamaLLM
#from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_core.messages import AIMessage
from pydantic import BaseModel, Field
from typing import Literal, Dict

from langchain_core.prompts import ChatPromptTemplate
from graph.state import AssistantState
from llm.llm import get_model
import os
import json
from typing import Callable
from prompts.prompts import DESTINATION_PROMPT, PACKING_PROMPT, ATTRACTIONS_PROMPT, PLANNER_PROMPT, ROUTER_PROMPT, SUMMARY_PROMPT

class RouterResponse(BaseModel):
    route: Literal["packing", "destination", "attractions", "planner", "irrelevant"]

class PlannerResponse(BaseModel):
    steps: list[Literal["destination", "packing", "attractions"]]
    
class SummaryResponse(BaseModel):
    summary_result: str

# def call_llm(prompt: ChatPromptTemplate) -> ChatGoogleGenerativeAI:
#     return get_model()

def call_llm(prompt: ChatPromptTemplate) -> OllamaLLM:
    return get_model()
         
def run_actor_node(state: AssistantState, prompt: ChatPromptTemplate) -> AssistantState:
    model = get_model()
    chain = prompt | model
    context = state.get_context()
    #result: AIMessage = chain.invoke({"input": context}).content.strip().strip('"\'')
    result = chain.invoke({"input": context}).strip().strip('"\'')
    state.output = result
    return state

def run_router_node(state: AssistantState) -> AssistantState:
    prompt = ROUTER_PROMPT
    context = state.get_context()
    model = get_model()
    #chain = prompt | model.with_structured_output(RouterResponse)
    chain = prompt | model
    #result: AIMessage = chain.invoke({"input": context}).content.strip().strip('"\'')
    result = chain.invoke({"input": context}).strip().strip('"\'')
    parsed_result = RouterResponse(route=result)    
    state.route = parsed_result.route
    return state

def run_packing_node(state: AssistantState) -> AssistantState:  
    prompt = PACKING_PROMPT
    return run_actor_node(state, prompt)

def run_destination_node(state: AssistantState) -> AssistantState:
    prompt = DESTINATION_PROMPT
    return run_actor_node(state, prompt)

def run_attractions_node(state: AssistantState) -> AssistantState:
    prompt = ATTRACTIONS_PROMPT
    return run_actor_node(state, prompt)

def run_planner_node(state: AssistantState) -> AssistantState:
    prompt = PLANNER_PROMPT
    model = get_model()
    #chain = prompt | model.with_structured_output(PlannerResponse)
    chain = prompt | model
    result = chain.invoke({"input": state.input})
    parsed_result = PlannerResponse(steps=result.split("\n"))
    state.next_steps = parsed_result.steps
    state.next_step = state.next_steps[0] if state.next_steps else None
    return state

def run_summary_node(state: AssistantState) -> AssistantState:
    prompt = SUMMARY_PROMPT
    model = get_model()
    #chain = prompt | model.with_structured_output(SummaryResponse)
    chain = prompt | model
    result = chain.invoke({"input": state.sub_output})  
    parsed_result = SummaryResponse(summary_result=result)  
    state.output = parsed_result.summary_result
    return state    

def run_next_node_in_plan(state: AssistantState) -> AssistantState:
    node_map = {
        "destination": (run_destination_node, "destination"),
        "packing": (run_packing_node, "packing"), 
        "attractions": (run_attractions_node, "attractions")
    }

    if state.next_step in node_map:
        node_func, output_key = node_map[state.next_step]
        node_func(state)
        state.sub_output[output_key] = state.output

    # Update next steps
    remaining_steps = state.next_steps[1:] if state.next_steps else []
    state.next_steps = remaining_steps
    state.next_step = remaining_steps[0] if remaining_steps else None
    
    return state




        
               
        

