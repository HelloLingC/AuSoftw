from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable
from textual.widgets import Label, Button, Input, Markdown
from textual.containers import Horizontal, Vertical
from textual.events import Click

from audio_manager import AudioManager

audio_manager = AudioManager()

markdown_text = """
# Hello, World!
"""

class AudioListWidget(DataTable):
    """音频文件列表显示组件"""
    
    def __init__(self, id=None):
        super().__init__(id=id)
        self.cursor_type = "row"
        self.add_columns("Name", "Duration")
    
    def update_audio_list(self, audio_files):
        """更新音频文件列表"""
        self.clear()
        for audio in audio_files:
            if len(audio.file_name) > 20:
                name = audio.file_name[:20] + "..."
                name = f"[bold]{name}[/bold]"
            else:
                name = f"[bold]{audio.file_name}[/bold]"

            self.add_row(
                name,
                audio.get_formatted_duration()
            )

class AuSoftware(App):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Horizontal():
            with Vertical():
                yield Markdown(markdown_text)
                yield Label("输入音频文件夹路径:")
                yield Input(placeholder="输入文件夹路径", id="directory_input")
                with Horizontal():
                    yield Button("加载音频", variant="primary", id="load_button", flat=True)
                    yield Button("刷新列表", variant="default", id="refresh_button", flat=True)
                
            with Vertical():
                yield Label("已加载的音频文件:")
                yield AudioListWidget(id="audio_list")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击事件处理"""
        if event.button.id == "load_button":
            input_widget = self.query_one("#directory_input", Input)
            directory_path = input_widget.value
            
            if directory_path:
                try:
                    audio_manager.clear_audio_files()
                    audio_manager.load_audio_files(directory_path)
                    self.update_audio_display()
                    self.notify(f"成功加载 {len(audio_manager.audio_files)} 个音频文件")
                except Exception as e:
                    self.notify(f"加载失败: {str(e)}", severity="error")
            else:
                self.notify("请输入文件夹路径", severity="error")
        
        elif event.button.id == "refresh_button":
            self.update_audio_display()
            self.notify("列表已刷新")
    
    def update_audio_display(self):
        """更新音频列表显示"""
        audio_list_widget = self.query_one("#audio_list", AudioListWidget)
        audio_list_widget.update_audio_list(audio_manager.audio_files)

if __name__ == "__main__":
    app = AuSoftware()
    app.run()