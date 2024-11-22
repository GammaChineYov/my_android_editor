import inspect

MAX_DEPTH = 5  # 设置最大递归深度
analyzed_modules = set()

def is_custom_module(obj):
    # 判断对象是否为自定义模块而不是内置模块
    try:
        return inspect.ismodule(obj)  and not obj.__name__ in __builtins__.__dict__
    except:
        return True

def analyze_module(module, depth=0):
    result = []  # 用于存储打印的内容
    if depth > MAX_DEPTH:
        return result
    if module in analyzed_modules:
        return result
    analyzed_modules.add(module)
    try:
        result.append(f"分析模块: {module.__name__}")
        module_vars = dict(vars(module))
        for name, obj in module_vars.items():
            if inspect.isclass(obj):
                try:
                    result.append(f"  类: {name}")
                    class_docstring = inspect.getdoc(obj)
                    if class_docstring:
                        result.append(f"    注释: {class_docstring}")
                    for attr_name, attr_value in vars(obj).items():
                        if not inspect.isroutine(attr_value) and not attr_name.startswith('__'):
                            attr_type = type(attr_value).__name__
                            result.append(f"    属性: {attr_name}: {attr_type}")
                    for method_name, method_obj in inspect.getmembers(obj):
                        if inspect.isfunction(method_obj):
                            argspec = inspect.getfullargspec(method_obj)
                            args_with_types = []
                            for arg in argspec.args:
                                arg_type = ""
                                if argspec.annotations and arg in argspec.annotations:
                                    arg_type = argspec.annotations[arg].__name__
                                args_with_types.append(f"{arg}: {arg_type}")
                            return_type = ""
                            if argspec.annotations and 'return' in argspec.annotations:
                                return_type = argspec.annotations['return'].__name__
                            method_docstring = inspect.getdoc(method_obj)
                            result.append(f"    函数: {method_name}({', '.join(args_with_types)}) -> {return_type}")
                            if method_docstring:
                                result.append(f"      注释: {method_docstring}")
                except Exception as e:
                    result.append(f"    分析类 {name} 时出错: {e}")
            elif inspect.isfunction(obj):
                try:
                    argspec = inspect.getfullargspec(obj)
                    args_with_types = []
                    for arg in argspec.args:
                        arg_type = ""
                        if argspec.annotations and arg in argspec.annotations:
                            arg_type = argspec.annotations[arg].__name__
                        args_with_types.append(f"{arg}: {arg_type}")
                    return_type = ""
                    if argspec.annotations and 'return' in argspec.annotations:
                        return_type = argspec.annotations['return'].__name__
                    function_docstring = inspect.getdoc(obj)
                    result.append(f"  函数: {name}({', '.join(args_with_types)}) -> {return_type}")
                    if function_docstring:
                        result.append(f"    注释: {function_docstring}")
                except Exception as e:
                    result.append(f"    分析函数 {name} 时出错: {e}")
            elif is_custom_module(obj):
                try:
                    result.extend(analyze_module(obj, depth + 1))
                except Exception as e:
                    result.append(f"    分析子模块 {name} 时出错: {e}")
    except Exception as e:
        
        result.append(f"分析模块 {module.__name__} 时出错: {e}")
    #return result
    return result  # 返回打印的内容

#import plyer
#print("\n".join(analyze_module(plyer)))