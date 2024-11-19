from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
import os


# 双列文件选择器视图类
class DualFileChooserViews(BoxLayout):
    left_fciv = ObjectProperty()
    right_fciv = ObjectProperty()

    def __init__(self, **kwargs):
        super(DualFileChooserViews, self).__init__(**kwargs)
        self.left_fciv = FileChooserIconView()
        self.right_fciv = FileChooserIconView()
        self.add_widget(self.left_fciv)
        self.add_widget(self.right_fciv)


# 文件选择器路径更新类
class FileChooserPathUpdater:
    def __init__(self, left_fciv, right_fciv):
        self.left_fciv = left_fciv
        self.right_fciv = right_fciv
        self.left_fciv.bind(path=self.update_right_path)
        self.right_fciv.bind(path=self.update_left_path)

    def update_right_path(self, instance, value):
        self.right_fciv.path = value

    def update_left_path(self, instance, value):
        self.left_fciv.path = value
        self.right_fciv.path = value


# 导航按钮功能类
class NavigationButtonFunctions:
    def __init__(self, left_fciv, right_fciv):
        self.left_fciv = left_fciv
        self.right_fciv = right_fciv
        self.left_nav_up_btn = Button(text="Up")
        self.right_nav_up_btn = Button(text="Up")
        self.left_nav_up_btn.bind(on_release=self.navigate_left_up)
        self.right_nav_up_btn.bind(on_release=self.navigate_right_up)

    def navigate_left_up(self, *args):
        current_path = self.left_fciv.path
        new_path = os.path.dirname(current_path)
        self.left_fciv.path = new_path
        self.right_fciv.path = new_path

    def navigate_right_up(self, *args):
        current_path = self.right_fciv.path
        new_path = os.path.dirname(current_path)
        self.left_fciv.path = new_path
        self.right_fciv.path = new_path


# 按钮功能类
class ButtonFunctions:
    def __init__(self, left_fciv, right_fciv, cancel_btn, select_btn, done_btn,
                 disable_cancel=False, disable_select=False, disable_done=False,
                 previous_selected_paths=[]):
        self.left_fciv = left_fciv
        self.right_fciv = right_fciv
        self.cancel_btn = cancel_btn
        self.select_btn = select_btn
        self.done_btn = done_btn
        self.disable_cancel = disable_cancel
        self.disable_select = disable_select
        self.disable_done = disable_done
        self.previous_selected_paths = previous_selected_paths

        self.cancel_btn.bind(on_release=self.cancel_selection)
        self.select_btn.bind(on_release=self.make_selection)
        self.done_btn.bind(on_release=self.complete_selection)

        # 初始化时设置上次选择的路径为高亮
        for path in self.previous_selected_paths:
            self.highlight_path(path)

    def cancel_selection(self, *args):
        if not self.disable_cancel:
            app = App.get_running_app()
            screen_manager = app.root
            if len(screen_manager.screens) > 1:
                previous_screen = screen_manager.screens[-2]
                screen_manager.current = previous_screen.name

    def make_selection(self, *args):
        if not self.disagelect:
            self.select_btn.background_color = (0, 1, 0, 1) if self.select_btn.background_color == (1, 0, 0, 1) else (1, 0, 0, 1)
            selected_path = self.left_fciv.selection or self.right_fciv.selection
            if selected_path:
                self.highlight_path(selected_path[0])

    def complete_selection(self, *args):
        if not self.disable_done:
            app = App.get_running_app()
            screen_manager = app.root
            if len(screen_manager.screens) > 1:
                previous_screen = screen_manager.screens[-2]
                screen_manager.current = previous_screen.name

            self.previous_selected_paths = [self.left_fciv.selection or self.right_fciv.selection][0] if self.left_fciv.selection or self.right_fciv.selection else []

    def highlight_path(self, path):
        for fciv in [self.left_fciv, self.right_fciv]:
            if path in fciv.files:
                fciv.selected_path = path
                fciv.refresh()


