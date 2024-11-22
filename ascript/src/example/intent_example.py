from typing import Optional
from ascript import android
from android.content import Intent, Context
from android.net import Uri
from android.provider import Settings, MediaStore
from ascript.android.system import R

def open_app(app_name_or_package: str) -> None:
    """
    启动应用程序

    参数:
    app_name_or_package (str): 应用程序的名称或包名
    """
    from ascript.android import system
    system.open(app_name_or_package)

def open_url(url: str) -> None:
    """
    使用系统浏览器打开网页

    参数:
    url (str): 要打开的网页网址
    """
    from ascript.android import system
    system.browser(url)

def take_photo() -> None:
    """
    打开相机应用拍照
    """
    it = Intent("android.media.action.IMAGE_CAPTURE")
    it.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    R.context.startActivity(it)

def pick_image() -> None:
    """
    打开相册选择图片
    """
    it = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
    it.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    R.context.startActivity(it)

def share_text(text: str) -> None:
    """
    分享文本内容到其他应用

    参数:
    text (str): 要分享的文本内容
    """
    it = Intent(Intent.ACTION_SEND)
    it.putExtra(Intent.EXTRA_TEXT, text)
    it.setType("text/plain")
    it.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    R.context.startActivity(it)

def share_image(image_path: str) -> None:
    """
    分享图片到其他应用

    参数:
    image_path (str): 要分享的图片路径
    """
    it = Intent(Intent.ACTION_SEND)
    image_uri = R.img(image_path)
    it.putExtra(Intent.EXTRA_STREAM, image_uri)
    it.setType("image/png")  # 根据图片格式设置类型
    it.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    R.context.startActivity(it)

def get_device_location() -> Optional[tuple[float, float]]:
    """
    获取设备位置信息（假设已获取位置权限）

    返回:
    Optional[tuple[float, float]]: 设备的经度和纬度，如果获取失败则返回None
    """
    from android.location import LocationManager
    location_manager = R.context.getSystemService(Context.LOCATION_SERVICE)
    if location_manager.isProviderEnabled(LocationManager.GPS_PROVIDER):
        location = location_manager.getLastKnownLocation(LocationManager.GPS_PROVIDER)
        if location:
            return location.getLongitude(), location.getLatitude()
    return None

def get_accelerometer_data() -> None:
    """
    获取设备加速度计数据（假设已获取传感器权限）
    """
    from android.hardware import SensorManager, Sensor, SensorEvent, SensorEventListener
    sensor_manager = R.context.getSystemService(Context.SENSOR_SERVICE)
    accelerometer = sensor_manager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)

    class AccelerometerListener(SensorEventListener):
        def onSensorChanged(self, event: SensorEvent):
            x = event.values[0]
            y = event.values[1]
            z = event.values[2]
            print("加速度计数据：x =", x, "y =", y, "z =", z)

        def onAccuracyChanged(self, sensor: Sensor, accuracy: int):
            pass

    sensor_listener = AccelerometerListener()
    sensor_manager.registerListener(sensor_listener, accelerometer, SensorManager.SENSOR_DELAY_NORMAL)

# 示例用法
if __name__ == "__main__":
    # 启动应用程序示例
    open_app("微信")  # 按应用名称启动
    open_app("com.tencent.mm")  # 按包名启动

    # 打开网页示例
    open_url("https://www.example.com")

    # 打开相机拍照示例
    take_photo()

    # 打开相册选择图片示例
    pick_image()

    # 分享文本示例
    share_text("这是一段要分享的文本")

    # 分享图片示例
    share_image("image_to_share.png")

    # 获取设备位置信息示例
    location = get_device_location()
    if location:
        print("获取到的设备位置：经度 =", location[0], "纬度 =", location[1])

    # 获取加速度计数据示例
    get_accelerometer_data()