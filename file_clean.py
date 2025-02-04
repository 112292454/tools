import os
import re

def rename_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # 获取文件名（不包含扩展名）
            base_name = os.path.splitext(file_name)[0]
            need_include_folder_name=False
            if re.match("^[0-9]+$", base_name):
                # 纯数字
                need_include_folder_name=True
            elif re.match("^[a-zA-Z]+$", base_name):
                # 纯字母
                need_include_folder_name=True
            elif re.match("^[a-zA-Z0-9]+$", base_name):
                need_include_folder_name=True

            # 判断文件名是否是纯数字
            if need_include_folder_name:
                # 获取文件夹名
                folder_name = os.path.basename(root)

                # 构建新的文件名
                new_name = os.path.join(root, folder_name+'---' + base_name)

                # 重命名文件
                os.rename(file_path, new_name)
                print(f'Renamed: {file_path} -> {new_name}')


def add_default_suffix(folder_path, suffix):
    if not suffix.startswith('.'):
        suffix = '.' + suffix
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # 检查是否没有文件扩展名
            if '.' not in file_name:
                # 构建新的文件名（加上指定的后缀名）
                new_name = os.path.join(root, f"{file_name}{suffix}")

                # 重命名文件
                os.rename(file_path, new_name)
                print(f'Renamed: {file_path} -> {new_name}')


def replace_suffix(folder_path, old_suffix, new_suffix):
    if not old_suffix.startswith('.'):
        old_suffix = '.' + old_suffix
    if not new_suffix.startswith('.'):
        new_suffix = '.' + new_suffix

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # 检查文件是否以指定的后缀名结尾
            if file_name.endswith(old_suffix):
                # 构建新的文件名
                new_name = os.path.join(root, file_name.rsplit(old_suffix, 1)[0] + new_suffix)

                # 重命名文件
                os.rename(file_path, new_name)
                print(f'Renamed: {file_path} -> {new_name}')


def extensions_to_lowercase(folder_path):
    unique_uppercase_extensions = set()

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # 获取文件的扩展名
            _, extension = os.path.splitext(file_name)

            # 检查扩展名是否包含大写字母
            if any(char.isupper() for char in extension):
                # 将大写扩展名添加到集合中
                unique_uppercase_extensions.add(extension)

    # 遍历大写扩展名集合，逐个替换为小写形式
    for old_suffix in unique_uppercase_extensions:
        new_suffix = old_suffix.lower()
        replace_suffix(folder_path, old_suffix, new_suffix)

def truncate_filenames(folder_path, max_bytes=250):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 判断是否为文件
        if os.path.isfile(file_path):
            # 获取文件后缀名
            _, file_extension = os.path.splitext(filename)

            # 获取文件名的字节数
            filename_bytes = filename.encode('utf-8')

            # 判断文件名字节数是否超过限制
            if len(filename_bytes) > max_bytes:
                # 截断文件名，保留前max_bytes个字节
                truncated_filename_bytes = filename_bytes[:max_bytes]

                # 解码为字符串
                truncated_filename = truncated_filename_bytes.decode('utf-8', 'ignore')

                # 构造新的文件名
                new_filename = truncated_filename + file_extension

                # 构造新的文件路径
                new_file_path = os.path.join(folder_path, new_filename)

                # 重命名文件
                os.rename(file_path, new_file_path)
                print(f"Renamed: {filename} to {new_filename}")


def remove_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        # 遍历文件夹，从底层向上删除空文件夹
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
                print(f'Removed empty folder: {folder_path}')