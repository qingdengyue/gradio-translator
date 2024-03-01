from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from utils import LOG


class TranslationChain:
    def __init__(self, model_name: str = "gpt-3.5-turbo", verbose: bool = True):
        template = (
            """You are a translation expert,proficient in various languages.\n
            Translates {source_language} to {target_language}.
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

        chat = ChatOpenAI(model_name=model_name,
                          temperature=0, verbose=verbose)

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
