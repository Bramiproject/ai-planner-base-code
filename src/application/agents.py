from typing import List, TypedDict, Annotated
from langchain_core.messages import BaseMessage
from .prompts import (
    ANALYSIS_PROMPT,
    REPORT_WRITER_PROMPT
)
from ..infrastructure.llm import get_model
from ..infrastructure.tools import get_tavily_search_tool
from ..domain.market_analysis import MarketAnalysis

# Mendefinisikan state yang akan melewati graph
class GraphState(TypedDict):
    initial_query: str
    research_results: str
    analysis_results: MarketAnalysis
    final_report: str
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]

def researcher_node(state: GraphState):
    """
    Node untuk agen peneliti: mencari informasi relevan di web.
    """
    print("---🔍 MASUK NODE PENELITI---")
    query = state["initial_query"]
    model = get_model()
    search_tool = get_tavily_search_tool()

    # --- PERUBAHAN DI SINI ---
    # Alih-alih membiarkan model memilih ("auto"), kita paksa untuk menggunakan tool ini.
    model_with_tools = model.bind_tools(
        [search_tool],
        # Memaksa model untuk memanggil tool yang tersedia.
        # "any" akan memilih salah satu jika ada banyak, 
        # karena Anda hanya punya satu, ini akan memilih search_tool.
        tool_choice="any" 
    )
    # -------------------------

    print(f"Memanggil model dengan paksaan tool untuk query: {query}")
    response = model_with_tools.invoke(query)

    # Tangani tool call atau jawaban langsung
    tool_output = ""
    # Dengan tool_choice="any", response hampir pasti akan memiliki tool_calls
    if hasattr(response, "tool_calls") and response.tool_calls:
        print("Model memanggil tool...")
        for tool_call in response.tool_calls:
            args = tool_call["args"] if isinstance(tool_call, dict) else tool_call.args
            print(f"Argumen tool: {args}")
            tool_output += str(search_tool.invoke(args)) + "\n\n"
    else:
        # Bagian ini kemungkinan besar tidak akan berjalan dengan tool_choice="any"
        print("Model menjawab langsung (tidak terduga)...")
        tool_output = response.content

    print(f"---✅ HASIL PENELITIAN---\n{tool_output[:200]}...") # Dibatasi agar tidak terlalu panjang di log
    return {"research_results": tool_output}

def analysis_node(state: GraphState):
    """
    Node untuk agen analis: menganalisis data mentah dan mengubahnya menjadi struktur.
    """
    print("---📊 MASUK NODE ANALIS---")
    research_data = state["research_results"]
    
    # Menggunakan model yang diinstruksikan untuk menghasilkan output terstruktur (Pydantic)
    structured_llm = get_model().with_structured_output(MarketAnalysis)
    
    prompt = ANALYSIS_PROMPT.format(research_data=research_data)
    
    analysis = structured_llm.invoke(prompt)
    
    print("---✅ HASIL ANALISIS (TERSTRUKTUR)---")
    print(analysis)
    return {"analysis_results": analysis}

def report_writer_node(state: GraphState):
    """
    Node untuk agen penulis laporan: membuat laporan akhir dalam format Markdown.
    """
    print("---✍️ MASUK NODE PENULIS LAPORAN---")
    analysis_data = state["analysis_results"]
    query = state["initial_query"]

    analysis_data_tojson = analysis_data.model_dump_json()
    print(f"---📄 QUERY: {query}---")
    print(f"---📊 DATA ANALISIS: {analysis_data_tojson}...")
    
    model = get_model()
    
    prompt = REPORT_WRITER_PROMPT.format(
        # query=query,
        analysis_data=analysis_data_tojson # Mengubah Pydantic model ke string JSON
    )
    
    report = model.invoke(prompt)
    
    print("---✅ LAPORAN FINAL DIBUAT---")
    return {"final_report": report.content}