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
        if not default_groq_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            default_groq_key = str(st.secrets["GROQ_API_KEY"])

        default_tavily_key = os.environ.get("TAVILY_API_KEY", "")
        if not default_tavily_key and hasattr(st, "secrets") and "TAVILY_API_KEY" in st.secrets:
            default_tavily_key = str(st.secrets["TAVILY_API_KEY"])

        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                # Model selection - only verified, working models from config
                model_options = self.config.get_groq_model_options()
                
                selected_model = st.selectbox(
                    "Select Model",
                    model_options,
                    index=0,
                    key="groq_model_select"
                )
                self.user_controls["selected_groq_model"] = selected_model

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
            
            ## USecase selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)

            if self.user_controls["selected_usecase"] in ["Chatbot With Web", "Chatbot with Web", "AI News"]:
                selected_model = self.user_controls.get("selected_groq_model", "")
                if any(x in selected_model.lower() for x in ['allam', 'deepseek', 'gemma']):
                    st.warning(f"⚠️ Model `{selected_model}` does not support tool calling. Please choose **llama-3.3-70b-versatile** or **llama-3.1-8b-instant** for web search / AI news.")

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