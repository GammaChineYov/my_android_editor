import time
from ascript.android import media
import enum

class KeyCode(enum.Enum):
    VOLUME = 1
    VOLUME_DOWN = 2
    VOLUME_UP = 3
     
            
# 检测音量变化的函数
def _wait_volume_button_down(any_key=True, decreace=True):
    
    last_volume = media.get_volume()
    while True:
        time.sleep(0.3)
        new_volume = media.get_volume()
        if any_key and last_volume != new_volume:
            return True
        if decreace and last_volume > new_volume:
            return True
        elif not decreace and last_volume < new_volume:
            return True
        last_volume = new_volume
        
_key_func_list = (
(_wait_volume_button_down,),
(_wait_volume_button_down, (False, )),
(_wait_volume_button_down, (False, False)),
)
def wait_button_down(key_code: KeyCode):
        func_data = _key_func_list[key_code.value - 1]
        if len(func_data) == 1:
            return func_data[0]()
        elif len(func_data) == 2:
            return func_data[0](*func_data[1])
        elif len(func_data) == 3:
            return func_data[0](*func_data[1], **func_data[2])
        raise KeyError("超长列表，请联系开发人员")