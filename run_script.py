import os

def run_script_with_logging(script_path):
    print(f"Checking path for script: {script_path}")
    src_path = get_src_path(script_path)
    if not src_path:
        raise ValueError(f"Could not find src path for {script_path}")
    print(f"Found src path: {src_path}")

    # 直接运行脚本
    command = f'python {script_path}'
    with os.popen(command) as pipe:
        while True:
            output = pipe.readline()
            if output == '' and pipe.close():
                break
            if output:
                print(output.strip())

def get_src_path(file_path):
    absolute_path = os.path.abspath(file_path)
    src_index = absolute_path.find('/src/')
    if src_index!= -1:
        return absolute_path[:src_index + 4]
    else:
        return None

if __name__ == "__main__":
    run_script_with_logging('src/example/example_textinput_cursor.py')