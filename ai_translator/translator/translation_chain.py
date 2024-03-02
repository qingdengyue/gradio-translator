from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain_community.llms.chatglm3 import ChatGLM3
from enum import Enum, auto

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from utils import LOG


class ModelType(Enum):
    OPENAI = auto()
    GLM = auto()


class TranslationChain:
    def __init__(self, model_name: str = "gpt-3.5-turbo", model_type: ModelType = ModelType.OPENAI, endpoint_url: str = None, verbose: bool = True):
        template = (
            """You are a translation expert,proficient in various languages.\n
            Translates {source_language} to {target_language}.
            保留(空格，分隔符、换行符)，只翻译文字内容。不增加任何前缀。：
            """
        )

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            template)

        human_template = "{text}"
        human_message_template = HumanMessagePromptTemplate.from_template(
            human_template)

        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_template]
        )

        if model_type == ModelType.OPENAI:
            chat = ChatOpenAI(model_name=model_name,
                              temperature=0, verbose=verbose)
            LOG.info(f"OpenAI Enabled")

        if model_type == ModelType.GLM:
            chat = ChatGLM3(
                endpoint_url=endpoint_url,
                max_tokens=8000,
                temperature=0,
                verbose=verbose
            )
            LOG.info(f"GLM Enabled.endpoint_url:{endpoint_url}")


        self.chain = LLMChain(
            llm=chat, prompt=chat_prompt_template, verbose=verbose)

    def run(self, text: str, source_language: str, target_language: str) -> (str, bool):
        result = ""
        try:
            result = self.chain.run({
                "text": text,
                "source_language": source_language,
                "target_language": target_language
            })
        except Exception as e:
            LOG.error(f"An error occurred during translation:{e}")
            return result, False

        return result, True
