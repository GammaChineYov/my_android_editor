from flask import Flask, request, send_file, jsonify
import os
import zipfile
import psutil
import socket
from code_manage_utils import get_local_ip, extract_zip_to_directory, compress_directory_to_zip

app = Flask(__name__)

# 设置上传文件的存储目录
UPLOAD_FOLDER = 'uploads'
TEMP_DIR = ".temp.server"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
    
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["TEMP_DIR"] = TEMP_DIR

local_ip = get_local_ip()
if local_ip:
    print(f"服务器端绑定到局域网IP: {local_ip}")
else:
    print("无法获取服务器端局域网IP，将使用默认的127.0.0.1")
    local_ip = "127.0.0.1"


@app.route('/upload-directory', methods=['POST'])
def upload_directory():
    if 'directory' not in request.files:
        return jsonify({"error": "No directory part"}), 400

    directory_zip = request.files['directory']
    if directory_zip.filename == '':
        return jsonify({"error": "No selected directory"}), 400

    # 确保文件名安全，防止恶意文件名导致的问题
    filename = secure_filename(directory_zip.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    directory_zip.save(file_path)
    extract_zip_to_directory(file_path, os.path.dirname(file_path))
    os.remove(file_path)
    return jsonify({"message": "Directory uploaded and unzipped successfully"}), 200


@app.route('/download/<directory_name>', methods=['GET'])
def download_directory(directory_name):
    directory_path = os.path.join(app.config['UPLOAD_FOLDER'], directory_name)
    if not os.path.exists(directory_path):
        return jsonify({"error": "Directory not found"}), 404

    # 将目录压缩成zip包
    zip_file_path = compress_directory_to_zip(directory_path, app.config["TEMP_DIR"])
    

    return send_file(zip_file_path)


if __name__ == '__main__':
    from werkzeug.utils import secure_filename
    app.run(host=local_ip, debug=True)
