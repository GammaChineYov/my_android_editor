import os
import sys

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

def make_context_support(layout_class):
	layout_stack=[]
	def __enter__(self,):
		
		#if layout_stack and not self in layout_stack[-1].children:
		#        layout_stack[-1].add_widget(self)
		layout_stack.append(self)
		self.__context_wait_add_list=[]
		print(">", self)
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		
		out = layout_stack.pop()
		print("<", out)
		for child in self.__context_wait_add_list:
			self.add_widget(child)
		del self.__context_wait_add_list
		if exc_value:
			print("exc", exc_type, exc_value, traceback)
	
	old_new = layout_class.__new__
	def wrap_new(cls, *args, **kwargs):
		instance = super(layout_class, cls).__new__(cls, *args, **kwargs)
		print("new:",instance, layout_stack)
		if layout_stack and not instance in layout_stack[-1].__context_wait_add_list:
				layout_stack[-1].__context_wait_add_list.append(instance)
		return instance
		
	layout_class.__new__ = wrap_new
	layout_class.__enter__ = __enter__
	layout_class.__exit__ = __exit__
	
	