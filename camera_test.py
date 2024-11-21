from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics.texture import Texture
import time

class CameraApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # 创建相机实例并设置相关属性
        self.camera = Camera(resolution=(640, 480), play=True)
        layout.add_widget(self.camera)

        # 创建操作按钮布局
        button_layout = BoxLayout(size_hint_y=None, height='48dp')

        # 拍照按钮
        self.take_picture_button = Button(text='拍照')
        self.take_picture_button.bind(on_release=self.take_picture)
        button_layout.add_widget(self.take_picture_button)

        # 切换摄像头按钮（假设设备有多个摄像头）
        self.switch_camera_button = Button(text='切换摄像头')
        self.switch_camera_button.bind(on_release=self.switch_camera)
        button_layout.add_widget(self.switch_camera_button)

        layout.add_widget(button_layout)

        return layout

    def take_picture(self, instance):
        # 获取当前时间作为图片文件名的一部分，避免文件名冲突
        current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        filename = f'photo_{current_time}.png'

        # 保存相机当前帧为图片
        self.camera.export_to_png(filename)

    def switch_camera(self, instance):
        # 获取当前使用的摄像头索引
        current_index = self.camera.index
        # 切换到另一个摄像头（假设设备有两个摄像头，索引为0和1）
        new_index = (current_index + 1) % 2
        self.camera.index = new_index

if __name__ == '__main__':
    CameraApp().run()