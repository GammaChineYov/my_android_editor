import re
import shutil
import os
from bs4 import BeautifulSoup

output_filepath = "docs.plyer.txt"

format_text = """
文件名:{}
文件内容:
{}
"""

docs_format_list = []
docs_dir = "docs/"

for root, dirs, files in os.walk(docs_dir):
    for file in files:
        file_path = os.path.join(root, file)
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            body_content = soup.find('body')
            if body_content:
                # 去除所有的 <script> 和 <style> 标签
                for script in body_content.find_all('script'):
                    script.decompose()
                for style in body_content.find_all('style'):
                    style.decompose()
                # 去除标签中的属性
                for tag in body_content.find_all(True):
                    tag.attrs = {}
                text_content = body_content.get_text()
                # 使用正则表达式去除全是空格或只有空格的行
                cleaned_text = re.sub(r'^\s*$', '', text_content, flags=re.MULTILINE)
                char_count = len(cleaned_text)
                print(f"文件 {file_path} 处理后的字符数为：{char_count}")
                docs_format_list.append(format_text.format(file_path, cleaned_text))

with open(output_filepath, "w", encoding="utf-8") as f:
    f.write("\n".join(docs_format_list))

#shutil.move("/content/docs", "/content/drive/MyDrive/docs")