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

        # Support pre-filling from Streamlit Secrets or Environment Variables
        default_groq_key = os.environ.get("GROQ_API_KEY", "")
        default_tavily_key = os.environ.get("TAVILY_API_KEY", "")
        try:
            if not default_groq_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                default_groq_key = str(st.secrets["GROQ_API_KEY"])
        except Exception:
            pass

        try:
            if not default_tavily_key and hasattr(st, "secrets") and "TAVILY_API_KEY" in st.secrets:
                default_tavily_key = str(st.secrets["TAVILY_API_KEY"])
        except Exception:
            pass

        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                groq_key_input = st.text_input(
                    "API Key",
                    value=st.session_state.get("GROQ_API_KEY", default_groq_key),
                    type="password",
                    key="groq_key_input"
                )
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = groq_key_input

                # Validate API key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")

                # Model selection - default to curated lightweight free models
                model_options = self.config.get_groq_model_options()

                # Dynamically fetch available chat models for this specific API key if provided
                clean_key = groq_key_input.strip().strip("'\"") if isinstance(groq_key_input, str) else ""
                if clean_key:
                    try:
                        from groq import Groq
                        client = Groq(api_key=clean_key)
                        live_models = [
                            m.id for m in client.models.list().data
                            if not any(x in m.id.lower() for x in [
                                'whisper', 'embed', 'guard', 'safeguard', 'orpheus', 'tts', 'audio', 'distil'
                            ])
                        ]
                        if live_models:
                            # Prioritize lightweight, fast, free chat models
                            preferred = [
                                "openai/gpt-oss-20b",
                                "qwen/qwen3.8-27b",
                                "qwen/qwen3.6-27b",
                                "groq/compound-mini",
                                "openai/gpt-oss-120b",
                            ]
                            sorted_models = [m for m in preferred if m in live_models] + [
                                m for m in live_models if m not in preferred
                            ]
                            if sorted_models:
                                model_options = sorted_models
                    except Exception:
                        pass

                # Preserve selection so it NEVER auto-changes on rerun
                prev_selected = st.session_state.get("selected_groq_model_state", model_options[0])
                model_index = model_options.index(prev_selected) if prev_selected in model_options else 0

                selected_model = st.selectbox(
                    "Select Model",
                    model_options,
                    index=model_index,
                    key="selected_groq_model_state"
                )
                self.user_controls["selected_groq_model"] = selected_model
            
            ## USecase selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)

            if self.user_controls["selected_usecase"] in ["Chatbot With Web", "Chatbot with Web", "AI News"]:
                selected_model = self.user_controls.get("selected_groq_model", "")
                if any(x in selected_model.lower() for x in ['allam', 'deepseek', 'gemma']):
                    st.warning(f"⚠️ Model `{selected_model}` does not support tool calling. Please choose **openai/gpt-oss-20b** or **qwen/qwen3.8-27b** for web search / AI news.")

                tavily_key_input = st.text_input(
                    "TAVILY API KEY",
                    value=st.session_state.get("TAVILY_API_KEY", default_tavily_key),
                    type="password",
                    key="tavily_key_input"
                )
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = tavily_key_input

                # Validate API key
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY_API_KEY key to proceed. Don't have? refer : https://app.tavily.com/home")

            if self.user_controls['selected_usecase']=="AI News":
                st.subheader("📰 AI News Explorer ")
                
                time_frame = st.selectbox(
                    "📅 Select Time Frame",
                    ["Daily", "Weekly", "Monthly"],
                    index=0,
                    key="news_timeframe_select"
                )
                if st.button("🔍 Fetch Latest AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame

                self.user_controls["timeframe"] = st.session_state.get("timeframe", time_frame)
                self.user_controls["IsFetchButtonClicked"] = st.session_state.get("IsFetchButtonClicked", False)

        return self.user_controls

LoadUI = LoadStreamlitUI