import time
from typing import List
from.models import DeviceRunningInfo
from utils import singleton, thread_decorator
from ascript.android.node import Selector
from ascript_utils import toast
import traceback


# 定义装饰器函数
def handle_listener_calls(func):
    def wrapper(self, *args):
        disactive_list = []
        for listener in AppSwitchManager().listeners:
            try:
                func(self, listener, *args)
            except BaseException as e:
                toast("程序出错", traceback.format_exc())
                traceback.print_exc()
                listener.is_active = false
                disactive_list.append(listener)
        listeners  = AppSwitchManager().listeners
        for listener in disactive_list:
            listeners.remove(listener)
                
    return wrapper


# 监听类
@singleton
class AppSwitchManager:
    
    """监听类，用于监听应用切换事件，并根据支持列表和使能状态调用相应监听对象的方法"""
    def __init__(self, period: float = 0.3):
        self.period = period  # 监听间隔时间
        self.listeners = []  # 监听对象列表
        self._run_state = False
        self._thread = None
        self.current_app = None
        self._selector_updated = False
        self._selector: Selector = None

    def start(self):
        self._thread = self._start()

    @thread_decorator()
    def _start(self):
        """启动监听，循环获取当前运行应用信息，检测应用切换并调用相应方法"""
        self._run_state = True
        while self._run_state:
            time.sleep(self.period)

            running_app_info = DeviceRunningInfo.get_running_app_info()
            if self.current_app is None or self.current_app.activity!= running_app_info.activity:

                self.current_app = running_app_info
                self._selector_updated = False
                
                self.handle_app_switch(self.current_app)

    def stop(self):
        self._run_state = False
        if self._thread:
            self._thread.join()
            self._thread = None

    def add_listener(self, listener):
        """添加监听对象到监听列表"""
        self.listeners.append(listener)

    def handle_app_switch(self, app_info):
        """处理应用切换事件，调用各个处理监听器回调函数的方法"""
        self.handle_awake(app_info)
        self.handle_on_enable(app_info)
        self.handle_on_switch(app_info)
        self.handle_on_disable(app_info)

    def get_selector(self):
        if not self._selector_updated:
            self._selector_updated = True
            self._selector = Selector(1|2)
        return self._selector
    
    @handle_listener_calls
    def handle_awake(self,listener, app_info):
        
        if not listener.initialized:
            listener.awake()
            listener.initialized = True
    
    
    @handle_listener_calls
    def handle_on_enable(self, listener, app_info):
        
        if app_info.package_name in listener.supported_packages or not listener.supported_packages:
            if not listener.enabled:
                listener.enabled = True
                listener.on_enable()

    
    @handle_listener_calls
    def handle_on_switch(self, listener, app_info):
        
        if app_info.package_name in listener.supported_packages or not listener.supported_packages:
            listener.on_switch(app_info)
    
    
    @handle_listener_calls
    def handle_on_disable(self,listener ,app_info):
        
        if listener.enabled and (app_info.package_name not in listener.supported_packages and listener.supported_packages):
            listener.enabled = False
            listener.on_disable()