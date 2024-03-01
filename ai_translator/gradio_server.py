import sys
import os
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser,LOG

from translator import PDFTranslator,TranslationConfig

def translation(input_file,source_language,target_language):
    LOG.debug(f"[翻译任务]\n源文件:{input_file.name}\n源语言:{source_language}\n目标语言:{target_language}")

    output_file_path=Translator.translate_pdf(
        input_file.name,
        source_language=source_language,
        target_language=target_language
    )

    return output_file_path


def launch_gradio():

    iface=gr.Interface(
        fn=translation,
        title="OpenAITranslator",
        inputs=[
                   gr.File(label="上传PDF文件"),
                   gr.Textbox(label="源语言（默认:英文）",placeholder="English",value="English"),
                   gr.Textbox(label="目标语言（默认:中文）",placeholder="Chinese",value="Chinese"),
        ],
        outputs=[
            gr.File(label="下载翻译文件")
        ],
        allow_flagging="never"
    )

    iface.launch(share=True,server_name="0.0.0.0")


def initialize_translator():
    argument_parser=ArgumentParser()
    args=argument_parser.parse_arguments()

    config=TranslationConfig()
    config.initialize(args)

    global Translator
    Translator=PDFTranslator(config.model_name)




if __name__ == "__main__":
    initialize_translator()
    launch_gradio()