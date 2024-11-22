from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.clipboard import Clipboard
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.core.window import Window
import sys
import os
os.environ['KIVY_LOG_LEVEL'] = 'debug'

# 创建一个文件对象，用于将输出重定向到 log.txt 文件
log_file = open('../log.txt', 'w')
# 将标准输出重定向到文件
sys.stdout = log_file
# 将标准错误输出也重定向到文件
sys.stderr = log_file

class MainScreen(Screen):
	def switch_to_file_chooser(self):
		app = App.get_running_app()
		app.screen_manager.current = 'file_chooser'
		

	def copy_text(self):
		Clipboard.copy(self.ids.text_input.text)

	def paste_text(self):
		if Clipboard.paste():
			self.ids.text_input.text += Clipboard.paste()


class FileChooserScreen(Screen):
	def __init__(self, **kwargs):
		super(FileChooserScreen, self).__init__(**kwargs)
		self.file_chooser = self.children[0]

	def handle_selection_change(self, selection):
		print(9)
		print(8,len(selection), selection[0],)
		if selection and len(selection) == 1 and not os.path.isdir(selection[0]):
			app = App.get_running_app()
			app.main_screen.ids.text_input.text = selection[0]
			app.screen_manager.current = 'main'
			print(7)


class FileChooserApp(App):
	def build(self):
		LabelBase.register(name='Roboto', fn_regular='data/fonts/font_abc.ttf')
		Builder.load_file('kv/main_screen.kv')
		Builder.load_file('kv/file_chooser_screen.kv')
		self.screen_manager = ScreenManager()
		self.main_screen = MainScreen(name='main')
		self.file_chooser_screen = FileChooserScreen(name='file_chooser')
		self.screen_manager.add_widget(self.main_screen)
		self.screen_manager.add_widget(self.file_chooser_screen)

		# 在 Python 脚本中处理文件选择器的提交逻辑
		file_chooser = self.file_chooser_screen.children[0]
		print("ok")

		return self.screen_manager


if __name__ == '__main__':
	try:
		FileChooserApp().run()
	finally:
		# 在程序结束时，恢复标准输出和标准错误输出
		sys.stdout = sys.__stdout__
		sys.stderr = sys.__stderr__
		log_file.close()