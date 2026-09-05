from src.langraphagenticai.UI.streamlit.display_result import DisplayResultStreamlit
import streamlit as st
from src.langraphagenticai.UI.streamlit.loadui import LoadUI
from src.langraphagenticai.LLMS.groqllm import GroqLLM
from src.langraphagenticai.graph.graph_builder import GraphBuilder


def load_langraph_agenticai_ui():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while
    implementing exception handling for robustness.
    """

    ## Load UI
    ui = LoadUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

    model = None
    if user_input.get("selected_llm") == "Groq":
        try:
            groq_llm = GroqLLM(user_input)
            model = groq_llm.get_llm_model()
        except Exception as e:
            st.error(f"Error initializing LLM: {e}")
            return

    if not model:
        st.info("👈 Please enter your Groq API Key in the sidebar to start chatting.")

    # Initialize and set up the graph based on use case
    usecase = user_input.get("selected_usecase")

    if not usecase:
        st.error("Error: No use case selected.")
        return

    if user_input.get("TAVILY_API_KEY"):
        import os
        os.environ["TAVILY_API_KEY"] = user_input["TAVILY_API_KEY"].strip()

    user_message = st.chat_input("Enter your message:")

    if user_message:
        if not model:
            st.error("⚠️ Please enter your Groq API Key in the sidebar before sending messages.")
            return

        if usecase in ["Chatbot With Web", "Chatbot with Web", "Chatbot with Tools"] and not user_input.get("TAVILY_API_KEY"):
            st.error("⚠️ Please enter your Tavily API Key in the sidebar to use web search.")
            return

        ## Graph Builder
        graph_builder = GraphBuilder(model)
        try:
            graph = graph_builder.setup_graph(usecase)
            DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
        except Exception as e:
            st.error(f"Error: {e}")
            return


