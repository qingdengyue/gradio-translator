from translator import PDFTranslator, TranslationConfig
from utils import ArgumentParser, LOG
from translator.translation_chain import ModelType
import sys
import os
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


SOURCE_LANGUAGE = (
    ('简体中文', 'Chinese(Simplified)'),
    ('English', 'English'),
)


SOURCE_FORMAT = (
    ('PDF', 'pdf')
)


def translation(input_file, source_language, target_language, file_format):
    LOG.debug(
        f"[翻译任务]\n源文件:{input_file.name}\n源语言:{source_language}\n目标语言:{target_language}\n目标格式:{file_format}")

    output_file_path = Translator.translate_pdf(
        input_file.name,
        output_file_format=file_format,
        source_language=source_language,
        target_language=target_language
    )
    LOG.info(f"获取到翻译后文件地址:{output_file_path}")

    return output_file_path


def launch_gradio():

    iface = gr.Interface(
        fn=translation,
        title="OpenAITranslator",
        inputs=[
            gr.File(label="上传PDF文件"),
            gr.Dropdown(label="源语言（默认:简体中文）",
                        value="Chinese(Simplified)", choices=SOURCE_LANGUAGE),
            gr.Dropdown(label="目标语言（默认:英文）", value="English",
                        choices=SOURCE_LANGUAGE),
            gr.Dropdown(label="目标文件格式（默认:PDF）",
                        value="pdf", choices=SOURCE_FORMAT),
        ],
        outputs=[
            gr.File(label="下载翻译文件")
        ],
        allow_flagging="never"
    )

    iface.launch(share=True, server_name="0.0.0.0")


def initialize_translator():
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    config = TranslationConfig()
    config.initialize(args)
    if config.model_type == 'OpenAIModel':
        model_type = ModelType.OPENAI
    if config.model_type == 'GLMModel':
        model_type = ModelType.GLM

    global Translator
    Translator = PDFTranslator(model_name=config.model_name,
                               model_type=model_type, endpoint_url=config.glm_model_url)


if __name__ == "__main__":
    initialize_translator()
    launch_gradio()
