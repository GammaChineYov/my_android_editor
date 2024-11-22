from enum import Enum
from .rect import Rect  # 假设 Rect 类在当前目录下的 rect.py 文件中

class AlignTypeEnum(Enum):
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    HORIZONTAL_CENTER = 'HORIZONTAL_CENTER'
    VERTICAL_CENTER = 'VERTICAL_CENTER'

class PositionExtractor:
    def __init__(self, align_type):
        self.align_type = align_type

    def extract(self, rect):
        if self.align_type == AlignTypeEnum.TOP:
            return rect.ymin
        elif self.align_type == AlignTypeEnum.BOTTOM:
            return rect.ymax
        elif self.align_type == AlignTypeEnum.LEFT:
            return rect.xmin
        elif self.align_type == AlignTypeEnum.RIGHT:
            return rect.xmax
        elif self.align_type == AlignTypeEnum.HORIZONTAL_CENTER:
            return (rect.xmin + rect.xmax) / 2
        elif self.align_type == AlignTypeEnum.VERTICAL_CENTER:
            return (rect.ymin + rect.ymax) / 2
        else:
            raise ValueError("Invalid alignment type")

class RectUtils:
    @staticmethod
    def group_by_alignment(rect_list, align_type):
        extractor = PositionExtractor(align_type)
        sorted_list = sorted(rect_list, key=extractor.extract)
        groups = []
        current_group = []
        prev_pos = None

        for rect in sorted_list:
            pos = extractor.extract(rect)
            if prev_pos is None or pos == prev_pos:
                current_group.append(rect)
            else:
                groups.append(current_group)
                current_group = [rect]
            prev_pos = pos

        if current_group:
            groups.append(current_group)

        return groups

    @staticmethod
    def group_by_vertical_intersection(rect_list, gap_tolerance=0):
        sorted_list = sorted(rect_list, key=lambda rect: rect.ymin)
        groups = []
        rect_groups = []

        for i in range(len(sorted_list)):
            combined_rect = sorted_list[i].copy()
            current_group = [sorted_list[i]]
            for j in range(i + 1, len(sorted_list)):
                if sorted_list[j].is_vertically_intersecting(combined_rect, gap_tolerance):
                    current_group.append(sorted_list[j])
                    combined_rect = RectUtils.combine_rects(combined_rect, sorted_list[j])
            groups.append(current_group)
            rect_groups.append(combined_rect)

        return groups, rect_groups

    @staticmethod
    def combine_rects(rect1, rect2):
        xmin = min(rect1.xmin, rect2.xmin)
        xmax = max(rect1.xmax, rect2.xmax)
        ymin = min(rect1.ymin, rect2.ymin)
        ymax = max(rect1.ymax, rect2.ymax)
        center_x = (xmin + xmax) / 2
        center_y = (ymin + ymax) / 2
        width = xmax - xmin
        height = ymax - ymin
        return Rect(center=(center_x, center_y), width=width, height=height)

    @staticmethod
    def group_by_horizontal_split(rect_list, split_lines):
        groups = []
        sorted_list = sorted(rect_list, key=lambda rect: rect.ymin)
        start = 0
        for line in split_lines:
            current_group = []
            for rect in sorted_list[start:]:
                if rect.ymax < line:
                    current_group.append(rect)
                else:
                    break
            groups.append(current_group)
            start += len(current_group)
        groups.append(sorted_list[start:])
        return groups

    @staticmethod
    def group_by_vertical_split(rect_list, split_lines):
        groups = []
        sorted_list = sorted(rect_list, key=lambda rect: rect.xmin)
        start = 0
        for line in split_lines:
            current_group = []
            for rect in sorted_list[start:]:
                if rect.xmax < line:
                    current_group.append(rect)
                else:
                    break
            groups.append(current_group)
            start += len(current_group)
        groups.append(sorted_list[start:])
        return groups

    @staticmethod
    def group_by_inside_rect(rect_list, target_rect, allow_intersection=True):
        groups = []
        inside_group = []
        outside_group = []

        for rect in rect_list:
            if allow_intersection and target_rect.is_vertically_intersecting(rect) and target_rect.is_horizontally_intersecting(rect):
                inside_group.append(rect)
            else:
                outside_group.append(rect)

        groups.append(inside_group)
        groups.append(outside_group)

        return groups