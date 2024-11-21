from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import re

def text_input_cursor(textinput):
    start = 0
    end = 0
    is_sliding = False
    is_hold_sliding = False
    hold_check_flag = False
    start_touch_pos = (0, 0)
    start_touch_time = 0
    touch_start_cursor_index = 0
    cursor_icon_height = 10
    cursor_icon_width = 5
    hold_check_time = 0.5

    def on_touch_down(touch):
        nonlocal start, end, is_sliding, is_hold_sliding, hold_check_flag, start_touch_pos, start_touch_time, touch_start_cursor_index
        if textinput.collide_point(*touch.pos):
            cursor_index = textinput.cursor_index()
            line, col = textinput.get_cursor_from_index(cursor_index)
            line_height = textinput.line_height
            x, y = touch.pos
            x -= textinput.x
            y -= textinput.y
            if _is_touch_in_cursor_icon(cursor_index, line, col, line_height, x, y):
                textinput.ctrl_start = cursor_index
                is_sliding = True
                start_touch_pos = touch.pos
                start_touch_time = touch.time_start
                hold_check_flag = True
                touch_start_cursor_index = cursor_index
            elif _is_touch_in_cursor_icon(cursor_index, line, col, line_height, x, y, is_end=True):
                textinput.ctrl_end = cursor_index
                is_sliding = True
                start_touch_pos = touch.pos
                start_touch_time = touch.time_start
                hold_check_flag = True
                touch_start_cursor_index = cursor_index
            else:
                textinput.select_text(cursor_index, cursor_index)
                start = cursor_index
                end = cursor_index
                is_sliding = False
                is_hold_sliding = False
                hold_check_flag = False
            return True
        return False

    def on_touch_move(touch):
        nonlocal hold_check_flag, is_hold_sliding
        if hold_check_flag:
            if touch.time_start - start_touch_time < hold_check_time:
                if is_hold_sliding:
                    return
                dx = touch.x - start_touch_pos[0]
                dy = touch.y - start_touch_pos[1]
                if abs(dx) > 5 or abs(dy) > 5:
                    hold_check_flag = False
            else:
                hold_check_flag = False
                is_hold_sliding = True
        elif is_hold_sliding:
            return
        elif is_sliding:
            cursor_index = textinput.cursor_index()
            textinput.select_text(start, cursor_index)
            end = cursor_index
            textinput.selection_from = start
            textinput.selection_to = end
            textinput.selection_text = textinput.text[start:end]
        return False

    def on_touch_up(touch):
        nonlocal is_sliding, is_hold_sliding, hold_check_flag
        is_sliding = False
        is_hold_sliding = False
        hold_check_flag = False
        textinput.ctrl_start = None
        textinput.ctrl_end = None
        return False

    def on_mouse_pos(window, pos):
        nonlocal is_hold_sliding
        if is_hold_sliding:
            cursor_index = textinput.cursor_index()
            textinput.select_text(start, cursor_index)
            end = cursor_index
            textinput.selection_from = start
            textinput.selection_to = end
            textinput.selection_text = textinput.text[start:end]

    def on_double_tap(instance):
        start, end = _get_word_index()
        instance.select_text(start, end)
        textinput.selection_from = start
        textinput.selection_to = end
        textinput.selection_text = textinput.text[start:end]

    def on_cursor_index_change(instance, value):
        nonlocal start, end
        if not is_hold_sliding:
            if is_sliding:
                start = textinput.ctrl_start if textinput.ctrl and textinput.ctrl_start else value
                end = textinput.ctrl_end if textinput.ctrl and textinput.ctrl_end else value
            else:
                start = value
                end = value
        else:
            start = min(touch_start_cursor_index, value)
            end = max(touch_start_cursor_index, value)
        if end - start > 0:
            textinput.select_text(start, end)
            textinput.selection_from = start
            textinput.selection_to = end
            textinput.selection_text = textinput.text[start:end]

    def _is_touch_in_cursor_icon(cursor_index, line, col, line_height, x, y, is_end=False):
        if is_end:
            return (start <= cursor_index <= end and
                    y >= (line + 1) * line_height - cursor_icon_height / 2 and
                    y <= (line + 1) * line_height + cursor_icon_height / 2 and
                    x >= col * textinput.width / len(textinput.text) - cursor_icon_width / 2 and
                    x <= col * textinput.width / len(textinput.text) + cursor_icon_width / 2)
        else:
            return (start <= cursor_index <= end and
                    y >= line * line_height - cursor_icon_height / 2 and
                    y <= line * line_height + cursor_icon_height / 2 and
                    x >= col * textinput.width / len(textinput.text) - cursor_icon_width / 2 and
                    x <= col * textinput.width / len(textinput.text) + cursor_icon_width / 2)

    def _get_word_index():
        cursor_index = textinput.cursor_index()
        line_text = textinput.get_text()[textinput.cursor_row * textinput.width:textinput.cursor_row * textinput.width + textinput.width]
        match = re.search(r'\b\w*$', line_text[:cursor_index])
        left_word_end_index = cursor_index if not match else match.end()
        match = re.search(r'\w*\b', line_text[cursor_index:])
        right_word_start_index = cursor_index if not match else cursor_index + match.start()
        return left_word_end_index, right_word_start_index

    textinput.bind(
        on_touch_down=on_touch_down,
        on_touch_move=on_touch_move,
        on_touch_up=on_touch_up,
        on_double_tap=on_double_tap,
        cursor_index=on_cursor_index_change
    )
    Window.bind(mouse_pos=on_mouse_pos)