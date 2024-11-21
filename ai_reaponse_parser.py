import re

# 读取文本文件内容
with open('ai_response.txt', 'r') as file:
    content = file.read()

# 豆包直接复制内容
if True:
    content = content.split("python\n", 1)[-1]

# 使用正则表达式进行替换
pattern = r'"文件路径": "(.+)",.*"文件内容": """(.*?)""",'

# 文件路径 文件内容
file_contents = re.findall(pattern, content, flags=re.DOTALL)
for filepath, file_content in file_contents:
    print(filepath)
    input("输入任意键继续")
    print(file_content)
    cmd = input("回车写入，空格跳过，任意键退出")
    if cmd == " ":
        continue
    elif cmd:
        print("退出写入")
        break
    with open(filepath, "w") as f:
        f.write(file_content)
        print("写入完成")

pattern2 = r'"文件内容": """(.*?)""",'
replacement = r'"文件内容": "",'
new_content = re.sub(pattern2, replacement, content, flags=re.DOTALL)
# 将处理后的内容写入新的 Python 文件
with open('ai_response_processed.py', 'w') as new_file:
    new_file.write(new_content)
    
# 执行新生成的 Python 文件
#import ai_response_processed