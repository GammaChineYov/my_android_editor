import os
import sys
from kivy.app import App
from kivy.config import Config
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

#filepath = "/storage/emulated/0/我的文档/vivo文档/out_to_ai.txt"
filepath = "/storage/emulated/0/targets.json"

def set_default_font():
    for font_ext in ['.otf', '.ttf']:
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith(font_ext):
                    from kivy.core.text import LabelBase
                    default_font = os.path.join(root, file)
                    LabelBase.register(name='Roboto', fn_regular=default_font)
                    return default_font

    return None


def get_kivy_log_file():
    import glob
    log_path = os.path.join('.', '.kivy', 'logs', 'kivy_*.txt')
    # 获取所有匹配的日志文件列表
    log_files = glob.glob(log_path)
    if not log_files:
        print("没有找到日志文件。")
        return
    # 根据文件修改时间获取最新的日志文件
    latest_log_file = max(log_files, key=os.path.getmtime)
    return latest_log_file


def redirect_output_to_kivy_log():
    # 获取Kivy应用的日志文件路径
    log_file_path = get_kivy_log_file()
    sys.stdout = open(log_file_path, 'a')
    sys.stderr = open(log_file_path, 'a')


def share_text(text, package_name="com.larus.nova", activity_name="com.larus.home.impl.MainActivity"):
    """
    分享文本内容
    :param text: 要分享的文本内容
    """
    from jnius import autoclass
    Intent = autoclass('android.content.Intent')
    context = autoclass('org.kivy.android.PythonActivity').mActivity
    String = autoclass('java.lang.String')
    intent = Intent(Intent.ACTION_SEND)
    if package_name:
        intent.setPackage(package_name)
    if activity_name:
        intent.setClassName(package_name, activity_name)
    intent.setType("text/plain")
    intent.putExtra(Intent.EXTRA_TEXT, String(text))
    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    context.startActivity(intent)


class ShareFileApp(App):

    def build(self):
        redirect_output_to_kivy_log()
        set_default_font()
        layout = BoxLayout(orientation='vertical')
        editor_content = "这是要分享的示例文本内容，你可以根据实际情况修改。"
        text_input = TextInput()
        layout.add_widget(text_input)
        text_input.text = editor_content
        self.text_input = text_input
        # 创建分享文本按钮
        share_text_button = Button(text="分享文本", font_size=18)
        share_text_button.bind(on_release=self.share_text)
        layout.add_widget(share_text_button)
        return layout
    
    def get_edit_content(self):
        return self.text_input.text
        
    def share_text(self, instance):
        share_text(self.get_edit_content())
        

if __name__ == '__main__':
    ShareFileApp().run()