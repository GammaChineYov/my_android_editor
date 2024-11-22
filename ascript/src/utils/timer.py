import threading
import time

class FlushTimer:
    def __init__(self, interval, callback):
        """
        初始化定时器

        :param interval: 定时器的总时长（秒）
        :param callback: 定时器结束时触发的回调函数
        """
        self.interval = interval
        self.callback = callback
        self.timer = None
        self.is_running = False

    def _countdown(self):
        while self.timer > 0:
            time.sleep(0.1)
            self.timer -= 0.1
        if self.is_running:
            self.callback()
            self.is_running = False

    def start(self):
        """
        启动定时器，如果定时器已经在运行，则不重复启动，而是重置定时器
        """
        if not self.is_running:
            self.timer = self.interval
            self.is_running = True
            self.timer_thread = threading.Thread(target=self._countdown)
            self.timer_thread.start()
        else:
            self.reset()

    def reset(self):
        """
        重置定时器，将定时器的剩余时间重新设置为初始值
        """
        if self.is_running:
            self.timer = self.interval