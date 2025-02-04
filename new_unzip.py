import os
import subprocess

PASSWORD_LIST = ['给我三连', 'password2', 'password3']  # 你的密码列表
input_dir = "/data/m50/shared/upload/三月兔/三月兔的动漫库/大佬角色分类（小）/【YESUI】老师/"


def remove_specific_strings(file_path, specific_strings):
    new_file_path = file_path
    for specific_string in specific_strings:
        if specific_string in new_file_path:
            new_file_path = new_file_path.replace(specific_string, "")
    if new_file_path != file_path:
        os.rename(file_path, new_file_path)
        return new_file_path
    return file_path

def concatenate_split_files(archive):
    base_name, ext = os.path.splitext(archive)
    output_file = base_name + "_concatenated" + ext

    with open(output_file, 'wb') as outfile:
        part_num = 1
        while True:
            part_file = f"{base_name}.{part_num:03d}"
            if os.path.exists(part_file):
                with open(part_file, 'rb') as infile:
                    outfile.write(infile.read())
                part_num += 1
            else:
                break

    return output_file
def merge_split_archives(dir):
    os.chdir(dir)
    split_archives = [file for file in os.listdir('.') if file.endswith('.001')]
    for archive in split_archives:
        base_name = os.path.splitext(archive)[0]  # 获取文件名（去掉后缀）
        # cat_command = f'cat "{base_name}."* > "{base_name}"'
        # print(cat_command)
        try:
            concatenate_split_files(archive)
            # subprocess.run(cat_command, shell=True, check=True)
            for part_file in os.listdir("."):
                if part_file.startswith(base_name) and part_file != f"{base_name}":
                    # os.remove(part_file)
                    pass
        except subprocess.CalledProcessError as e:
            print(f"Failed to merge split archives: {e}")


def extract_all_archives(dir):
    os.chdir(dir)
    archives = [file for file in os.listdir(".") if file.lower().endswith(('.zip', '.7z'))]
    for archive in archives:
        if not extract_archive(archive):
            print(f"Failed to extract {archive}")


def extract_archive(archive_path):
    for password in PASSWORD_LIST:
        try:
            if password:
                command = f'unzip -P {password} "{archive_path}" -d "{os.path.dirname(archive_path)}"'
            else:
                command = f'unzip "{archive_path}" -d "{os.path.dirname(archive_path)}"'
            subprocess.run(command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            pass
    print(f"Failed to extract {archive_path}: Password required.")
    return False


def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # 删除文件名中的特定字符串
            specific_strings = ["删我", "删除"]
            new_file_path = remove_specific_strings(file_path, specific_strings)
            if new_file_path != file_path:
                print(f"Renamed {file_path} to {new_file_path}")
        # 合并分卷压缩文件
        merge_split_archives(root)

        # 解压所有压缩文件
        # extract_all_archives(root)

            # # 删除所有压缩文件
            # archives = [file for file in os.listdir(root) if file.lower().endswith(('.zip', '.7z'))]
            # for archive in archives:
            #     os.remove(os.path.join(root, archive))


def main():
    process_directory(input_dir)


if __name__ == "__main__":
    main()
