import psutil
import socket
from concurrent.futures import ThreadPoolExecutor

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


found_ip = None

def scan_ip(ip, port):
    global found_ip
    if found_ip:
        return
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        print(f"找到服务端在IP: {ip}")
        found_ip = ip
        s.close()
        return ip
    except Exception:
        pass


def scan_ips_threaded():
    global found_ip
    ip_range_start, ip_range_end = get_client_local_network_info()
    if not ip_range_start or not ip_range_end:
        print("无法获取客户端本地网络信息，无法进行IP扫描。")
        return

    PORT = 5000
    found_ips = []

    with ThreadPoolExecutor(max_workers=10)  as executor:
     # 设置线程池最大线程数为10，可根据实际情况调整
    
        tasks = []
        for i in range(int(ip_range_start.split('.')[3]), int(ip_range_end.split('.')[3]) + 1):
            ip = f"{ip_range_start.split('.')[0]}.{ip_range_start.split('.')[1]}.{ip_range_start.split('.')[2]}.{i}"
            task = executor.submit(scan_ip, ip, PORT)
            tasks.append(task)

        for task in tasks:
            result = task.result()
            if result:
                found_ips.append(result)

    if found_ips:
        return found_ips[0]
    else:
        print("未找到服务端IP。")


if __name__ == '__main__':
    scan_ips_threaded()
