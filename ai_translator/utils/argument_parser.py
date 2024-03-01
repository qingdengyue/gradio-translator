import argparse
from .logger import LOG
import os

class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Translate English PDF book to Chinese.')
        self.parser.add_argument('--config', type=str, default='config.yaml',
                                 help='Configuration file with mode and API settings.')
        self.parser.add_argument('--model_type', type=str, required=True, choices=[
                                 'GLMModel', 'OpenAIModel'], help='The type of translation model to use.Choose between "GLMModel" and "OpenAIModel".')
        self.parser.add_argument(
            '--glm_model_url', type=str, help='The URL of the ChatGLM model URL.')
        self.parser.add_argument(
            '--timeout', type=int, help='Timeout for the API request in seconds.')
        self.parser.add_argument(
            '--openai_model', type=str, help='The model name of OPenAI Model.Required if model_type is "OpenAIModel".')
        self.parser.add_argument('--openai_api_key', type=str,
                                 help='The API key for OpenAIModel.Required if model_type is "OpenAIModel".')
        self.parser.add_argument(
            '--book', type=str, help="PDF file to translate.")
        self.parser.add_argument(
            '--file_format', type=str, help='The file format of translated book.Now supporting PDF and markdown')

    def parse_arguments(self):
        args = self.parser.parse_args()
        if args.model_type == 'OpenAIModel' and not args.openai_model:
           LOG.warning(f"openai_model not configured.will using default openai_model gpt-3.5-turbo")
           args.openai_model = "gpt-3.5-turbo"

        if args.model_type == 'OpenAIModel' and not args.openai_api_key:
            LOG.warning(f"openai_api_key not configured from config.yaml.will using default env() value")
            args.openai_api_key = os.getenv("OPENAI_API_KEY")

        if args.model_type == 'OpenAIModel' and not args.openai_api_key:
            self.parser.error('--openai_api_key not found when using OpenAIModel');
      
        return args
