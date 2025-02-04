import os
import subprocess

import patoolib

PASSWORD_LIST = ['给我三连', 'password2', 'password3']  # 你的密码列表
input_dir = "/data/m50/shared/upload/三月兔/三月兔的动漫库/大佬角色分类（小）/【MANA】老师（漫画）/补漏"
# input_dir = "J://三月兔/三月兔的动漫库/大佬角色分类（小）/【Custom Udon乌冬】大佬/9月更新"


def extract_archive(archive_path, password=None):
    try:
        # 如果是分卷压缩文件，合并为一个压缩文件
        if archive_path.endswith('.001'):
            base_name = os.path.splitext(archive_path)[0]  # 获取文件名（去掉后缀）
            cat_command = f'cat "{base_name}."* > "{base_name}"'
            print("===================")
            print(cat_command)
            subprocess.run(cat_command, shell=True, check=True)
            archive_path = f"{base_name}"
    except subprocess.CalledProcessError as e:
        print(f"Failed to combine file {archive_path}: {e}")
        return False
    try:
        # 解压文件
        if password:
            command = f'unzip -P {password} -O gbk "{archive_path}"  -d "{os.path.dirname(archive_path)}"'
        else:
            command = f'unzip -O gbk "{archive_path}" -d "{os.path.dirname(archive_path)}"'
        print("===================")
        print(command)
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract {archive_path}: {e}")
        return False



def find_and_extract_archives(root_dir):
    processed_files = set()
    for root, dirs, files in os.walk(root_dir):
        files=sorted(files)
        for file in files:
            file_path = os.path.join(root, file)
            if is_archive(file_path) and file_path not in processed_files:
                print(f"Processing {file_path}...")
                processed_files.add(file_path)
                if "删我" in file:  # 删除文件名中的特定字符串
                    new_file_name = file.replace("删我", "")
                    os.rename(file_path, os.path.join(root, new_file_name))
                    file_path = os.path.join(root, new_file_name)
                if file.endswith('.001'):  # 如果是分卷压缩文件，只修改第一个文件的后缀名
                    header = read_file_header(file_path)
                    if header.startswith(b'PK'):
                        # 不做任何操作，保持后缀名不变
                        pass
                    base_name = os.path.splitext(file)[0]  # 去掉后缀
                    for i in range(2, 1000):  # 假设最多有999个分卷
                        next_part = f"{base_name}.{i:03d}"
                        if next_part in files:
                            files.remove(next_part)
                            # os.remove(os.path.join(root,next_part))
                else:
                    header = read_file_header(file_path)
                    if header.startswith(b'PK'):
                        os.rename(file_path, os.path.join(root, file.replace('.7z', '.zip')))
                extract_and_remove(file_path, processed_files)


def read_file_header(file_path, num_bytes=2):
    with open(file_path, 'rb') as f:
        return f.read(num_bytes)


def is_archive(file_path):
    return any(file_path.lower().count(extension) for extension in ['.zip', '.7z'])


def extract_and_remove(file_path, processed_files):
    for password in PASSWORD_LIST:
        if extract_archive(file_path, password=password):
            print(f"Successfully extracted {file_path}")
            extracted_size = get_directory_size(os.path.dirname(file_path))
            source_size = os.path.getsize(file_path)
            if extracted_size > source_size:
                print(f"Removing source file {file_path}")
                # os.remove(file_path)
            break



def get_directory_size(directory):
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size


def main():

    find_and_extract_archives(input_dir)


if __name__ == "__main__":
    main()
