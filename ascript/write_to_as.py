import os
from editor_helper import editor_helper as ehelper


def find_all_file_in_phone_storage(file_name):
    # 假设手机存储的根目录为 '/storage'
    root_directory = "/storage/emulated/0"
    for root, dirs, files in os.walk(root_directory):
        # 过滤掉隐藏文件夹（以点开头的文件夹）
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        if file_name in files:
            yield os.path.join(root, file_name)
    return None


dir = "/storage/emulated/0/airscript/model/MyHelper/"
path_map = {
    "src/": dir
}

if __name__ == "__main__":
    # for filepath in find_all_file_in_phone_storage("myhelper.py"):
    #    print(filepath)
    ehelper.stop_program()
    for source, target in path_map.items():
        content = ""
        if os.path.isfile(source):
            os.makedirs(os.path.dirname(source))
            with open(source, "r") as sf:
                content = sf.read()
            with open(target, "w") as f:
                f.write(content)
        elif os.path.isdir(source):
            for root, dirs, files in os.walk(source):
                # 过滤掉隐藏文件夹（以点开头的文件夹）和Python缓存文件夹（通常是__pycache__）
                dirs[:] = [d for d in dirs if not d.startswith('.') and d!= '__pycache__']
                filepaths = (os.path.join(root, file) for file in files)
                filepathmap = ((filepath, os.path.join(target, os.path.relpath(filepath, source))) for filepath in filepaths)
                for spath, tpath in filepathmap:
                    print(spath, tpath)
                    content = ""
                    os.makedirs(os.path.dirname(tpath), exist_ok=True)
                    with open(spath, "r") as f:
                        content = f.read()
                    with open(tpath, "w") as f:
                        f.write(content)
                    print(f"复制：{spath}\n\t到 {tpath}")
    ehelper.start_program(dir.strip("/").rsplit("/",1)[-1])