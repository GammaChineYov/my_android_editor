import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import WidgetBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from src.utils import redirect_output_to_kivy_log, set_default_font, make_context_support
from kivy.config import Config
from kivy.clock import Clock
make_context_support(WidgetBase)

# 设置键盘模式为停靠
Config.set('input', 'keyboard_mode', 'docked')

file_list = [
#"/storage/emulated/0/airscript/model/MyHelper/__init__.py",
'file1.txt',
 'file2.txt', 
'file3.txt']

			
class FileButton(Button):
	def __init__(self, filepath,  **kwargs):
		super(FileButton, self).__init__(**kwargs)
		self.filepath = filepath
		self.text = os.path.basename(filepath)
		self.edited_content = None
		self.source_content = None
		self.last_selection_text = ""
		self.last_selectin_from = 0
		self.last_selection_to = 0
		self.text_input = None
		self._edited_content = None
		self.last_cursor = (0,0)
	
	@property
	def edited_content(self):
		if self._edited_content is None:
			self.load_file_content()
			self._edited_content = self.source_content
		return self._edited_content
	
	@edited_content.setter
	def edited_content(self, value):
		self._edited_content = value
		self._update_button_status()
		
	def load_file_content(self):
		if os.path.exists(self.filepath):
			with open(self.filepath, 'r') as f:
				content = f.read()
				self.source_content = content
		else:
			print("找不到文件：", self.filepath)
				
	def destory(self):
		if self.parent:
			self.parent.remove_widget(btn)
			
	def _update_button_status(self):
		if self.edited_content!= self.source_content:
			self.text = "*" + os.path.basename(self.filepath)
		else:
			self.text = os.path.basename(self.filepath)
		
