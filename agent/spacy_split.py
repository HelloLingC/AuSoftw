import pandas as pd
import spacy.cli
import spacy.cli.download
import env_check
import spacy
import os

# 常量定义
TRANSCRIPTION_SENT_PATH = "transcription_sent.txt"
SPLIT_LLM_PATH = "split_llm.txt"

# 配置映射
map = """
language_space_joiner: [en, es, fr, de, it, ru]
language_no_space_joiner: [zh, ja, ko]

spacy:
  model_map:
    en: en_core_web_md
    zh: zh_core_web_md
    ja: ja_core_web_md
    ko: ko_core_web_md
    fr: fr_core_web_md
    de: de_core_web_md
    es: es_core_web_md
    it: it_core_web_md
    pt: pt_core_web_md
    ru: ru_core_web_md
"""

# 配置相关函数
def get_config_value(key: str, default=None):
    """获取配置值，这里使用硬编码的默认值"""
    config_map = {
        'whisper.language': 'auto',
        'whisper.detected_language': 'en',
        'language_space_joiner': ['en', 'es', 'fr', 'de', 'it', 'ru'],
        'language_no_space_joiner': ['zh', 'ja', 'ko']
    }
    return config_map.get(key, default)

def prepare_spacy_model(lang: str):
    """准备spaCy模型"""
    if env_check.is_gpu_available():
        spacy.prefer_gpu()
        print("Using GPU for LLM splitting.")
    else:
        print("GPU not available, using CPU.")

    lang = get_config_value('whisper.language')
    # if whisper.language set auto
    if lang == 'auto':
        lang = get_config_value('whisper.detected_language')

    model_map = {
        'en': 'en_core_web_md',
        'zh': 'zh_core_web_md', 
        'ja': 'ja_core_web_md',
        'ko': 'ko_core_web_md',
        'fr': 'fr_core_web_md',
        'de': 'de_core_web_md',
        'es': 'es_core_web_md',
        'it': 'it_core_web_md',
        'pt': 'pt_core_web_md',
        'ru': 'ru_core_web_md'
    }
    
    model_name = model_map.get(lang, 'en_core_web_md')
    try:
        return spacy.load(model_name)
    except OSError:
        print(f"模型 {model_name} 未安装，尝试下载...")
        try:
            spacy.cli.download(model_name)
            return spacy.load(model_name)
        except Exception as e:
            print(f"下载模型失败: {e}")
            return spacy.load('en_core_web_sm')  # 使用小模型作为后备

def get_joiner(lang):
    if lang in get_config_value('language_space_joiner'):
        return " "
    elif lang in get_config_value('language_no_space_joiner'):
        return ""
    else:
        print(f"Language {lang} not supported for joining.")
        return " "
