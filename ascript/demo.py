from ascript.android.ui import FloatWindow, ImageWindow, Dialog
from ascript.android.action import Ime
from ascript.android.system import Device
from ascript.android import screen
#导包
from android.content import Intent 
from ascript.android.system import R
import time

# 假设的页面信息视图控制类
class PageInfoViewController:
    def __init__(self):
        self.page_info_list = []  # 页面信息列表
        self.add_page_mode = False  # 添加页面模式标志
        self.init_float_window()

    def init_float_window(self):
        # 创建悬浮窗有
        self.float_window = FloatWindow()
        # 添加激活按钮
        self.float_window.add_menu("my_activate", R.ui("my_icon.png"), self.activate_button_click)
        # 显示悬浮窗
        self.float_window.show(x=0.1,y=0.1)

    def activate_button_click(self):
        self.add_page_mode = True
        print("激活添加页面模式")

    def add_page_object(self, page_object):
        self.page_info_list.append(page_object)
        # 创建跳转按钮并添加到悬浮窗
        self.float_window.add_menu(page_object.page_name, "icon_path", lambda: self.jump_to_page(page_object))

    def jump_to_page(self, page_object):
        page_object.jump_to_app_page()

# 假设的应用页面信息类
class AppPageInfo:
    def __init__(self, page_name, app_name, app_package_name, page_route, snapshot_path):
        self.page_name = page_name
        self.app_name = app_name
        self.app_package_name = app_package_name
        self.page_route = page_route
        self.snapshot_path = snapshot_path

    @staticmethod
    def get_current_page_info():
        # 获取当前设备运行的APP信息
        app_info = Device.current_appinfo()
        return AppPageInfo("当前页面", app_info.name, app_info.packageName, "", "")

    def take_page_snapshot(self):
        print(f"拍摄页面快照并保存到: {self.snapshot_path}")
        # 进行截图操作
        screenshot = screen.capture()
        ImageWindow.show(screenshot)
        # 这里可以添加保存截图到指定路径的逻辑，例如使用文件读写操作（参考`api/file.md`中的方法）将截图保存到self.snapshot_path

    def jump_to_app_page(self):
        print(f"跳转到应用页面: {self.app_name}, 包名: {self.app_package_name}, 路由: {self.page_route}")
        # 使用意图（intent）跳转到应用页面
        intent = Intent()
        intent.setComponent(Intent.ComponentName(self.app_package_name, self.page_route))
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        R.intent.startActivity()


# 主函数或测试代码
Dialog.toast("开始运行demo")
page_controller = PageInfoViewController()
#current_page_info = AppPageInfo.get_current_page_info()
#page_controller.add_page_object(current_page_info)

while True:
    if page_controller.add_page_mode:
        if detect_volume_decrease():
            new_page_info = AppPageInfo.get_current_page_info()
            page_controller.add_page_object(new_page_info)
            page_controller.jump_to_page(new_page_info)
    time.sleep(0.1)