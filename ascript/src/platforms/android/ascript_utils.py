from ascript.android.ui import Dialog
import time as _time
from ascript.android.system import KeyValue
from utils import SingletonMeta
import json

_toast_calls = []
def toast(*args, delay=5000):
    global _toast_calls
    current_time = _time.strftime("%H:%M:%S", _time.localtime())
    data = " ".join([current_time, ":"] +[str(item) for item in args])
    now = _time.time()
    _toast_calls = [(d, t, dl) for d,t,dl in _toast_calls if (now - t) < dl/1000]
    _toast_calls.append((data, now, delay))
    Dialog.toast("\n".join([d for d,_,_ in _toast_calls]))

def promt(*args):
    
    return False
    
class Config(metaclass=SingletonMeta):
    def __init__(self):
        pass
        
    @property
    def config_dict(self):
        return json.loads(KeyValue.get("config_dict", "{}"))
    @config_dict.setter
    def config_dict(self, value):
        KeyValue.save("config_dict", json.dumps(value))
        
    def get(self, key, default_value=None):
        
        return self.config_dict.get(key, default_value)
    
    def save(self, key, value):
        config_dict = self.config_dict
        config_dict[key] = value
        self.config_dict= config_dict

    
    