# 双列文件选择器类，组合各个功能类
class DualFileChooser(BoxLayout):
    def __init__(self, root_path, **kwargs):
        super(DualFileChooser, self).__init__(**kwargs)

        self.root_path = root_path
        self.views = DualFileChooserViews()
        self.path_updater = FileChooserPathUpdater(self.views.left_fciv, self.views.right_fciv)
        self.nav_buttons = NavigationButtonFunctions(self.views.left_fciv, self.views.right_fciv)
        self.buttons = ButtonFunctions(self.views.left_fciv, self.views.right_fciv,
                                       self.nav_buttons.left_nav_up_btn, self.nav_buttons.right_nav_up_btn,
                                       Button(text="取消"), Button(text="选择"), Button(text="完成"))

        self.views.left_fciv.path = root_path
        self.views.right_fciv.path = root_path

        self.add_widget(self.views)
        self.add_widget(self.nav_buttons.left_nav_up_btn)
        self.add_widget(self.nav_buttons.right_nav_up_btn)
        self.add_widget(self.buttons.cancel_btn)
        self.add_widget(self.buttons.select_btn)
        self.add_widget(self.buttons.done_btn)

        self.selections = []
        self.last_root = root_path

    def select(self, just_file=True, suffix=[]):
        selected_path = self.views.left_fciv.selection or self.views.right_fciv.selection
        if selected_path:
            file_path = selected_path[0]
            file_name, file_ext = os.path.splitext(file_path)
            if (not just_file or os.path.isfile(file_path)) and (not suffix or file_ext in suffix):
                self.selections.append(file_path)
                self.last_root = os.path.dirname(file_path)
                return True
        return False

    def select_many(self, paths_to_select, just_file=False, suffix=[]):
        selected_paths = []
        for path in paths_to_select:
            file_name, file_ext = os.path.splitext(path)
            if (not just_file or os.path.isfile(path)) and (not suffix or file_ext in suffix):
                selected_paths.append(path)

        if selected_paths:
            self.selections.extend(selected_paths)
            self.last_root = os.path.dirname(paths_to_select[-1])
            return True
        return False


# 主屏幕类
class FileChooserScreen(Screen):
    def __init__(self, **kwargs):
        super(FileChooserScreen, self).__init__(**kwargs)
        self.dual_file_chooser = DualFileChooser(root_path="./src[]")
        self.add_widget(self.dual_file_chooser)


# 构建应用的KV语言字符串
kv_string = """
#:import Factory kivy.factory.Factory

<FileChooserScreen>:
    name: 'file_chooser_screen'
    dual_file_chooser: dual_file_chooser

<DualFileChooser>:
    orientation: 'vertical'
    views: views
    path_updater: path_updater
    nav_buttons: nav_buttons
    buttons: buttons

    BoxLayout:
        orientation: 'horizontal'
        Button:
            text: "取消"
            on_release: buttons.cancel_btn.dispatch('on_release') if not buttons.disable_cancel else None
        Button:
            text: "选择"
            on_release: buttons.select_btn.dispatch('on_release') if not buttons.disable_select else None
        Button:
            text: "完成"
            on_release: buttons.done_btn.dispatch('on_release') if not buttons.disable_done else None

    FileChooserIconView:
        id: views.left_fciv
    FileChooserIconView:
        id: views.right_fciv
    Button:
        text: "Up"
        on_release: nav_buttons.left_nav_up_btn.dispatch('on_release')
    Button:
        text: "Up"
        on_release: nav_buttons.right_nav_up_btn.dispatch('on_release')
"""


# 定义应用类
class MyApp(App):
    def build(self):
        screen_manager = ScreenManager()
        file_chooser_screen = FileChooserScreen()
        screen_manager.add_widget(file_chooser_screen)

        Builder.load_string(kv_string)

        return screen_manager


if __name__ == '__main__':
    MyApp().run()