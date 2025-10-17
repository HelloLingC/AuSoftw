from textual.widgets import ProgressBar, Label, Static
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from typing import Optional
from background_worker import TaskProgress, TaskStatus

class TaskProgressWidget(Static):
    """任务进度显示组件"""
    
    def __init__(self, task_id: str, task_name: str = "", **kwargs):
        super().__init__(**kwargs)
        self.task_id = task_id
        self.task_name = task_name
        self.progress_bar = ProgressBar(total=100, show_eta=False)
        self.status_label = Label("等待中...")
        self.message_label = Label("")
        
    def compose(self):
        with Vertical():
            if self.task_name:
                yield Label(f"[bold]{self.task_name}[/bold]")
            yield self.progress_bar
            yield self.status_label
            yield self.message_label
    
    def update_progress(self, progress: TaskProgress):
        """更新进度显示"""
        if progress.task_id != self.task_id:
            return
            
        # 更新进度条
        self.progress_bar.progress = int(progress.progress * 100)
        
        # 更新状态标签
        status_colors = {
            TaskStatus.PENDING: "yellow",
            TaskStatus.RUNNING: "blue", 
            TaskStatus.COMPLETED: "green",
            TaskStatus.FAILED: "red",
            TaskStatus.CANCELLED: "dim"
        }
        
        color = status_colors.get(progress.status, "white")
        self.status_label.update(f"[{color}]{progress.status.value}[/{color}]")
        
        # 更新消息
        if progress.message:
            self.message_label.update(progress.message)
        
        # 如果有错误，显示错误信息
        if progress.error:
            self.message_label.update(f"[red]错误: {progress.error}[/red]")

class ProcessingStatusWidget(Static):
    """处理状态总览组件"""
    
    active_tasks = reactive(0)
    completed_tasks = reactive(0)
    failed_tasks = reactive(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_widgets: dict[str, TaskProgressWidget] = {}
        
    def compose(self):
        with Vertical():
            yield Label("[bold]处理状态[/bold]")
            yield Label("", id="status_summary")
            yield Static("", id="task_list")
    
    def add_task(self, task_id: str, task_name: str = ""):
        """添加新任务"""
        task_widget = TaskProgressWidget(task_id, task_name)
        self.task_widgets[task_id] = task_widget
        
        # 添加到任务列表
        task_list = self.query_one("#task_list", Static)
        task_list.mount(task_widget)
        
        self.active_tasks += 1
        self._update_summary()
    
    def update_task(self, progress: TaskProgress):
        """更新任务进度"""
        if progress.task_id in self.task_widgets:
            self.task_widgets[progress.task_id].update_progress(progress)
            
            # 更新统计
            if progress.status == TaskStatus.COMPLETED:
                self.completed_tasks += 1
                self.active_tasks = max(0, self.active_tasks - 1)
            elif progress.status == TaskStatus.FAILED:
                self.failed_tasks += 1
                self.active_tasks = max(0, self.active_tasks - 1)
            
            self._update_summary()
    
    def _update_summary(self):
        """更新状态摘要"""
        summary = self.query_one("#status_summary", Label)
        summary.update(
            f"活跃: {self.active_tasks} | "
            f"完成: {self.completed_tasks} | "
            f"失败: {self.failed_tasks}"
        )
    
    def remove_task(self, task_id: str):
        """移除任务"""
        if task_id in self.task_widgets:
            self.task_widgets[task_id].remove()
            del self.task_widgets[task_id]
