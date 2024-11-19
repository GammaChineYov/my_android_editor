from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
import math


class FloatingButton(Button):
    def __init__(self, **kwargs):
        super(FloatingButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 100)
        window_center_x = Window.width / 2 - self.size[0] / 2
        window_center_y = Window.height / 2 - self.size[1] / 2
        self.pos = (window_center_x, window_center_y)

        with self.canvas:
            Color(1, 0, 0, 1)
            Ellipse(pos=self.pos, size=self.size)
            Rectangle(texture=self.texture, size=self.size, pos=self.pos)
        self.drag_start_pos = None
        self.is_double_tapped = False
        self.surrounding_buttons = []  # 用于存储围绕的按钮

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            print("按钮按下")
            if touch.is_double_tap:
                self.is_double_tapped = True
                self.show_surrounding_buttons()
            else:
                self.drag_start_pos = touch.pos
            return True
        return super(FloatingButton, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            print("按钮释放")
            if self.is_double_tapped:
                if not touch.is_double_tap:
                    self.hide_surrounding_buttons()
                    self.is_double_tapped = False
            else:
                self.drag_start_pos = None
        return super(FloatingButton, self).on_touch_up(touch)

    def on_touch_move(self, touch):
        if self.drag_start_pos:
            new_x = touch.pos[0] - self.drag_start_pos[0] + self.pos[0]
            new_y = touch.pos[1] - self.drag_start_pos[1] + self.pos[1]

            if new_x < 0:
                new_x = 0
            elif new_x > Window.width - self.size[0]:
                new_x = Window.width - self.size[0]

            if new_y < 0:
                new_y = 0
            elif new_y > Window.height - self.size[1]:
                new_y = Window.height - self.size[1]

            self.pos = (new_x, new_y)

            for child in self.canvas.children:
                if isinstance(child, Ellipse) or isinstance(child, Rectangle):
                    child.pos = self.pos
        return super(FloatingButton, self).on_touch_move(touch)

    def show_surrounding_buttons(self):
        button_size = 50
        button_gap = 20
        center_x, center_y = self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2
        radius = math.sqrt((2.5 * button_size) ** 2 / (2 * (1 - math.cos(2 * math.pi / 8))))
        angle_step = 360 / 8

        for i in range(8):
            angle = math.radians(i * angle_step)
            x = center_x + radius * math.cos(angle) - button_size / 2
            y = center_y + radius * math.sin(angle) - button_size / 2

            if 0 <= x <= Window.width - button_size and 0 <= y <= Window.height - button_size:
                button = Button(size=(button_size, button_size), pos=(x, y))
                with button.canvas:
                    Color(0, 1, 0, 1)
                    Ellipse(pos=(0, 0), size=button_size)
                    Rectangle(texture=button.texture, size=button_size, pos=(0, 0))
                self.surrounding_buttons.append(button)

        layout = self.parent
        for button in self.surrounding_buttons:
            layout.add_widget(button)

    def hide_surrounding_buttons(self):
        layout = self.parent
        for button in self.surrounding_buttons:
            layout.remove_widget(button)
        self.surrounding_buttons = []


class MyApp(App):
    def build(self):
        layout = FloatLayout()
        floating_button = FloatingButton(text='点击我')
        layout.add_widget(floating_button)
        return layout


if __name__ == '__main__':
    MyApp().run()