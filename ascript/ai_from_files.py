import os
import shutil
import ast
import re
import traceback

prompt = r"""
编写一个监听脚本（子线程）：监听类：每隔priod=0.3秒调用一次DeviceRunningInfo.get_running_app_info()，当检测到用户切换app时，调用函数1（遍历所以监听对象列表，根据包名支持列表/是否已使能/是否被禁用决定是否调用监听对象.on_enable()，在调用前如果没有初始化，先调用监听对象.start()），再调用函数2（遍历使能的监听对象列表，对不支持新应用的监听对象调用对象.on_disable()）
监听对象基类：字段：支持的包名列表，是否被禁用，是否使能，是否初始化，脚本路径；函数：start，on_enable，on_disable, on_destory,loads(静态函数，从目录中获取所有脚本中的监听对象类并示例化)
"""
filepaths = [
"src/"
]

is_write_prompt_in_file = True
ai_response_format_file = "ai回答模板.md"
out_prompt = f"按照文档需求实现内容,按照'{ai_response_format_file}'文件回复"

if is_write_prompt_in_file and ai_response_format_file:
    filepaths.insert(0, ai_response_format_file)
    

def remove_ast_comments_and_empty_docstrings(content):
    tree = ast.parse(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.body:
            first_statement = node.body[0]
            if isinstance(first_statement, ast.Expr) and isinstance(first_statement.value, ast.Constant) and isinstance(first_statement.value.value, str):
                node.body.pop(0)
        elif isinstance(node, ast.ClassDef) and node.body:
            first_statement = node.body[0]
            if isinstance(first_statement, ast.Expr) and isinstance(first_statement.value, ast.Constant) and isinstance(first_statement.value.value, str):
                node.body.pop(0)
        elif isinstance(node, ast.Module) and isinstance(node.body[-1], ast.Expr) and isinstance(node.body[-1].value, ast.Constant) and isinstance(node.body[-1].value.value, str) and not hasattr(node.body[-1], 'targets'):
            node.body.pop()
    return ast.unparse(tree)

def remove_comments(content):
    content = remove_ast_comments_and_empty_docstrings(content)
    content = re.sub(r'(?<!\\)#.*', '', content)
    # 新增删除空白行的逻辑
    content = '\n'.join([line for line in content.split('\n') if line.strip()])
    return content

def ensure_file_exists(filepath):
    if not os.path.exists(filepath):
        directory = os.path.dirname(filepath)
        if directory:
             os.makedirs(directory,exist_ok=True)
        with open(filepath,"w") as f:
            f.write("")
            pass

def find_file_in_phone_storage(file_name):
    # 假设手机存储的根目录为 '/storage'
    root_directory = "/storage/emulated/0"
    for root, dirs, files in os.walk(root_directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return None
    
import ftfy
def write_to_file(output):
    docs_filepath = "/storage/emulated/0/我的文档/vivo文档/out_to_ai.txt"
    output = ftfy.fix_text(output)
    with open(docs_filepath, "w", encoding="utf8") as f:
        f.write(output)
        #print(output)


def get_all_file_paths(input_list, check_suffixes=None):
    all_file_paths = []
    for item in input_list:
        if isinstance(item, str):
            if os.path.isfile(item):
                all_file_paths.append(item)
            elif os.path.isdir(item):
                all_file_paths.extend(_traverse_directory(item, check_suffixes))
        elif isinstance(item, list) and len(item) >= 1:
            dir_path = item[0]
            if os.path.isdir(dir_path):
                suffixes = item[1:] if len(item) > 1 else []
                suffixes.extend(check_suffixes)
                all_file_paths.extend(_traverse_directory(dir_path, suffixes))

    return all_file_paths


def _traverse_directory(dir_path, suffixes=None):
    file_paths = []
    for root, dirs, files in os.walk(dir_path):
        # 剔除__pycache__和隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.') and d!= '__pycache__']
        for file in files:
            if not suffixes or any(file.endswith(suffix) for suffix in suffixes):
                file_paths.append(os.path.join(root, file))
    return file_paths
    
format_text = """
文件名：{}
文件内容：
{}
"""
if __name__ == "__main__":
    format_list = []
    filepaths = get_all_file_paths(filepaths)
    for filepath in filepaths:
        
        try:
            ensure_file_exists(filepath)
            with open(filepath, "r") as f:
                content = f.read()
                if content:
                    if filepath.endswith(".py"):
                        content = remove_comments(content)
                format_list.append(format_text.format(filepath, content))
        except BaseException as e:
            print("文件处理出错：", filepath)
            traceback.print_exc()
            raise e
            
    if is_write_prompt_in_file:
        # promt 在文档内
        output = "\n".join([prompt, *format_list])
        #print(output)
        write_to_file(output)
        #path = find_file_in_phone_storage(docs_filepath)
        print(out_prompt)
        input()
    else:
        # promt 在文档外
        output = "\n".join(format_list)
        write_to_file(output)
        print(prompt)
        input()
    