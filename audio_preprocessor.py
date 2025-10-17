from audio import Audio
import subprocess
# import demucs.seperate

class AudioPreprocessor:
    def __init__(self):
        pass

    def start_processing(self, audio: Audio):
        """
        Start processing the audio file
        """
        self.vocal_seperate(audio)
        self.enhance_audio_volume(audio)
        self.compress_audio(audio)
        self.split_audio(audio)
        return audio

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
            f'{audio.file_path}.enhanced'
        )
        subprocess.run(ffmpeg_cmd, shell=True)

    def compress_audio(self, audio: Audio):
        """
        Compress the audio file
        """
        subprocess.run([
            'ffmpeg', '-y', '-i', f'{audio.file_path}.enhanced', '-vn', '-b:a', '96k',
            '-ar', '16000', '-ac', '1', '-metadata', 'encoding=UTF-8',
            '-f', 'mp3', f'{audio.file_path}.compressed'
        ], check=True, stderr=subprocess.PIPE)

    def _silence_detect(self, audio_file, start:float, end:float)->list[float]:
        cmd = ['ffmpeg', '-y', '-i', f'{audio_file}.compressed',
            '-ss', str(start), '-to', str(end),
            '-af', 'silencedetect=n=-30dB:d=0.5',
            '-f', 'null', '-']

        output = subprocess.run(cmd, capture_output=True, text=True,
                            encoding='utf-8').stderr

        return [float(line.split('silence_end: ')[1].split(' ')[0])
                for line in output.split('\n')
                if 'silence_end' in line]

    def split_audio(self, audio: Audio, frag_len:int=30*60, window: int=60) -> list[tuple[float, float]]:
        """
        Split audio into 30mins for whisper model
        The real split will happen when trascribe, whose output in SEGMENT_TEMP_PATH
        Return: segments - list of tuples (start_time, end_time)
        """
        duration = audio.duration
        segments = []
        pos = 0
        while pos < duration:
            if duration - pos < frag_len:
                segments.append((pos, duration))
                break
            win_start = pos + frag_len - window
            win_end = min(win_start + 2 * window, duration)
            silences = self._silence_detect(audio.file_path, win_start, win_end)

            if silences:
                target_pos = frag_len - (win_start - pos)
                split_at = next((t for t in silences if t - win_start > target_pos), None)
                if split_at:
                    segments.append((pos, split_at))
                    pos = split_at
                    continue
            segments.append((pos, pos + frag_len))
            pos += frag_len
        # Audio has been split into {} segments
        print(f"Audio has been split into {len(segments)} segments")
        return segments