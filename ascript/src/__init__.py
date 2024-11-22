import sys
import os
import time 
import json

from ascript.android.system import Clipboard, R
sys.path.append(R.root())

import platforms
from platforms.android import input
from ascript_utils import toast
from ascript.android.node import Selector
from intent_helper import IntentHelper
from core.models import DeviceRunningInfo, AppInstallInfo
from core.component_manager import component_manager


toast("基础模块加载完成")
dir = "/storage/emulated/0/airscript/model/MyHelper/"
filedir = "/storage/emulated/0/我的文档/vivo文档/"
docs_filepath = "/storage/emulated/0/我的文档/vivo文档/for_ai.txt"

apps = AppInstallInfo.load_installed_apps()


toast("程序已启动")
while input.wait_button_down(input.KeyCode.VOLUME):
    runtime_info = DeviceRunningInfo.get_running_app_info()
    str_runtime_info = str(runtime_info)
    app_install_info = [item for item in apps if item.package_name == runtime_info.package_name]
    str_info2 = str(app_install_info)
    toast(str_runtime_info + str_info2)
    
    Clipboard.put(str_runtime_info+str_info2)
    res = Selector.dump()
    res = json.dumps(json.loads(res),indent=4, ensure_ascii=False)
    page_filepath = filedir+("cur_page_info.json")
    with open(page_filepath, "w") as f:
        f.write(res)
    
    
    time.sleep(0.1)