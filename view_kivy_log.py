import os
import glob

def get_kivy_log_file():
	log_path = os.path.join('.', '.kivy', 'logs', 'kivy_*.txt')
	# 获取所有匹配的日志文件列表
	log_files = glob.glob(log_path)
	if not log_files:
		print("没有找到日志文件。")
		return
	# 根据文件修改时间获取最新的日志文件
	latest_log_file = max(log_files, key=os.path.getmtime)
	return latest_log_file
def print_latest_log():
	# 构建日志文件路径模式
	latest_log_file = get_kivy_log_file()
	with open(latest_log_file, 'r') as file:
		print(file.read())

if __name__ == "__main__":
	print_latest_log()