import requests

# 基础URL，需根据实际情况修改
BASE_URL = "http://localhost:9096"

class EditorHelper:
    def __init__(self):
        self.session = requests.Session()

    def _send_request(self, endpoint, method="GET", data=None):
        url = BASE_URL + endpoint
        if method == "GET":
            response = self.session.get(url, params=data)
        elif method == "POST":
            response = self.session.post(url, json=data)
        else:
            raise ValueError("Invalid request method")

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}")

    def stop_program(self):
        """
        停止指定名称的小程序。

        Args:
            program_name (str): 要停止的小程序名称。

        Returns:
            dict: 包含操作结果信息的字典。
        """
        endpoint = f"/api/model/stop"
        return self._send_request(endpoint, method="GET")

    def start_program(self, program_name):
        """
        启动指定名称的小程序。

        Args:
            program_name (str): 要启动的小程序名称。

        Returns:
            dict: 包含操作结果信息的字典。
        """
        endpoint = f"/api/model/run"
        data = {"name": program_name}
        return self._send_request(endpoint, method="GET", data=data)

editor_helper = EditorHelper()

def main():
    editor = EditorHelper()

    # 启动小程序示例
    program_name_to_start = "MyHelper"
    try:
        start_result = editor.start_program(program_name_to_start)
        print(f"启动小程序 {program_name_to_start} 的结果: {start_result}")
    except Exception as e:
        print(f"启动小程序时出错: {e}")
    
    
    # 停止小程序示例
    program_name_to_stop = "MyHelper"
    try:
        stop_result = editor.stop_program()
        print(f"停止小程序 {program_name_to_stop} 的结果: {stop_result}")
    except Exception as e:
        print(f"停止小程序时出错: {e}")

if __name__ == "__main__":
    main()