class EditorApp(App):
	_filepath_list = []
	
	@property
	def filepath_list(self):
		return self._filepath_list

	def build(self):
		set_default_font()
		redirect_output_to_kivy_log()
		self.active_file_btn:FileButton = None
		self.selection_text = ""
		self.selection_from = 0
		self.selection_to = 0
		self.cursor = (0,0)
		self.file_buttons = []

		with FloatLayout(size_hint=(1,1)) as root:
			with BoxLayout(orientation='vertical'):
				# 顶部文档
				with BoxLayout(size_hint_y=None, height='48dp') as tr:
					self.top_row = tr
					self.img = AsyncImage()
					
				# 文本编辑区
				self.text_input = TextInput(multiline=True)
				# 第一排按钮
				with BoxLayout(size_hint_y=None, height='48dp') as r1:
					restore_button = Button(text='恢复', on_release=self.restore_file)
					copy_button = Button(text='复制', on_release=self.copy_text)
					paste_button = Button(text='粘贴', on_release=self.paste_text)
					save_button = Button(text='保存', on_release=self.save_file)
					
				# 第二排滚动视图中的按钮布局
				with BoxLayout(size_hint_y=None, ):
					with ScrollView(do_scroll_x=True, do_scroll_y=False, scroll_type=['content'], size_hint_y=None) as scrollview:
						self.scrollview = scrollview
						with BoxLayout(size_hint_y=None, orientation="horizontal") as r2:
							self.filebutton_layout = r2
							self.update_filebutton_layout()
					add_button = Button(text="+", size_hint_x=0.1, on_release=self.add_file_button_from_dir)
				
		 
		# 监听文本编辑器的内容变化
		self.last_height = self.scrollview.height
		self.text_input.bind(text=self.on_text_changed,
		 on_touch_up=self.on_text_input_touch_up,
		 selection_text=self.on_selection_text_change,
		 cursor=self.on_text_input_cursor)
		#self.text_input.bind(focus=self.on_textinput_focus)
		#self.text_input._trigger_show_handles = self.handle_show_handles
		
		return root
		
	def on_text_input_cursor(self, handler, *args, **kwargs):
		if not self.text_input.focus:
			return
		self.cursor = self.text_input.cursor
		if self.active_file_btn:
			self.active_file_btn.last_cursor = self.text_input.cursor
		
	def add_file_button_from_dir(self, handler):
		# 从文件夹中加载文件
		self._filepath_list = file_list
		self.update_filebutton_layout()
		
	def update_filebutton_layout(self):
		# 更新文件按钮布局
		button_dict = {btn.filepath: btn for btn in self.file_buttons}
		print("添加新按钮", self.filepath_list)
		new_buttons = []
		for filepath in self.filepath_list:
			if filepath in button_dict:
				btn = button_dict.pop(filepath)
			else:
				print("添加新按钮:", filepath)
				btn = self.add_file_button(filepath)
			new_buttons.append(btn)
		self.file_buttons = new_buttons
		[btn.destory() for _,btn in button_dict] 

		
	def add_file_button(self, filepath):
		# 添加文件按钮
		print("添加文件按钮:", filepath)
		btn = FileButton(filepath=filepath, on_release=self.open_selected_file)
		self.filebutton_layout.add_widget(btn)
		return btn
							
	def on_selection_text_change(self, handler, *args,**kwargs):
		if not self.text_input.focus:
			print("失去焦点")
			handler.select_text(self.selection_from, self.selection_to)
			return
		self.selection_text = self.text_input.selection_text
		start = min(self.text_input.selection_from,self.text_input.selection_to)
		end = max(self.text_input.selection_from,self.text_input.selection_to)
		self.selection_from = start
		self.selection_to = end
		if self.active_file_btn:
			self.active_file_btn.last_selection_from = start
			self.active_file_btn.last_selection_to = end
			#self.active_file_btn.last_cursor = self.text_input.cursor
			
			
		
	def on_text_input_touch_up(self, *args,**kwargs):
		# 触摸抬起
		#print(args, kwargs)
		text_input = self.text_input
		source=self.text_input.handle_image_left
		self.cursor = self.text_input.cursor
		#if self.active_file_btn:
		#	self.active_file_btn.last_cursor = self.cursor
		self.img.source = source
		
		
	def copy_text(self, instance):
		self.text_input.select_all()
		Clipboard.copy(self.text_input.text)

	def paste_text(self, instance):
		# 实现粘贴功能
		paste_content = Clipboard.paste()
		if not paste_content:
			return
		if self.selection_text:
			self.text_input.select_text(self.selection_from,self.selection_to)
			self.text_input.paste()
		else:
			cursor = self.text_input.cursor
			self.text_input.text = paste_content
			# 更新光标位置    
			#self.cursor = text_input.get
			
		
	def open_selected_file(self, filebutton):
		# 打开选择的文件
		self.active_file_btn = filebutton
		self.text_input.text = self.active_file_btn.edited_content

		start = self.active_file_btn.last_selectin_from
		end = self.active_file_btn.last_selection_to
		cursor = self.active_file_btn.last_cursor
		self.selection_from = start
		self.selection_to = end
		self.selection_text = self.text_input.text[start:end]
		self.cursor = cursor


		self.text_input.cursor = cursor
		#if end - start>0:

		self.text_input.focus = True
		self.text_input.select_text(start, end)			

		# 设置按钮高亮
		for btn in self.file_buttons:
			btn.background_color = [0.8, 0.8, 0.8, 1]
		self.active_file_btn.background_color = [0.5, 0.5, 1, 1]

	def save_file(self, instance):
		if self.active_file_btn:
			filename = self.active_file_btn.filename
			with open(filename, 'w') as f:
				f.write(self.text_input.text)
			text = self.text_input.text
			self.active_file_btn.edited_content = text
			self.active_file_btn.source_content = text
			self.set_file_status(self.active_file_btn)

	def restore_file(self, instance):
		if self.active_file_btn:
			self.load_file_content(self.active_file_btn)
			self.active_file_btn.edited_content = self.active_file_btn.source_content
			self.text_input.text = self.active_file_btn.source_content
			self.set_file_status(self.active_file_btn)
			
	def on_text_changed(self, instance, value):
		if self.active_file_btn:
			self.active_file_btn.edited_content = value



if __name__ == '__main__':
	EditorApp().run()