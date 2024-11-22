import logging
from model import *

# 配置日志记录到文件
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 获取设备信息并记录到日志
device_info = DeviceInfo.get_device_info()
logging.info(f"设备ID: {device_info.device_id}")
logging.info(f"设备名称: {device_info.device_name}")
logging.info(f"屏幕高度: {device_info.screen_height}")
logging.info(f"屏幕宽度: {device_info.screen_width}")
logging.info(f"屏幕密度: {device_info.screen_density}")
logging.info(f"设备品牌: {device_info.brand}")
logging.info(f"设备型号: {device_info.model}")
logging.info(f"SDK版本: {device_info.sdk_version}")
logging.info(f"Android版本: {device_info.android_version}")
logging.info(f"IP地址: {device_info.ip_address}")
logging.info(f"电池电量: {device_info.battery_level}%")
logging.info(f"剩余内存: {device_info.remaining_memory} 字节")
logging.info(f"已用内存: {device_info.used_memory} 字节")
logging.info(f"总内存: {device_info.total_memory} 字节")

# 获取已安装应用列表并记录到日志
installed_apps = AppInstallInfo.get_installed_apps()
for app in installed_apps:
    logging.info(f"应用名称: {app.app_name}")
    logging.info(f"应用大小: {app.app_size} 字节")
    logging.info(f"是否在SD卡: {app.is_sd}")
    logging.info(f"是否为系统应用: {app.is_system}")
    logging.info(f"包名: {app.package_name}")
    logging.info(f"安装路径: {app.apk_path}")

# 获取设备当前运行的应用信息并记录到日志
running_app_info = DeviceRunningInfo.get_running_app_info()
logging.info(f"当前运行应用名称: {running_app_info.app_name}")
logging.info(f"当前运行应用包名: {running_app_info.package_name}")
logging.info(f"当前运行应用Activity: {running_app_info.activity}")