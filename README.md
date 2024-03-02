# AI文件翻译

## 简介

OpenAITranslator文件翻译是一款基于集成了ChatGPT和GLM文件翻译工具，支持简体中文翻译到英文 


## 准备环境: 
- 安装Miniconda [参考官方文档](https://docs.anaconda.com/free/miniconda/index.html)
- 创建并激活新的虚拟环境（可选）
  ```bash
  conda create -n gradio-translator python=3.10
  conda activate gradio-translator
  ``` 

## 启动:
  ```bash
  pip install -r requirements.txt
  ```

### ChatGPT模式:
  为了方便使用,需要确保环境变量中存在 OPENAI_API_KEY
  ```bash
  python3 ./ai_translator/gradio_server.py --model_type=OpenAIModel --config_file=/home/ruilong/gradio-translator/ai_translator/config.yaml 
  ```

### GLM模式:
  默认支持ChatGLM3-6B,API方式部署，需要以OpenAI格式的开源模型部署代码。 可以参考：[本地化部署](https://github.com/li-plus/chatglm.cpp)
  ```bash
  python3 ./ai_translator/gradio_server.py --model_type=GLMModel --config_file=/home/ruilong/gradio-translator/ai_translator/config.yaml --glm_model_url=http://127.0.0.1:8010/v1/chat/completions
  ```
