from langgraph.graph import StateGraph, END
from .agents import GraphState, researcher_node, analysis_node, planner_node, syllabus_creation_node

def create_workflow():
    """Creates and compiles the LangGraph workflow without transformer agent."""
    workflow = StateGraph(GraphState)

    # Add nodes to graph
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyst", analysis_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("syllabus", syllabus_creation_node)

    # Define workflow: researcher -> analyst -> planner -> syllabus
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", "planner")
    workflow.add_edge("planner", "syllabus")
    workflow.add_edge("syllabus", END)

    # Compile graph into executable object
    app = workflow.compile()
    return app