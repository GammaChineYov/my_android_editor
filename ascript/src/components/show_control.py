from core import Component
from intent_helper import IntentHelper
from core.float_window import FloatWindow
from ascript_utils import promt,toast
from ascript_utils import Config

class ShowControl(Component):
    name = "悬浮窗显示控制"
    
    def awake(self):
        self.float_window = FloatWindow()
        self.is_show_all=False
        self.system_table_package = Config().get("system_table_package")
        toast("桌面设置", self.system_table_package)
    
    def on_enable(self):
        app_info = self.cur_app_info
        if not self.system_table_package:
            self.float_window.show()
            self.float_window.add_button("设置桌面", self.set_as_system_table)
            return
            
        if app_info.package_name == self.system_table_package:
            self.float_window.show()
            
            
        elif self.is_show_all:
            self.float_window.show()
        else:
            self.float_window.hide()
    
    def on_switch(self, app_info):
        if app_info.package_name == self.system_table_package:
            self.float_window.add_button("show_all", self.on_show_all_enable)
        self.enabled=False
            
    
    def on_disable(self):
        pass
    
    def on_show_all_enable(self):
        self.is_show_all = not self.is_show_all
        
    def set_as_system_table(self):
        self.system_table_package = self.cur_app_info.package_name
        Config().save("system_table_package", self.system_table_package)
        
    def on_destory(self):
        pass