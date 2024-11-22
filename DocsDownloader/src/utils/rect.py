class Rect:
    def __init__(self, center=(0, 0), width=1, height=1):
        self._center_x, self._center_y = center
        self._width = width
        self._height = height
        self._update_boundaries()

    def _update_boundaries(self):
        """更新矩形的边界信息"""
        self.half_width = self._width / 2
        self.half_height = self._height / 2
        self._xmin = self._center_x - self.half_width
        self._xmax = self._center_x + self.half_width
        self._ymin = self._center_y - self.half_height
        self._ymax = self._center_y + self.half_height

    @property
    def x(self):
        """获取 x 坐标"""
        return self._center_x

    @x.setter
    def x(self, value):
        """设置 x 坐标并更新边界"""
        self._center_x = value
        self._update_boundaries()

    @property
    def y(self):
        """获取 y 坐标"""
        return self._center_y

    @y.setter
    def y(self, value):
        """设置 y 坐标并更新边界"""
        self._center_y = value
        self._update_boundaries()

    @property
    def center_x(self):
        """获取中心 x 坐标"""
        return self._center_x

    @center_x.setter
    def center_x(self, value):
        """设置中心 x 坐标并更新边界"""
        self._center_x = value
        self._update_boundaries()

    @property
    def center_y(self):
        """获取中心 y 坐标"""
        return self._center_y

    @center_y.setter
    def center_y(self, value):
        """设置中心 y 坐标并更新边界"""
        self._center_y = value
        self._update_boundaries()

    @property
    def width(self):
        """获取宽度"""
        return self._width

    @width.setter
    def width(self, value):
        """设置宽度并检查有效性，然后更新边界"""
        if value < 0:
            raise ValueError('Width must be non-negative.')
        self._width = value
        self._update_boundaries()

    @property
    def height(self):
        """获取高度"""
        return self._height

    @height.setter
    def height(self, value):
        """设置高度并检查有效性，然后更新边界"""
        if value < 0:
            raise ValueError('Height must be non-negative.')
        self._height = value
        self._update_boundaries()

    @property
    def xmin(self):
        """获取最小 x 坐标"""
        return self._xmin

    @xmin.setter
    def xmin(self, value):
        """设置最小 x 坐标并检查有效性，然后更新边界"""
        if value >= self.xmax:
            raise ValueError('xmin must be less than xmax.')
        self._width = self.xmax - value
        self._center_x = (self.xmin + self.xmax) / 2
        self._update_boundaries()

    @property
    def xmax(self):
        """获取最大 x 坐标"""
        return self._xmax

    @xmax.setter
    def xmax(self, value):
        """设置最大 x 坐标并检查有效性，然后更新边界"""
        if value <= self.xmin:
            raise ValueError('xmax must be greater than xmin.')
        self._width = value - self.xmin
        self._center_x = (self.xmin + self.xmax) / 2
        self._update_boundaries()

    @property
    def ymin(self):
        """获取最小 y 坐标"""
        return self._ymin

    @ymin.setter
    def ymin(self, value):
        """设置最小 y 坐标并检查有效性，然后更新边界"""
        if value >= self.ymax:
            raise ValueError('ymin must be less than ymax.')
        self._height = self.ymax - value
        self._center_y = (self.ymin + self.ymax) / 2
        self._update_boundaries()

    @property
    def ymax(self):
        """获取最大 y 坐标"""
        return self._ymax

    @ymax.setter
    def ymax(self, value):
        """设置最大 y 坐标并检查有效性，然后更新边界"""
        if value <= self.ymin:
            raise ValueError('ymax must be greater than ymin.')
        self._height = value - self.ymin
        self._center_y = (self.ymin + self.ymax) / 2
        self._update_boundaries()

    @property
    def min_coord(self):
        """获取最小坐标"""
        return (self.xmin, self.ymin)

    @min_coord.setter
    def min_coord(self, value):
        """设置最小坐标并检查有效性，然后更新边界"""
        xmin, ymin = value
        if xmin >= self.xmax or ymin >= self.ymax:
            raise ValueError('Min coord must be within the bounds of the rectangle.')
        self.xmin = xmin
        self.ymin = ymin
        self._update_boundaries()

    @property
    def max_coord(self):
        """获取最大坐标"""
        return (self.xmax, self.ymax)

    @max_coord.setter
    def max_coord(self, value):
        """设置最大坐标并检查有效性，然后更新边界"""
        xmax, ymax = value
        if xmax <= self.xmin or ymax <= self.ymin:
            raise ValueError('Max coord must be within the bounds of the rectangle.')
        self.xmax = xmax
        self.ymax = ymax
        self._update_boundaries()

    @property
    def center(self):
        """获取中心坐标"""
        return (self._center_x, self._center_y)

    @center.setter
    def center(self, value):
        """设置中心坐标并更新边界"""
        self._center_x, self._center_y = value
        self._update_boundaries()

    def is_horizontally_intersecting(self, other_rect, gap_tolerance=0):
        """检查水平方向的相交情况"""
        return not (self.xmax + gap_tolerance < other_rect.xmin or self.xmin - gap_tolerance > other_rect.xmax)

    def is_vertically_intersecting(self, other_rect, gap_tolerance=0):
        """检查垂直方向的相交情况"""
        return not (self.ymax + gap_tolerance < other_rect.ymin or self.ymin - gap_tolerance > other_rect.ymax)

    def combine_with(self, other_rect):
        """合并两个矩形"""
        xmin = min(self.xmin, other_rect.xmin)
        xmax = max(self.xmax, other_rect.xmax)
        ymin = min(self.ymin, other_rect.ymin)
        ymax = max(self.ymax, other_rect.ymax)
        center_x = (xmin + xmax) / 2
        center_y = (ymin + ymax) / 2
        width = xmax - xmin
        height = ymax - ymin
        self._center_x = center_x
        self._center_y = center_y
        self._width = width
        self._height = height
        self._update_boundaries()

    def copy(self):
        """复制矩形"""
        return Rect(self.center, self.width, self.height)
        
    @classmethod
    def from_vectors(cls, start_vector, end_vector):
        """
        根据两个向量创建 Rect 对象

        参数:
        start_vector (Vector2): 起始向量
        end_vector (Vector2): 结束向量

        返回:
        Rect: 创建的 Rect 对象
        """
        center_x = (start_vector.x + end_vector.x) / 2
        center_y = (start_vector.y + end_vector.y) / 2
        width = abs(end_vector.x - start_vector.x)
        height = abs(end_vector.y - start_vector.y)
        return cls((center_x, center_y), width, height)