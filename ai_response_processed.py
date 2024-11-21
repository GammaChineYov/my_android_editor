ai_promt_tip = { 
"python":{
    "需要参数类型提示": True,
    "需要返回类型提示": True,
    "需要函数注释": True,
    "需要函数参数注释": False,
    "需要函数返回类型注释": True,
    "需要字段注释": True,
    "公开属性设计方法": "使用属性装饰器",
    "需要超百行模块拆分建议": True,
    "UI开发设计模式":  "MVVM"
}}
ai_response_json = {
"任务纪要": "实现example_textinput_cursor.py，用于展示TextInputCursor类的使用示例，创建一个文本输入框并绑定相关事件处理，以便用户可以进行交互操作，验证TextInputCursor类的功能。",
"示例":[ {
    "文件路径": "src/text_input_cursor/example/example_textinput_cursor.py",
    "文件内容": "",
    "拓展说明": "example_textinput_cursor.py创建了一个Kivy应用，在应用中创建了一个文本输入框，并将其与TextInputCursor类实例绑定，从而实现了文本输入框的交互功能，包括双击选单词、游标位置变化处理和滑动操作处理等。运行该应用后，用户可以在文本输入框中进行相应操作来验证功能。"
}]