import os
import shutil
import ast
import re

prompt = r"""
实现example_textinput_cursor.py
"""
filepaths = [
"src/example/example_textinput_cursor.py",
"src/text_input_cursor/__init__.py",
"src/text_input_cursor/cursor_position_handler.py",
"src/text_input_cursor/touch_event_handler.py",#3.  TouchEventHandler  类：
"src/text_input_cursor/word_index_handler.py",#4.  WordIndexHandler  类：
"src/text_input_cursor/模块划分.txt",
]

is_write_prompt_in_file = True
ai_response_format_file = "ai回答格式.md"
out_prompt = f"按照文档需求实现内容,按照'{ai_response_format_file}'文件格式回复"

if is_write_prompt_in_file and ai_response_format_file:
    filepaths.append(ai_response_format_file)
    

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
    
def write_to_file(output):
    docs_filepath = "/storage/emulated/0/我的文档/vivo文档/for_ai.txt"
    with open(docs_filepath, "w") as f:
        f.write(output)


def get_all_file_paths(input_list):
    all_file_paths = []
    for item in input_list:
        if isinstance(item, str):
            if os.path.isfile(item):
                all_file_paths.append(item)
            elif os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    for file in files:
                        all_file_paths.append(os.path.join(root, file))
        elif isinstance(item, list) and len(item) >= 1:
            dir_path = item[0]
            if os.path.isdir(dir_path):
                suffixes = item[1:] if len(item) > 1 else []
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if not suffixes or any(file.endswith(suffix) for suffix in suffixes):
                            all_file_paths.append(os.path.join(root, file))

    return all_file_paths
    
    
format_text = """
文件名：{}
文件内容：
{}
"""
if __name__ == "__main__":
    format_list = []
    filepaths = get_all_file_paths(filepaths)
    for filepath in filepaths:
        ensure_file_exists(filepath)
        with open(filepath, "r") as f:
            content = f.read()
            if content:
                if filepath.endswith(".py"):
                    content = remove_comments(content)
            format_list.append(format_text.format(filepath, content))
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
    