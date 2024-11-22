from ascript.android.ui import WebWindow, Dialog
from ascript.android.system import R,Clipboard

class ButtonWindow:
    class ButtonViewItem:
        def __init__(self, rect)
    def __init__(self, show=True):
        # 创建Web窗口
        self.window = WebWindow(R.ui('button_window.html'), self.button_click_callback)
        # 设置窗口宽度为屏幕宽度的1/5，高度为屏幕高度的1/2
        self.window.size('20vw', '50vh')
        # 设置窗口背景色为白色
        self.window.background("#FFFFFF")
        # 设置窗口可拖动
        self.window.drag(True)
        # 设置窗口引力位置在右边
        self.window.gravity(5|16)
        # 设置窗口模式为窗口内和外都可获取点击触摸事件，且可在窗口内调出键盘，同时禁止窗口缩放
        self.window.mode(3)
        # 设置窗口遮罩层透明度为0（完全透明）
        self.window.dim_amount(0)
        
        if show:
            self.show()
        
        
    def show(self):
        # 显示窗口
        self.window.show()

    def button_click_callback(self, k, v):
        if k == "test_button_click":
            # 点击按钮后弹出吐司提示
            Dialog.toast('点击了测试按钮')