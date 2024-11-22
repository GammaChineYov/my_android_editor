import os
import importlib
import json
from.component import Component
from .app_switch_manager import AppSwitchManager
from utils import singleton
from ascript.android.system import R
from ascript_utils import toast
import importlib.util
import sys

config_dict = {}


def import_module_from_path(module_path, module_name):
    """
    通过指定的文件路径和模块名导入模块

    :param module_path: 模块文件的绝对路径
    :param module_name: 要导入的模块名
    :return: 导入的模块对象
    """
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    my_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = my_module
    spec.loader.exec_module(my_module)
    return my_module
    
    
def import_and_process_module(module_path):
    try:
        if module_path.endswith(".py"):
            module = import_module_from_path(module_path,os.path.basename(module_path)[:-3])
        else:
            
            module = importlib.import_module(module_path, ".")
            
        result = []
        for name, obj in vars(module).items():
            if isinstance(obj, type) and issubclass(obj, Component) and hasattr(obj, 'name') and Component != obj:
                class_name = f"{obj.__name__}:{obj.name}"
                if (class_name not in config_dict) or (config_dict[class_name]['is_active']):
                    if (class_name not in config_dict):
                        config_dict[class_name] = {"is_active": True,
                                                   "module_path": module_path,
                                                   "class_name": class_name,
                                                   "name": obj.name}
                    instance = obj()
                    
                    result.append(instance)
        return result
    except BaseException as e:
        toast(f"导入模块 {module_path} 失败: {e}")
        return []


def import_and_create_objects_list(module_paths):
    object_list = []
    for path in module_paths:
        object_list.extend(import_and_process_module(path))
    return object_list


def import_and_create_objects(directory):
    object_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                module_name = file[:-3]
                module_path = os.path.join(root,file)
                object_list.extend(import_and_process_module(module_path))
    return object_list


@singleton
class ComponentManager:
    def __init__(self):
        toast("开始加载模块")
        self.module_paths = ["core.float_window"]
        self.module_dir_path = R.root("components")
        self.config_path = R.root("config/component_config.json")
        self.load_config()
        for key,value in config_dict.items():
            config_dict[key]["is_active"] = True
        self.component_list = import_and_create_objects_list(self.module_paths)
        self.component_list.extend(import_and_create_objects(self.module_dir_path))
        self.save_config()
        asm = AppSwitchManager()
        self.component_list = list(set(self.component_list))
        for component in self.component_list:
            toast("加载组件:", component.name)
            asm.add_listener(component)
        asm.start()

    def load_config(self):
        global config_dict
        if not os.path.exists(self.config_path):
            return  # 如果配置文件不存在，直接返回，后续可根据需要添加创建默认配置文件的逻辑

        with open(self.config_path, 'r') as f:
            try:
                config_dict = json.load(f)
            except json.JSONDecodeError as e:
                print(f"加载配置文件失败: {e}")

    def save_config(self):
        dir = os.path.dirname(self.config_path)
        if dir:
            os.makedirs(dir, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config_dict, f, indent=4)
            
component_manager = ComponentManager()