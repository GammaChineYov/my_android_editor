from android.content import Intent
from android.net import Uri
from ascript.android.system import R
from ascript.android.ui import Dialog
from java.util import ArrayList

class IntentHelper:
    def __init__(self, app_info,use_activity_index=0):
        self.use_activity_index = use_activity_index
        self.app_name = app_info["app_name"]
        self.package_name = app_info["package_name"]
        self.activitys = app_info["activitys"]

    def _create_intent(self, action):
        intent = Intent(action)
        intent.setPackage(self.package_name)
        intent.setClassName(self.package_name, self.activitys[self.use_activity_index])
        return intent

    def start_app(self):
        intent = self._create_intent("android.intent.action.VIEW")
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        R.context.startActivity(intent)
        
    def uri_from_file(self, file_path):
        file = File(file_path)
        return Uri.fromFile(file)

    def share_intent(self, text=None, file_path=None):
        if text and file_path:
            # 同时分享文本和文件
            share_intent = self._create_intent(Intent.ACTION_SEND)
            share_intent.putExtra(Intent.EXTRA_TEXT, text)
            share_intent.putExtra(Intent.EXTRA_STREAM, self.url_from_file(file_path))
            share_intent.setType("text/plain")
            share_intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            R.context.startActivity(share_intent)
        elif text:
            # 仅分享文本
            share_intent = self._create_intent(Intent.ACTION_SEND)
            share_intent.putExtra(Intent.EXTRA_TEXT, text)
            share_intent.setType("text/plain")
            share_intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            R.context.startActivity(share_intent)
        elif file_path:
            # 仅分享文件
            share_intent = self._create_intent(Intent.ACTION_SEND_MULTIPLE)
            l = ArrayList()
            l.add(file_path)
            share_intent.putParcelableArrayListExtra(Intent.EXTRA_STREAM, l)
            share_intent.setType("*/*")
            share_intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            R.context.startActivity(share_intent)