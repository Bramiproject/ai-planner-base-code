from langgraph.graph import StateGraph, END
from .agents import GraphState, researcher_node, analysis_node, report_writer_node

def create_workflow():
    """Membuat dan mengkompilasi graph LangGraph."""
    workflow = StateGraph(GraphState)

    # Menambahkan node ke graph
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyst", analysis_node)
    workflow.add_node("report_writer", report_writer_node)

    # Menentukan alur kerja
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", "report_writer")
    workflow.add_edge("report_writer", END)

    # Mengkompilasi graph menjadi objek yang bisa dijalankan
    app = workflow.compile()
    return app