from . import AppSwitchManager
from .models import DeviceRunningInfo

# 监听对象基类
class Component:
    name = ""
    """监听对象基类，包含支持的包名列表、是否被禁用、是否使能等字段，以及相关方法"""
    def __init__(self, supported_packages=None, is_active: bool = True, enabled: bool = False, initialized: bool = False):
        self.supported_packages = supported_packages if supported_packages else [] # 支持的包名列表
        self.is_active = is_active  # 是否被禁用
        self.enabled = enabled  # 是否使能
        self.initialized = initialized  # 是否初始化
        self.switch_manager = AppSwitchManager()

    def awake(self):
        """启动监听对象，设置初始化状态为True"""
        self.initialized = True

    def on_enable(self):
        """当监听对象被使能时调用的方法，需在子类中实现"""
        pass
        
    def on_switch(self, app_info:DeviceRunningInfo):
        """当切换app的activity时调用的方法，需在子类中实现"""
        pass
    
    def on_disable(self):
        """当监听对象被禁用时调用的方法，需在子类中实现"""
        pass

    def on_destroy(self):
        """销毁监听对象，设置使能和初始化状态为False"""
        self.enabled = False
        self.initialized = False
    
    @property
    def cur_app_info(self) -> DeviceRunningInfo:
        return self.switch_manager.current_app
    
    @property
    def selector(self):
        return self.switch_manager.get_selector()