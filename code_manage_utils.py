
import zipfile
import asyncio
import socket
import psutil
import os
from tqdm import tqdm  # 用于显示进度条
import socket

# 获取服务器端局域网IP地址用于绑定
def get_local_ip():
    addrs = psutil.net_if_addrs()
    for interface, addr_list in addrs.items():
        for addr in addr_list:
            if addr.family == socket.AF_INET:
                ip = addr.address
                if "192.168" in ip or "10." in ip or "172.16" in ip or "172.31" in ip:
                    return ip



def is_port_used(ip="127.0.0.1", port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((ip, port))
            return False
        except OSError as e:
            if e.errno == 98:  # 表示地址已被使用的错误码
                return True
            raise

# 获取客户端局域网IP地址范围用于扫描
def get_client_local_network_info():
    addrs = psutil.net_if_addrs()
    for interface, addr_list in addrs.items():
        for addr in addr_list:
            if addr.family == socket.AF_INET:
                ip = addr.address
                if "192.168" in ip or "10." in ip or "172.16" in ip or "172.31" in ip:
                    ip_parts = ip.split('.')
                    ip_range_start = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.1"
                    ip_range_end = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.255"
                    return ip_range_start, ip_range_end


# 查找服务器IP地址的函数
def find_server_ip(port=5000):
    local_ip = get_local_ip()
    if is_port_used(ip=local_ip, port=port):
        return local_ip
    ip_range_start, ip_range_end = get_client_local_network_info()
    if not ip_range_start or not ip_range_end:
        print("无法获取客户端本地网络信息，无法进行IP扫描。")
        return None

    PORT = port
    tasks = []
    found_ips = []

    async def scan_ip_async(ip, port):
        try:
            reader, writer = await asyncio.open_connection(ip, port)
            print(f"找到服务端在IP: {ip}")
            found_ips.append(ip)
            writer.close()
            #await writer.drain()
            return ip
        except Exception:
            pass

    async def scan_ips_async():
        for i in range(int(ip_range_start.split('.')[3]), int(ip_range_end.split('.')[3]) + 1):
            ip = f"{ip_range_start.split('.')[0]}.{ip_range_start.split('.')[1]}.{ip_range_start.split('.')[2]}.{i}"
            task = asyncio.create_task(scan_ip_async(ip, PORT))
            tasks.append(task)

        await asyncio.gather(*tasks)

    asyncio.run(scan_ips_async())

    if found_ips:
        return found_ips[0]
    return None


if __name__ == '__main__':
    res = find_server_ip(5000)

    if res:
        print(f"找到服务端IP: {res}")  # 这里也可根据需求输出全部找到的IP
    else:
        print("未找到服务端IP。")


# 将目录压缩成zip包的函数
def compress_directory_to_zip(directory_path, zip_file_dir=".temp/"):
    directory_path = os.path.abspath(directory_path)
    zip_file_name = os.path.basename(directory_path) + '.zip'
    zip_file_path = os.path.join(zip_file_dir, zip_file_name)
    rel_path = directory_path.rsplit("/",1)[0]
    os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)
    
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        total_files = sum([len(files) for root, dirs, files in os.walk(directory_path)])
        with tqdm(total=total_files, desc="Compressing directory") as pbar:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_full_path = os.path.join(root, file)
                    # 获取相对路径，去掉前面的 "uploads/" 部分，以得到期望的根目录结构
                    relative_path = os.path.relpath(file_full_path, rel_path)
                    zipf.write(file_full_path, arcname=relative_path)
                    pbar.update(1)

    return zip_file_path

def extract_zip_to_directory(from_filepath, to_dirpath):
    # 解压目录压缩包到指定目录
    with zipfile.ZipFile(from_filepath, 'r') as zip_ref:
        zip_ref.extractall(to_dirpath)
