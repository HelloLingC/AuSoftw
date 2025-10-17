import os
from audio import Audio
import audio_preprocessor
from agent.llm_spilitter import SplitterLLM
from agent.llm_translator import TranslatorLLM

class AudioManager:
    def __init__(self):
        self.accepted_file_types = (".mp3", ".wav", ".flac", ".m4a", ".aac")
        self.audio_files = []

    def add_audio_file(self, audio_file):
        self.audio_files.append(audio_file)

    def get_audio_files(self):
        return self.audio_files

    def clear_audio_files(self):
        self.audio_files = []
    
    # Load audio files from a directory
    def load_audio_files(self, directory):
        for file in os.listdir(directory):
            if file.endswith(self.accepted_file_types):
                self.add_audio_file(Audio(os.path.join(directory, file)))
        return self.audio_files

    def start_all(self):
        for audio in self.audio_files:
            audio_preprocessor.start_processing(audio)
            SplitterLLM().split(audio)
            TranslatorLLM().translate(audio)