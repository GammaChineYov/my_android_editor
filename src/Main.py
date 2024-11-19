from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ToggleButtonBehavior
import os


# 定义自定义的 RadioButton 类
class MyRadioButton(ToggleButtonBehavior, BoxLayout):
	text_value = StringProperty()

	def __init__(self, **kwargs):
		super(MyRadioButton, self).__init__(**kwargs)
		self.orientation = 'horizontal'
		self.button = Button(text='Radio Option')
		self.add_widget(self.button)
		self.bind(state=self.update_style)
		self.button.bind(on_release=self.on_button_release)

	def update_style(self, instance, value):
		if value == 'down':
			self.background_color = [0.5, 0.5, 1, 1]  # 选中时的颜色
		else:
			self.background_color = [0.8, 0.8, 0.8, 1]  # 未选中时的颜色

	def on_button_release(self, instance):
		main_screen = App.get_running_app().root.get_screen('main')
		main_screen.select_function(self.text_value)


# 注册自定义的 RadioButton 类
Factory.register('MyRadioButton', cls=MyRadioButton)


# 定义HeaderLayout类
class HeaderLayout(BoxLayout):
	pass


# 注册HeaderLayout类到Factory
Factory.register('HeaderLayout', cls=HeaderLayout)


class MainScreen(Screen):
	scene_name = StringProperty("默认场景")

	def show_settings(self):
		self.manager.current ='settings'

	def select_function(self, function_name):
		self.ids.text_edit.text = f"当前选中功能: {function_name}"


class SettingsScreen(Screen):
	def hide_settings(self):
		self.manager.current ='main'

	def set_font_size(self, size):
		print(f"设置字体大小为: {size}")

	def toggle_some_setting(self, is_active):
		print(f"设置开关状态为: {is_active}")

	def set_text_color(self, color):
		main_screen = self.manager.get_screen('main')
		main_screen.ids.text_edit.color = color


class MyScreenManager(ScreenManager):
	pass


def get_default_font():
	for font_ext in ['.otf', '.ttf']:
		for root, dirs, files in os.walk('.'):
			for file in files:
				if file.endswith(font_ext):
					return os.path.join(root, file)
	return None


class MyApp(App):
	def build(self):
		default_font = get_default_font()
		if default_font:
			from kivy.core.text import LabelBase
			LabelBase.register(name='Roboto', fn_regular=default_font)

		Builder.load_file('main.kv')
		Builder.load_file('settings.kv')

		sm = MyScreenManager()
		sm.add_widget(MainScreen(name='main'))
		sm.add_widget(SettingsScreen(name='settings'))
		return sm


if __name__ == '__main__':
	MyApp().run()