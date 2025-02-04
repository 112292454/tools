import os
import chardet
from shutil import copy2
from codecs import open as codecs_open

def detect_and_convert_to_utf8(file_path, backup_folder):
    try:
        # 读取文件内容并检测编码
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)

        # 获取检测到的编码
        detected_encoding = result['encoding']

        # 如果检测到的编码不是 UTF-8，则进行转换
        if detected_encoding and detected_encoding.lower() != 'utf-8':
            # 读取文件内容并以检测到的编码解码
            with codecs_open(file_path, 'r', detected_encoding, errors='ignore') as f:
                content = f.read()

            # 将内容以 UTF-8 编码写回文件
            with codecs_open(file_path, 'w', 'utf-8') as f:
                f.write(content)

            print(f'Converted: {file_path} from {detected_encoding} to utf-8')

    except Exception as e:
        print(f'Error processing {file_path}: {e}')
        # 复制有问题的文件到备份文件夹
        backup_file_path = os.path.join(backup_folder+'/errors', os.path.basename(file_path))
        copy2(file_path, backup_file_path)
        print(f'Backed up: {file_path} -> {backup_file_path}')

def detect_and_convert_folder(folder_path, backup_folder):
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    if not os.path.exists(backup_folder+'/errors'):
        os.makedirs(backup_folder+'/errors')
    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # 只处理文本文件
            if file_name.lower().endswith(('.txt', '.md', '.csv', '.py', '.html', '.xml')):
                detect_and_convert_to_utf8(file_path, backup_folder)

