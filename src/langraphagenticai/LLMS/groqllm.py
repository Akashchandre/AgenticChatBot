import os
import streamlit as st
from langchain_groq import ChatGroq



class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        groq_api_key = self.user_controls_input.get("GROQ_API_KEY", "")
        if isinstance(groq_api_key, str):
            groq_api_key = groq_api_key.strip().strip("'\"")

        if not groq_api_key:
            groq_api_key = os.environ.get("GROQ_API_KEY", "")
        if not groq_api_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            groq_api_key = str(st.secrets["GROQ_API_KEY"]).strip().strip("'\"")

        selected_groq_model = self.user_controls_input.get("selected_groq_model", "")
        if isinstance(selected_groq_model, str):
            selected_groq_model = selected_groq_model.strip()

        # If no key is entered yet, return None so UI loads cleanly
        if not groq_api_key:
            return None

        try:
            llm = ChatGroq(groq_api_key=groq_api_key, model=selected_groq_model)
            return llm
        except Exception as e:
            raise ValueError(f"Error initializing ChatGroq: {e}")
