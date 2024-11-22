from. import Component
from utils import SingletonMeta
from ascript.android.system import R
from ascript.android.ui import WebWindow
from ascript_utils import toast
import traceback
import json
import time
from ascript.android.system import KeyValue
from utils.timer import FlushTimer


class FloatWindow(Component, metaclass=SingletonMeta):
    name = "悬浮窗"
    button_callbacks = []

    def awake(self, show=True):
        # 初始化函数加载html，配置监听
        self.html_path = R.ui('button_window.html')
        self._window = None  # 先初始化为None，之后通过装饰器属性来处理获取逻辑
        self.last_app = None
        self.timer = FlushTimer(1, self.auto_window_height)
        
    def _init_window(self):
        self.window.tunner(self.on_callback)

        # 设置窗口宽度为屏幕宽度的1/5，高度为屏幕高度的1/2
        # self.window.size('20vw', '50vh')
        # 设置窗口背景色为白色
        self.window.background("#80FFFFFF")
        # 设置窗口可拖动
        # self.window.drag(True)
        # 设置窗口引力位置在右边
        self.window.gravity(3 | 48)
        # 设置窗口模式为窗口内和外都可获取点击触摸事件，且可在窗口内调出键盘
        self.window.mode(3)
        # 设置窗口遮罩层透明度为0（完全透明）
        self.window.dim_amount(0)
        # 假设在HTML页面中有一个名为'fun1'的JavaScript函数
        # web_window.call('fun1("自在老师", 2)')
        self.cur_size = ('30vw', '50vh')
        self.window.size(*self.cur_size)

    def auto_window_height(self):
        #禁用，暂时无法解决
        height = KeyValue.get("buttonBoxHeight", "")
        if self._window is not None and height and False:            
            self.cur_size = self.cur_size[0], str(int(height)//7 + 10) + 'vh'
            toast("自动宽高", self.cur_size)
            self._window.size(*self.cur_size)
            
            KeyValue.save("buttonBoxHeight", "")
            
    @property
    def window(self):
        if self._window is None:
            self._window = WebWindow(self.html_path)
            self._init_window()
        return self._window

    @window.setter
    def window(self, value):
        self._window = value

    def _set_size(self, width, height):
        """设置窗口宽度为屏幕宽度的1/5，高度为屏幕高度的1/2
        self.window.size('20vw', '50vh') 
        """
        self.window.size(width, height)

    def _set_gravity(self, value):
        # 设置窗口引力位置
        self.window.gravity(value)

    def _set_position(self, x, y):
        pass

    def show(self):
        # 显示窗口
        self.window.show()
        time.sleep(0.5)

    def hide(self):
        self.window.close()
        self.window = None

    def _set_gravity(self, gravity_value, offset_x=0, offset_y=0):
        """
        设置WebWindow的重力方向和偏移量。

        参数:
        web_window (WebWindow): 要设置的WebWindow对象。
        gravity_value (int): 重力方向的值，应使用android.view.Gravity中的常量值或其组合。
        offset_x (int, 可选): x轴方向的偏移量，默认为0。
        offset_y (int, 可选): y轴方向的偏移量，默认为0。

        返回:
        无

        示例:
        # 创建WebWindow实例
        web_window = WebWindow(...)
        # 设置窗口布局至左上角，偏移x轴100像素，y轴200像素
        set_webwindow_gravity(web_window, 3 | 48, 100, 200)
        # 设置窗口布局至屏幕居中
        set_webwindow_gravity(web_window, 17)
        """
        self.window.gravity(gravity_value, offset_x, offset_y)

    def on_enable(self):
        pass

    def on_switch(self, app_info):
        pass

    def on_callback(self, key, value):
        # 监听函数，调用对应index的回调

        if value.isdigit():
            index = int(value)

            if 0 <= index < len(self.button_callbacks):
                # toast(key,value)
                try:
                    self.button_callbacks[index]()
                except BaseException as e:
                    toast("悬浮窗回调出错", key,value, traceback.format_exc())

    def add_button(self, button_name, callback, icon_path="", height=None):
        if self.cur_app_info != self.last_app:
            self.last_app = self.cur_app_info
            self.clearButtonList()
        self.timer.start()
        #toast("添加按钮:", button_name)
        # 添加按钮到HTML页面，并注册回调函数
        button_data = {
            "name": button_name
        }
        self.button_callbacks.append(callback)
        # 使用call方法向HTML传递按钮数据和回调函数索引
        data = json.dumps(button_data, ensure_ascii=False)

        res = self.window.call(f"generateButton('{data}')")

    def clearButtonList(self):
        # toast("清除按钮")
        self.button_callbacks.clear()
        # 清除HTML页面上的按钮列表
        self.window.call("clearButtonList()")