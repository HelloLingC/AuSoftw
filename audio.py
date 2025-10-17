import os
from mutagen import File as MutagenFile

class Audio:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_extension = os.path.splitext(file_path)[1]
        self.file_size = os.path.getsize(file_path)
        self.file_created_time = os.path.getctime(file_path)
        self.file_modified_time = os.path.getmtime(file_path)

        metadata = self._get_audio_metadata()
        self.duration = metadata["duration"]
        self.bitrate = metadata["bitrate"] # kbps
    
    def _get_audio_metadata(self):
        """获取音频文件时长（秒）"""
        try:
            audio_file = MutagenFile(self.file_path)
            if audio_file is not None and hasattr(audio_file, 'info'):
                return {
                    "duration": int(audio_file.info.length),
                    "bitrate": audio_file.info.bitrate / 1000,
                }
            return {
                "duration": 0,
                "bitrate": 0,
            }
        except Exception:
            return {
                "duration": 0,
                "bitrate": 0,
            }
    
    def get_formatted_size(self):
        """格式化文件大小显示"""
        size = self.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
    
    def get_formatted_duration(self):
        """格式化时长显示（分:秒）"""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes:02d}:{seconds:02d}"
