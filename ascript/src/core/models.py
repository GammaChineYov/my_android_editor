import json
from typing import List, Tuple


class DeviceInfo:
    """
    设备信息类，用于存储设备的各种信息
    """

    def __init__(self, device_id: str, device_name: str, screen_info: Tuple[int, int, float],
                 brand: str, model: str, sdk_version: str, android_version: str, ip_address: str,
                 battery_level: int, memory_info: Tuple[int, int, int]):
        """
        初始化设备信息类

        :param device_id: 设备的唯一ID
        :param device_name: 设备名称
        :param screen_info: 屏幕信息，包含高度、宽度和密度的元组
        :param brand: 设备品牌
        :param model: 设备型号
        :param sdk_version: 设备SDK版本
        :param android_version: 设备Android版本
        :param ip_address: 设备本地IP地址
        :param battery_level: 电池电量百分比
        :param memory_info: 内存信息，包含剩余内存、已用内存和总内存的元组
        """
        self.device_id = device_id
        self.device_name = device_name
        self.screen_height, self.screen_width, self.screen_density = screen_info
        self.brand = brand
        self.model = model
        self.sdk_version = sdk_version
        self.android_version = android_version
        self.ip_address = ip_address
        self.battery_level = battery_level
        self.remaining_memory, self.used_memory, self.total_memory = memory_info

    def __str__(self) -> str:
        """
        返回设备信息的JSON格式字符串表示

        :return: JSON格式字符串
        """
        return json.dumps({
            "device_id": self.device_id,
            "device_name": self.device_name,
            "screen_height": self.screen_height,
            "screen_width": self.screen_width,
            "screen_density": self.screen_density,
            "brand": self.brand,
            "model": self.model,
            "sdk_version": self.sdk_version,
            "android_version": self.android_version,
            "ip_address": self.ip_address,
            "battery_level": self.battery_level,
            "remaining_memory": self.remaining_memory,
            "used_memory": self.used_memory,
            "total_memory": self.total_memory
        }, indent=4, ensure_ascii=False)

    def __repr__(self) -> str:
        """
        返回设备信息的可打印表示，与__str__相同

        :return: JSON格式字符串
        """
        return self.__str__()

    @staticmethod
    def get_device_info() -> 'DeviceInfo':
        """
        静态方法，用于获取设备信息并返回DeviceInfo对象

        :return: DeviceInfo对象，包含设备的各种信息
        """
        from ascript.android.system import Device

        device_id = Device.id()
        device_name = Device.name()
        screen_info = Device.display()
        brand = Device.brand()
        model = Device.model()
        sdk_version = Device.sdk()
        android_version = Device.version()
        ip_address = Device.ip()
        battery_level = Device.battery()
        memory_info = Device.memory()

        return DeviceInfo(
            device_id,
            device_name,
            (screen_info.heightPixels, screen_info.widthPixels, screen_info.density),
            brand,
            model,
            sdk_version,
            android_version,
            ip_address,
            battery_level,
            (memory_info[0], memory_info[1], memory_info[2])
        )


class AppInstallInfo:
    """
    应用安装信息类，用于存储已安装应用的信息
    """

    def __init__(self, app_name: str, app_size: int, is_sd: bool, is_system: bool,
                 package_name: str, apk_path: str):
        """
        初始化应用安装信息类

        :param app_name: 应用名称
        :param app_size: 应用大小（字节）
        :param is_sd: 是否安装在SD卡中
        :param is_system: 是否为系统应用
        :param package_name: 应用包名
        :param apk_path: 应用安装路径
        """
        self.app_name = app_name
        self.app_size = app_size
        self.is_sd = is_sd
        self.is_system = is_system
        self.package_name = package_name
        self.apk_path = apk_path

    def __str__(self) -> str:
        """
        返回应用安装信息的JSON格式字符串表示

        :return: JSON格式字符串
        """
        return json.dumps({
            "app_name": self.app_name,
            "app_size": self.app_size,
            "is_sd": self.is_sd,
            "is_system": self.is_system,
            "package_name": self.package_name,
            "apk_path": self.apk_path
        }, indent=4, ensure_ascii=False)

    def __repr__(self) -> str:
        """
        返回应用安装信息的可打印表示，与__str__相同

        :return: JSON格式字符串
        """
        return self.__str__()

    @staticmethod
    def get_installed_apps() -> List['AppInstallInfo']:
        """
        静态方法，用于获取已安装应用列表并返回AppInstallInfo对象列表

        :return: 包含AppInstallInfo对象的列表，每个对象表示一个已安装应用的信息
        """
        from ascript.android.system import Device

        apps = Device.apps()
        app_install_info_list = []

        for app in apps:
            app_install_info_list.append(AppInstallInfo(
                app.appName,
                app.appSize,
                app.isSd(),
                app.isSystem(),
                app.appPackageName,
                app.apkPath
            ))

        return app_install_info_list
        
    @staticmethod
    def load_installed_apps(update=False):
        from ascript.android.system import R
        import os
        cache_path = R.root(".cache_app_install_info.json")
        if update or not os.path.exists(cache_path):
            apps = AppInstallInfo.get_installed_apps()
            with open(cache_path,"w") as f:
                f.write(
                json.dumps(
                 [str(app) for app in apps],
                 indent=4, ensure_ascii=False))
        data = ""
        with open(cache_path, "r") as f:
            data = json.load(f)
        apps = [AppInstallInfo(**json.loads(app)) for app in data]
        return apps
        
        

class DeviceRunningInfo:
    """
    设备运行信息类，用于存储设备当前运行的应用信息
    """

    def __init__(self, app_name: str, package_name: str, activity: str):
        """
        初始化设备运行信息类

        :param app_name: 当前运行的应用名称
        :param package_name: 当前运行应用的包名称
        :param activity: 当前运行应用的Activity
        """
        self.app_name = app_name
        self.package_name = package_name
        self.activity = activity

    def __str__(self) -> str:
        """
        返回设备运行信息的JSON格式字符串表示

        :return: JSON格式字符串
        """
        return json.dumps({
            "app_name": self.app_name,
            "package_name": self.package_name,
            "activity": self.activity
        }, indent=4, ensure_ascii=False)

    def __repr__(self) -> str:
        """
        返回设备运行信息的可打印表示，与__str__相同

        :return: JSON格式字符串
        """
        return self.__str__()

    @staticmethod
    def get_running_app_info() -> 'DeviceRunningInfo':
        """
        静态方法，用于获取设备当前运行的应用信息并返回DeviceRunningInfo对象

        :return: DeviceRunningInfo对象，包含当前运行应用的名称、包名和Activity
        """
        from ascript.android.system import Device

        app_info = Device.current_appinfo()

        return DeviceRunningInfo(
            app_info.name,
            app_info.packageName,
            app_info.activity
        )