from audio import Audio
import subprocess

class AudioPreprocessor:
    def __init__(self):
        pass

    def vocal_seperate(self, audio: Audio):
        """
        Separate the vocal from the audio file
        """
        pass

    def enhance_audio_volume(self, audio: Audio):
        """
        After demucs,
        Enhance the volume of the audio file
        """
        volume_ratio = 2.5
        ffmpeg_cmd = (
            f'ffmpeg -y -i "{audio.file_path}"'
            f'-filter:a "volume={volume_ratio}"'
            f'{audio.file_path.replace(audio.file_extension, f"_enhanced{audio.file_extension}")}'
        )
        subprocess.run(ffmpeg_cmd, shell=True)

    def compress_audio(self, audio: Audio):
        """
        Compress the audio file
        """
        pass

    