import streamlit as st
import os
from src.langraphagenticai.UI.streamlit.uiconfigfile import UIConfigFile as Config
from src.langraphagenticai.UI.streamlit.uiconfigfile import UIConfigFile

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())
        if "timeframe" not in st.session_state:
            st.session_state.timeframe = ""
        if "IsFetchButtonClicked" not in st.session_state:
            st.session_state.IsFetchButtonClicked = False


        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                # Model selection
                model_options = self.config.get_groq_model_options()

                # If user entered an API key, dynamically load all models accessible to this key
                groq_key = st.session_state.get("GROQ_API_KEY", "")
                if groq_key and isinstance(groq_key, str) and groq_key.strip():
                    try:
                        from groq import Groq
                        client = Groq(api_key=groq_key.strip().strip("'\""))
                        live_models = [
                            m.id for m in client.models.list().data 
                            if not any(x in m.id.lower() for x in ['whisper', 'embed', 'guard', 'safetensors'])
                        ]
                        if live_models:
                            priority_models = [
                                "llama-3.3-70b-versatile",
                                "llama-3.1-8b-instant",
                                "llama-3.2-11b-vision-preview",
                                "llama-3.2-3b-preview",
                                "llama-3.2-1b-preview",
                                "qwen-2.5-32b",
                            ]
                            model_options = [m for m in priority_models if m in live_models] + [
                                m for m in live_models if m not in priority_models
                            ]
                    except Exception:
                        pass

                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type="password")
                # Validate API key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
            
            ## USecase selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)

            if self.user_controls["selected_usecase"] in ["Chatbot With Web", "Chatbot with Web", "AI News"]:
                selected_model = self.user_controls.get("selected_groq_model", "")
                if any(x in selected_model.lower() for x in ['allam', 'deepseek', 'gemma']):
                    st.warning(f"⚠️ Model `{selected_model}` does not support tool calling. Please choose **llama-3.3-70b-versatile** or **llama-3.1-8b-instant** for web search.")

                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("TAVILY API KEY", type="password")

                # Validate API key
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY_API_KEY key to proceed. Don't have? refer : https://app.tavily.com/home")

            if self.user_controls['selected_usecase']=="AI News":
                st.subheader("📰 AI News Explorer ")
                
                with st.sidebar:
                    time_frame = st.selectbox(
                        "📅 Select Time Frame",
                        ["Daily", "Weekly", "Monthly"],
                        index=0
                    )
                if st.button("🔍 Fetch Latest AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame

                self.user_controls["timeframe"] = st.session_state.get("timeframe", time_frame)
                self.user_controls["IsFetchButtonClicked"] = st.session_state.get("IsFetchButtonClicked", False)

        return self.user_controls

LoadUI = LoadStreamlitUI