from configparser import ConfigParser


class UIConfigFile:
    def __init__(self, config_file: str = "src/langraphagenticai/UI/streamlit/uiconfigfile.ini"):
        self.config_file = config_file
        self.config = ConfigParser()
        self.config.read(self.config_file)

    def get_config(self):
        return self.config

    def get_page_title(self):
        return self.config.get('DEFAULT', 'PAGE_TITLE')

    def get_llms_options(self):
        return [opt.strip() for opt in self.config.get('DEFAULT', 'LLMS_OPTIONS').split(',')]

    def get_llm_options(self):
        return self.get_llms_options()

    def get_use_case_options(self):
        return [opt.strip() for opt in self.config.get('DEFAULT', 'USE_CASE_OPTIONS').split(',')]

    def get_usecase_options(self):
        return self.get_use_case_options()

    def get_groq_model_options(self):
        return [opt.strip() for opt in self.config.get('DEFAULT', 'GROQ_MODEL_OPTIONS').split(',')]

