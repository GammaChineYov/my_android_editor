import random

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    @classmethod
    def from_tuple(cls, tup):
        return cls(*tup)

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)
        else:
            raise TypeError('不支持的相加类型')

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x - other, self.y - other)
        else:
            raise TypeError('不支持的相减类型')

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        else:
            raise TypeError('不支持的相乘类型')

    def __truediv__(self, other):
        if isinstance(other, (int, float)) and other!= 0:
            return Vector2(self.x / other, self.y / other)
        else:
            raise TypeError('不支持的相除类型或除数为 0')

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def distance_to(self, other):
        if isinstance(other, Vector2):
            diff = self - other
            return diff.magnitude()
        else:
            raise TypeError('输入必须是 Vector2 类型')

    def __min__(self, other):
        if isinstance(other, Vector2):
            return Vector2(min(self.x, other.x), min(self.y, other.y))
        else:
            raise TypeError('不支持的比较类型')

    def __max__(self, other):
        if isinstance(other, Vector2):
            return Vector2(max(self.x, other.x), max(self.y, other.y))
        else:
            raise TypeError('不支持的比较类型')

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    @classmethod
    def randint(cls, min_x, max_x, min_y, max_y):
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        return cls(x, y)

    @classmethod
    def rand(cls):
        x = random.random()
        y = random.random()
        return cls(x, y)

    # 新增生成 x 和 y 在 0 - 1 范围内的 Vector2 的方法
    @classmethod
    def random_unit(cls):
        x = random.random()
        y = random.random()
        return cls(x, y)

    # 新增将 Vector2 的值转换为整数的方法
    def to_int(self):
        return Vector2(int(self.x), int(self.y))