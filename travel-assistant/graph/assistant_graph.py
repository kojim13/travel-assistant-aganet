from langgraph.graph import StateGraph, END
from .state import AssistantState
from nodes.node import run_router_node, run_packing_node, run_destination_node, run_attractions_node, run_planner_node, run_summary_node, run_next_node_in_plan



def handle_irrelevant(state: AssistantState) -> AssistantState:
    """Handle queries that are not related to travel assistance."""
    state.output = "I'm sorry, I don't understand your request. I am a travel assistant, I can help you plan your trip, but I can't help you with that."
    return state


builder = StateGraph(state_schema=AssistantState)


builder.add_node("router", run_router_node)
builder.add_node("packing", run_packing_node)
builder.add_node("destination", run_destination_node)
builder.add_node("attractions", run_attractions_node)
builder.add_node("irrelevant", handle_irrelevant)
builder.add_node("planner", run_planner_node)
builder.add_node("plan_executor", run_next_node_in_plan)
builder.add_node("summary", run_summary_node)



builder.set_entry_point("router")


builder.add_conditional_edges(
    "router",
    lambda state: state.route,
    path_map={
        "packing": "packing",
        "destination": "destination",
        "planner": "planner",
        "attractions": "attractions",
        "irrelevant": "irrelevant"
    }
)


builder.add_edge("planner", "plan_executor")

builder.add_conditional_edges(
    "plan_executor",
    lambda state: "plan_executor" if state.next_steps else "summary"
)

builder.add_edge("summary", END)
builder.add_edge("packing", END)
builder.add_edge("destination", END)
builder.add_edge("attractions", END)
builder.add_edge("irrelevant", END)

assistant_graph = builder.compile()
