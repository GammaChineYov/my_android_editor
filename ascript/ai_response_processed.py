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
    "UI开发设计模式":  "MVVM", 
}}
ai_response_json = {
"任务纪要": "根据文档要求，实现了一个应用切换监听脚本，包含监听类和监听对象基类。监听类每隔0.3秒获取一次当前运行应用信息，当检测到应用切换时，根据支持列表和使能状态调用相应监听对象的方法。监听对象基类包含支持的包名列表、是否被禁用、是否使能、是否初始化、脚本路径等字段，以及start、on_enable、on_disable、on_destory等方法，还有一个静态方法loads用于从目录中获取所有脚本中的监听对象类并实例化。",
"示例":[ {
    "文件路径": "src/listener.py",
    "文件内容": "",
    "拓展说明": "在上述代码中，ListenerBase类定义了监听对象的基本结构和方法，包括构造函数、start、on_enable、on_disable、on_destroy和loads方法。AppSwitchListener类用于监听应用切换事件，它在构造函数中接受一个监听间隔时间，在start方法中循环获取当前运行应用信息，当检测到应用切换时，调用handle_app_switch方法处理。handle_app_switch方法遍历监听对象列表，根据监听对象的使能状态和支持的包名列表，调用相应的on_enable或on_disable方法。"
}
]}