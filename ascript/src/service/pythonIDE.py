from ascript.android.node import Selector

{
    "app_name": "Python编译器IDE",
    "package_name": "com.cscjapp.python",
    "activity": "com.cscjapp.python/.MainActivity"
}
[{
    "app_name": "Python编译器IDE",
    "app_size": 336677843,
    "is_sd": True,
    "is_system": False,
    "package_name": "com.cscjapp.python",
    "apk_path": "/data/app/~~hALC0WBVXAEAIwYKle7Iiw==/com.cscjapp.python-KPsQI7p1h5RmAkyLm4yl6w==/base.apk"
}]

def get_file_name(selector):
    file_name_node = selector.id("com.cscjapp.python:id/fileName").find()
    if file_name_node:
        return file_name_node.text
    return None


def get_file_directory_path(selector):
    project_path_node = selector.id("com.cscjapp.python:id/project").find()
    if project_path_node:
        return project_path_node.text.split("：")[1]
    return None


def get_editor_content(selector):
    editor_node = selector.id("com.cscjapp.python:id/editorLayout").find()
    if editor_node:
        return editor_node.text
    return None
    
    
# 创建一个Selector实例
selector = Selector()

# 获取文件名
file_name = get_file_name(selector)
if file_name:
    print("文件名:", file_name)
else:
    print("未找到文件名控件或无法获取文件名")

# 获取文件目录路径
file_directory_path = get_file_directory_path(selector)
if file_directory_path:
    print("文件目录路径:", file_directory_path)
else:
    print("未找到文件目录路径控件或无法获取文件目录路径")

# 获取代码编辑区内容
editor_content = get_editor_content(selector)
if editor_content:
    print("代码编辑区内容:")
    print(editor_content)
else:
    print("未找到代码编辑区控件或无法获取内容")