import requests
import os
import shutil
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.clipboard import Clipboard
from kivy.core.text import LabelBase


def find_file_in_phone_storage(file_name):
    # 假设手机存储的根目录为 '/storage'
    root_directory = "/storage/emulated/0"
    for root, dirs, files in os.walk(root_directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return None
    
class ClipboardApp(App):
    def build(self):
        
        #path = find_file_in_phone_storage("font_abc.ttf")
        #shutil.copy(path, "font_abc.ttf")
        LabelBase.register(name='Roboto', fn_regular='font_abc.ttf')

        layout = BoxLayout(orientation='vertical')

        self.text_input = TextInput()
        self.text_input.multiline = True

        copy_button = Button(text='复制到剪切板')
        copy_button.bind(on_press=self.copy_to_clipboard)

        paste_button = Button(text='从剪切板粘贴')
        paste_button.bind(on_press=self.paste_from_clipboard)

        # 添加文件选择按钮和文件选择视图
        file_chooser_button = Button(text='选择文件')
        file_chooser_button.bind(on_press=self.open_file_chooser)

        self.file_chooser = FileChooserIconView()

        layout.add_widget(self.text_input)
        layout.add_widget(copy_button)
        layout.add_widget(paste_button)
        layout.add_widget(file_chooser_button)
        layout.add_widget(self.file_chooser)

        return layout

    def copy_to_clipboard(self, instance):
        Clipboard.copy(self.text_input.text)

    def paste_from_clipboard(self, instance):
        content = Clipboard.paste()
        self.text_input.text = content

    def open_file_chooser(self, instance):
        self.file_chooser
        from utils.analytic_plyer_dynamic import analyze_module
        res =analyze_module(FileChooserIconView)
        self.text_input.text = "\n".join(res)

if __name__ == '__main__':
    ClipboardApp().run()