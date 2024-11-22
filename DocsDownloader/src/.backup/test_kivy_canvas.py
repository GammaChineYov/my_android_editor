from kivy.graphics import Color, Line       
from utils import Rect
from kivy.utils import get_color_from_hex

class CanvasUtil:
    @staticmethod
    def clear_canvas(canvas):
        """清除画布的方法"""
        canvas.clear()

    @staticmethod
    def draw_line(canvas, start, end, color, line_width=1):
        """在画布上绘制直线的方法

        Args:
            canvas (Canvas): 要绘制的画布对象
            start (Vector2): 直线的起点
            end (Vector2): 直线的终点
            color (tuple): 直线的颜色，格式为(r, g, b, a)
            line_width (int): 直线的线宽，默认为1
        """
        with canvas:
            Color(*color)
            Line(points=[start.x, start.y, end.x, end.y], width=line_width)

    @staticmethod
    def draw_rect_x(canvas, rect_x):
        """在画布上绘制单个RectX的方法

        Args:
            canvas (Canvas): 要绘制的画布对象
            rect_x (RectX): 要绘制的RectX对象
        """
        with canvas:
            Color(*rect_x.color)
            Line(rectangle=(rect_x.xmin, rect_x.ymin, rect_x.width, rect_x.height), width=rect_x.line_width)

    @staticmethod
    def draw_rects_x(canvas, rects_x):
        """在画布上绘制多个RectX的方法

        Args:
            canvas (Canvas): 要绘制的画布对象
            rects_x (list): 要绘制的RectX对象列表
        """
        for rect_x in rects_x:
            CanvasUtil.draw_rect_x(canvas, rect_x)
     


class RectX(Rect):
    def __init__(self, center=(0, 0), width=1, height=1, color=(1, 1, 1, 1), line_width=1):
        super().__init__(center, width, height)
        self.color = color
        self.line_width = line_width

    def set_color(self, new_color):
        self.color = new_color

    @classmethod
    def random_color_instance(cls, center=(0, 0), width=1, height=1, line_width=1):
        random_color = get_color_from_hex('{:06x}'.format(random.randint(0, 0xFFFFFF)))
        return cls(center, width, height, random_color, line_width)