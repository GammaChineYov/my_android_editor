from core import Component
from intent_helper import IntentHelper
from core.float_window import FloatWindow
from ascript_utils import promt,toast


class AskDoubao(Component):
    name = "豆包"
    
    def awake(self):
        doubao_appinfo = {
        "app_name": "豆包",
        "package_name": "com.larus.nova",
        "activitys": ["com.larus.home.impl.MainActivity",#对话列表
            "com.larus.bmhome.chat.ChatActivity", #豆包聊天
            "com.larus.bmhome.chat.ChatActivity" #对话框
            ]}
        self.doubao_helper = IntentHelper(doubao_appinfo)
        self.float_window = FloatWindow()
    
    def on_enable(self):
        pass
    
    def on_switch(self, app_info):
        self.float_window.add_button("问豆包", self.on_ask_button)
    
    def on_disable(self):
        pass
        
    def ask(self, question):
        doubao_helper.share_intent(question)
        
    def on_ask_button(self):
        #对话框
        toast("豆包回调")
        result = promt("请输入你的问题")
        if result:
            self.ask(result)
       
    def on_destory(self):
        pass