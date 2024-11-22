import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import re

class PlyerDocParser:
    def __init__(self, base_url, limit_url):
        self.base_url = base_url
        self.limit_url = limit_url
        self.current_page_url = None

    def get_soup(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        print(f"请求 URL: {url}, 状态码: {response.status_code}")
        if response.status_code == 200:
            self.current_page_url = url
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"无法访问网址：{url}，状态码: {response.status_code}")
            return None

    def parse_link_to_filepath(self, link):
        limit_index = link.find(self.limit_url) + len(self.limit_url)
        sub_url = link[limit_index:]
        if sub_url.endswith('/'):
            sub_url = sub_url.rstrip('/')
        if '.' in sub_url:
            sub_url = sub_url.rsplit('.', 1)[0]
        print(f"生成文件路径：{sub_url}.html")
        return sub_url + '.html'

    def parse_link_to_request(self, soup):
        links = []
        base_url_parsed = urlparse(self.base_url)
        current_page_path = urlparse(self.current_page_url).path.rsplit('/', 1)[0] + '/'
        print(f"当前页面路径：{current_page_path}")
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                print(f"原始链接：{href}")
                if '#' in href:
                    href = href.split('#')[0]
                    print(f"去除锚点后链接：{href}")
                # 调整链接拼接逻辑，使用urljoin处理相对链接
                full_href = urljoin(self.current_page_url, href)
                print(f"拼接后链接：{full_href}")
                href_parsed = urlparse(full_href)
                if href_parsed.netloc == base_url_parsed.netloc and full_href.startswith(self.limit_url):
                    file_name = self.parse_link_to_filepath(full_href)
                    links.append(full_href)
                    print(f"识别到可请求链接：{full_href}")
        return links

    def download_page(self, url, output_dir):
        soup = self.get_soup(url)
        if soup:
            file_name = self.parse_link_to_filepath(url)
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print(f"已下载页面：{url} 到 {file_path}")

    def recursive_download(self, start_url, limit_url, output_dir):
        visited = set()
        to_visit = [start_url]

        while to_visit:
            current_url = to_visit.pop(0)
            if current_url in visited or not current_url.startswith(self.base_url):
                print(f"跳过链接：{current_url}")
                continue
            visited.add(current_url)

            soup = self.get_soup(current_url)
            if soup and current_url.startswith(limit_url):
                self.download_page(current_url, output_dir)
                links = self.parse_link_to_request(soup)
                for new_url in links:
                    print(f"新增请求：{new_url}")
                to_visit.extend(links)


def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


if __name__ == "__main__":
    start_url = "https://plyer.readthedocs.io/en/2.0.0/"
    #https://plyer.readthedocs.io/en/latest/index.html"
    limit_url = "https://plyer.readthedocs.io/en/2.0.0/"
    #https://plyer.readthedocs.io/en/latest/"
    output_dir = "docs"

    base_url = get_base_url(start_url)
    parser = PlyerDocParser(base_url, limit_url)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    parser.recursive_download(start_url, limit_url, output_dir)