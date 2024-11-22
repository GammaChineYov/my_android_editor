import os
import shutil
import ast
import re

prompt = r"""
根据文档与目前项目进度，选取main.py与一个文件进行完善需求与项目的开发
需求：在Main.py实现一个良好扩展的函数化kivy应用：
-CanvasUtil
.函数：清除画布
.函数：绘制直线，颜色
.函数：在画布绘制RectX（*args，单个/列表/多维）
-RectX（继承Rect）：
.字段：颜色
.字段：线宽
-MyAPP
.设置ui文本的labelbase的基础font为font_abc.ttf
.函数（初始化时调用）：在画布区生成n*m的RectX，间隙为x和y，与画布边框间距mx和my，返回二维RectX数组
.函数：设置RectX的颜色（*args）
.函数：刷新画布
.函数：随机颜色
.其它函数：具有重复逻辑的代码块
.使用布局文本生成这个布局:
垂直：（
垂直：最大化，画布，灰色；
水平： 宽度最大化，高1/15（
按钮："├"（用Util将RectX组按垂直中心对齐分组并按组随机颜色）
按钮："↑"(用Util将RectX组的按向上对齐分组并按组随机颜色)
按钮："/"(用户在画布区滑动动态绘制一条线段，过线段的RectX改变颜色)
按钮："□"（用户在画布区滑动动态绘制一个RectX边框，结束后用Util分组，将RectX组中被选中对象线宽加粗，弃选后恢复）
按钮："|"(用户点击画布区时生成过该点的竖线，使用Util将RectX按竖线左右，按组随机颜色)；
）
水平：宽度最大化，高1/15（
按钮："┴"（用Util将RectX组按水平中心对齐分组并按组随机颜色）
按钮："←"(向左对齐分组，同"↑")
按钮："↓"(向下对齐分组，同"↑")
按钮："→"(向右对齐分组，同"↑")
按钮："—"（用户点击画布区时生成过该点的横线，使用Util将RectX组重新按横线上下分组，按组随机颜色）
）
）
"""
filepaths = [
    "Main.py",
    "kivy_utils.py",
    "main_screen.kv",
    "utils/__init__.py",
    "utils/rect.py",
    "utils/rect_utils.py",
    "utils/vector2.py"
]

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


if __name__ == "__main__":
    format_text = """
    文件名：{}
    文件内容：
    {}
    """
    format_list = []
    for filepath in filepaths:
        with open(filepath, "r") as f:
            content = f.read()
            if filepath.endswith(".py"):
                content = remove_comments(content)
            format_list.append(format_text.format(filepath, content))
    
    output = "\n".join([prompt, *format_list])
    print(output)
    input()