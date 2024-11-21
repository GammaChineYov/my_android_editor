import ast
import os
import enum



class Config:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def get_all_configs(self):
        all_configs = {}
        with open(self.config_file_path, "r") as file:
            config_content = file.read()
        tree = ast.parse(config_content)

        def process_node(node):
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                variable_name = node.targets[0].id
                value = self._process_value(node.value)
                all_configs[variable_name] = value
                return True
            return True

        self._traverse_tree(tree, process_node)

        return all_configs

    def get_value(self, variable_name):
        with open(self.config_file_path, "r") as file:
            config_content = file.read()
        tree = ast.parse(config_content)

        value = None

        def process_node(node):
            nonlocal value
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and node.targets[0].id == variable_name:
                print("找到", variable_name)
                value = self._process_value(node.value)
                return False
            return True

        self._traverse_tree(tree, process_node)

        if value is None:
            raise ValueError(f"变量 {variable_name} 未在配置文件中找到")

        return value

    def set_value(self, variable_name, new_value):
        with open(self.config_file_path, "r") as file:
            config_content = file.read()
        tree = ast.parse(config_content)

        def process_node(node):
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and node.targets[0].id == variable_name:
                self._set_value(node.value, new_value)
                return True
            return True

        self._traverse_tree(tree, process_node)

        modified_content = self._unparse(tree)
        with open(self.config_file_path, "w") as file:
            file.write(modified_content)

    def _traverse_tree(self, tree, process_node):
        for node in ast.walk(tree):
            if not process_node(node):
                break

    def _process_value(self, value_node):
        if isinstance(value_node, ast.Constant):
            return value_node.value
        elif isinstance(value_node, ast.List):
            return [self._process_value(item) for item in value_node.elts]
        elif isinstance(value_node, ast.Dict):
            return {self._process_value(key): self._process_value(val)
                    for key, val in zip(value_node.keys, value_node.values)}
        elif isinstance(value_node, ast.Num):
            return value_node.n
        elif isinstance(value_node, ast.Tuple):
            return tuple(self._process_value(item) for item in value_node.elts)
        elif isinstance(value_node, set):
            return set(self._process_value(item) for item in value_node)
        elif isinstance(value_node, bytes):
            return bytes(self._process_value(item) for item in value_node)
        elif isinstance(value_node, bytearray):
            return bytearray(self._process_value(item) for item in value_node)
        elif isinstance(value_node, range):
            start = self._process_value(value_node.start) if value_node.start is not None else None
            stop = self._process_value(value_node.stop) if value_node.stop is not None else None
            step = self._process_value(value_node.step) if value_node.step is not None else None
            return range(start, stop, step)
        elif isinstance(value_node, str):
            return str(self._process_value(item) for item in value_node)
        elif isinstance(value_node, enum.Enum):
            return enum.Enum(self._process_value(item) for item in value_node)
        elif isinstance(value_node, bool):
            return bool(self._process_value(item) for item in value_node)
        elif isinstance(value_node, int):
            return int(self._process_value(item) for item in value_node)
        elif isinstance(value_node, float):
            return float(self._process_value(item) for item in value_node)
        elif isinstance(value_node, complex):
            return complex(self._process_value(item) for item in value_node)
        else:
            raise ValueError(f"不支持的类型: {type(value_node)}")
            
    def _unparse(self, tree):
        return ast.unparse(tree)
        
    def _set_value(self, value_node, new_value):
        if isinstance(value_node, ast.Constant):
            value_node.value = new_value
            return value_node
        elif isinstance(value_node, ast.List):
            value_node.elts = self._to_elts(new_value)
            return value_node
        elif isinstance(value_node, ast.Dict):
            new_key_value_pairs = []
            for key, val in new_value.items():
                new_key = self._to_elts(key)
                new_val = self._to_elts(val)
                new_key_value_pairs.append((new_key, new_val))
            value_node.elts = [ast.Tuple([key, val]) for key, val in new_key_value_pairs]
            return value_node
        elif isinstance(value_node, ast.Tuple):
            value_node.elts = self._to_elts(new_value)
            return value_node
        elif isinstance(value_node, ast.Num):
            value_node.n = new_value
            return value_node
        elif isinstance(value_node, ast.Set):
            value_node.elts = self._to_elts(new_value)
            return value_node
        elif isinstance(value_node, ast.Bytes):
            value_node.value = new_value
            return value_node
        elif isinstance(value_node, ast.Bytearray):
            value_node.value = new_value
            return value_node
        elif isinstance(value_node, ast.Range):
            start = self._to_elts(new_value.start) if new_value.start is not None else None
            stop = self._to_elts(new_value.stop) if new_value.stop is not None else None
            step = self._to_elts(new_value.step) if new_value.step is not None else None
            value_node.start = start
            value_node.stop = stop
            value_node.step = step
            return value_node
        elif isinstance(value_node, ast.Str):
            value_node.value = new_value
            return value_node
        elif isinstance(value_node, ast.Attribute):
            if isinstance(new_value, enum.Enum):
                enum_value_name = new_value.name
                enum_class_name = new_value.__class__.__name__
                value_node.value = ast.Name(id=enum_class_name, ctx=ast.Load())
                value_node.attr = enum_value_name
                return value_node
            else:
                raise ValueError("不支持将非枚举值赋给Attribute类型节点")
        elif isinstance(value_node, ast.Call):
            # 假设这里调用函数的参数需要更新
            new_args = self._to_elts(new_value.args) if hasattr(new_value, 'args') else []
            new_kwargs = self._to_elts(new_value.kwargs) if hasattr(new_value, 'kwargs') else []
            value_node.args = new_args
            value_node.kwargs = new_kwargs
            return value_node
        else:
            raise BaseException("不支持类型", type(value_node), new_value)
            
    def _to_elts(self, value):
        
        if isinstance(value, list):
            return [self._to_elts(item) for item in value]
        elif isinstance(value, dict):
            return {self._to_elts(key): self._to_elts(val) for key, val in value.items()}
        elif isinstance(value, tuple):
            return (self._to_elts(item) for item in value)
        elif isinstance(value, set):
            return [self._to_elts(item) for item in value]
        elif isinstance(value, bytes):
            return ast.Bytes(value)
        elif isinstance(value, bytearray):
            return ast.Bytes(bytearray(value))
        elif isinstance(value, range):
            start = self._to_elts(value.start) if value.start is not None else None
            stop = self._to_elts(value.stop) if value.stop is not None else None
            step = self._to_elts(value.step) if value.step is not None else None
            return ast.Call(
                func=ast.Name(id='range', ctx=ast.Load()),
                args=[start, stop, step],
                keywords=[]
            )
        elif isinstance(value, str):
            return ast.Str(value)
        elif isinstance(value, enum.Enum):
            enum_value_name = value.name
            enum_class_name = value.__class__.__name__
            return ast.Attribute(
                value=ast.Name(id=enum_class_name, ctx=ast.Load()),
                attr=enum_value_name,
                ctx=ast.Load()
            )
        elif isinstance(value, int):
            return ast.Constant(value)
        elif isinstance(value, float):
            return ast.Constant(value)
        elif isinstance(value, complex):
            return ast.Constant(value)
        elif isinstance(value, bool):
            return ast.Constant(value)
        else:
            raise ValueError(f"不支持的类型: {type(value)}")


# 使用示例
config_file_path = "config.py"
config = Config(config_file_path)

# 获取所有配置
all_configs = config.get_all_configs()
print("所有配置:", all_configs)

# 获取特定变量的值
list_value = config.get_value("LIST_SETTING")
print("LIST_SETTING的值:", list_value)

# 设置特定变量的值
try:
    config.set_value("LIST_SETTING", ["value", 6.9, True, 8, b"2", 'a'])
except:
    import traceback
    traceback.print_exc()

# 再次获取所有配置，查看设置后的值是否更新
updated_all_configs = config.get_all_configs()
print("更新后的所有配置:", updated_all_configs)