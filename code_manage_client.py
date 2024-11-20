import requests
import os
from code_manage_utils import compress_directory_to_zip, get_client_local_network_info, find_server_ip,extract_zip_to_directory
# 要上传的目录路径，可根据实际情况修改
directory_path = "src"
download_directory_path = "downloaded_files"
temp_dir = ".client.temp/"
url_upload = "http://{server_ip}:5000/upload-directory"
url_download = "http://{server_ip}:5000/download/{directory_name}"


# 上传目录压缩包的函数
def upload_directory_zip(zip_file_path, server_ip):
    with open(zip_file_path, 'rb') as f:
        files = {'directory': (os.path.basename(zip_file_path), f)}
        url_upload_full = url_upload.format(server_ip=server_ip)
        response_upload = requests.post(url_upload_full, files=files)
        if response_upload.status_code == 200:
            print("目录压缩包上传成功。")
            return True
        else:
            print(f"上传目录压缩包失败，状态码: {response_upload.status_code}")
            return False


# 下载目录的函数
def download_directory(server_ip, directory_name):
    url_download_full = url_download.format(server_ip=server_ip, directory_name=directory_name)
    response_download = requests.get(url_download_full)
    if response_download.status_code == 200:
        zip_file_path = os.path.join(download_directory_path, directory_name + '.zip')
        os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)
        with open(zip_file_path, 'wb') as f:
            f.write(response_download.content)
        print("提取", zip_file_path, os.path.dirname(zip_file_path))
        extract_zip_to_directory(zip_file_path, os.path.dirname(zip_file_path))
        os.remove(zip_file_path)
        print(f"Directory {directory_name} downloaded successfully")
        return True
    else:
        print(f"下载目录失败，状态码: {response_download.status_code}")
        return False


if __name__ == '__main__':
    # 压缩目录为zip包
    zip_file_path = compress_directory_to_zip(directory_path,temp_dir)

    # 查找服务器IP并上传压缩包
    server_ip = find_server_ip()

    if server_ip:
        print(f"找到服务器端在IP: {server_ip}")
        print("开始进行上传:", zip_file_path)
        if upload_directory_zip(zip_file_path, server_ip):
            # 假设上传成功，获取目录名后进行下载
            directory_name = os.path.splitext(os.path.basename(zip_file_path))[0]
            print("上传成功，开始下载测试:", directory_name)
            if download_directory(server_ip, directory_name):
                print("整个上传和下载流程完成。")
            else:
                print("下载失败")
    else:
        print("未找到服务器端IP，无法进行上传和下载操作。")

    # 清理临时生成的zip文件
    os.remove(zip_file_path)
