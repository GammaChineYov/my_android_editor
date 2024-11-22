import sys
import os
import ast

# 重定向输出的装饰器
def redirect_output(output_path='log.txt'):
    def inner_decorator(func):
        def wrapper(*args, print_no_class_or_function=False, print_comments=True, **kwargs):
            original_stdout = sys.stdout
            log_file = open(output_path, 'w')
            sys.stdout = log_file
            try:
                func(*args, print_no_class_or_function=print_no_class_or_function, print_comments=print_comments, **kwargs)
            except Exception as e:
                print(f"程序运行过程中出现错误: {e}", file=log_file)
            finally:
                log_file.close()
                sys.stdout = original_stdout
        return wrapper
    return inner_decorator

# 打印注释的函数
def print_comment(comment, indent):
    """ 打印注释，换行后增加缩进，并前后加上 ``` """
    lines = comment.split('\n')
    print(f"{indent}```")
    for line in lines:
        print(f"{indent}{line}")
    print(f"{indent}```")

def get_directory_info(plyer, default_path='platforms/android'):
    """ 获取指定的目录信息 """
    return os.path.join(os.path.dirname(plyer.__file__), default_path)

def print_class_info(node, indent):
    """ 打印类的相关信息 """
    class_name = node.name
    if class_name not in printed_classes:
        printed_classes.add(class_name)
        class_docstring = ast.get_docstring(node)
        print(f"{indent}类 {class_name}:")
        if class_docstring:
            print_comment(class_docstring, indent + "  ")
            pass
        for base in node.bases:
            print(f"{indent}  基类: {ast.dump(base)}")
        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                print_function_info(stmt, indent + "  ")

def print_function_info(node, indent):
    """ 打印函数的相关信息 """
    function_name = node.name
    if function_name not in printed_functions:
        printed_functions.add(function_name)
        function_docstring = ast.get_docstring(node)
        args_with_types = []
        for arg in node.args.args:
            arg_type = ""
            if arg.annotation:
                arg_type = ast.dump(arg.annotation)
            args_with_types.append(f"{arg.arg}: {arg_type}")
        func_info = f"{function_name}({', '.join(args_with_types)})"
        print(f"{indent}函数 {func_info}")
        if function_docstring:
            print_comment(function_docstring, indent + "  ")
            pass

def analyze_python_file(file_path, indent, print_no_class_or_function=False, print_comments=True):
    """ 分析 Python 文件的函数 """
    global printed_classes, printed_functions  # 声明使用全局变量
    printed_classes = set()  # 重置类的过滤集合
    printed_functions = set()  # 重置函数的过滤集合
    print(f"{indent}  分析文件: {os.path.basename(file_path)}")
    with open(file_path, 'r') as source_file:
        source_code = source_file.read()
        tree = ast.parse(source_code)
        has_class_or_function = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) or isinstance(node, ast.FunctionDef):
                has_class_or_function = True
                if isinstance(node, ast.ClassDef):
                    print_class_info(node, indent + "  ")
                elif isinstance(node, ast.FunctionDef):
                    print_function_info(node, indent + "  ")
        if not has_class_or_function and print_no_class_or_function:
            print(f"{indent}  没有类或函数的代码:")
            print_comment(source_code, indent + "  ")
        

@redirect_output()  # 调用重定向装饰器，使用默认路径
def print_python_file_structure(directory, print_no_class_or_function=False, print_comments=True):
    print(f"分析目录: {directory}")
    def traverse_directory(directory, indent_level=0, print_no_class_or_function=print_no_class_or_function, print_comments=print_comments):
        indent = "  " * indent_level  # 减少缩进空格为 2 个
        dir_name = os.path.basename(directory)
        if os.path.isdir(directory) and not (dir_name.startswith('.') or dir_name == '__pycache__'):  # 忽略隐藏文件夹和 "__pycache__" 文件夹
            print(f"{indent}{dir_name}/")
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path) and not (item.startswith('.') or item == '__pycache__'):  # 忽略隐藏文件夹和 "__pycache__" 文件夹
                    traverse_directory(item_path, indent_level + 1, print_no_class_or_function, print_comments)
                elif item.endswith('.py') and not item.endswith('.pyc'):
                    analyze_python_file(item_path, indent , print_no_class_or_function, print_comments)
        else:  # 被忽略的文件夹直接跳过
            return

    traverse_directory(directory, print_no_class_or_function=print_no_class_or_function, print_comments=print_comments)

if __name__ == "__main__":
    try:
        import kivy
    except ImportError as e:
        print(f"导入 kivy 或其相关模块时出错: {e}")
    directory = get_directory_info(kivy, "")
    print_python_file_structure(directory, print_comments=False)  # 使用默认参数，即不输出没有类或函数的代码，输出注释