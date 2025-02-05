import os
import re
import shutil


#   重命名文件夹中的文件
def rename_files_in_folder(folder_path):
    """
    重命名指定文件夹中的文件，将文件名前面加上文件夹名。处理类似多个文件夹里面都有1.jpg，2.jpg，3.jpg这种文件名。
    （对于1/1.jpg，2/1.jpg这种文件名没法救）
    :param folder_path:
    :return:
    """
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
                # 字母和数字
                need_include_folder_name=True
            #如果文件名已经包含了文件夹名，则不重命名.即，不处理1/1.jpg，2/1.jpg这种文件名——这种也只能把时间戳写到文件名。
            if file_name.startswith(os.path.basename(root)):
                need_include_folder_name=False

            # 判断文件名是否是纯数字
            if need_include_folder_name:
                # 获取文件夹名
                folder_name = os.path.basename(root)

                # 构建新的文件名
                target_base_name = folder_name + '---' + base_name

                new_name = os.path.join(root, target_base_name)

                # 重命名文件
                os.rename(file_path, new_name)
                print(f'Renamed: {file_path} -> {new_name}')


# 为文件夹中没有扩展名的文件添加默认后缀名
def add_default_suffix(folder_path, suffix):
    """
    为指定文件夹中没有扩展名的文件添加默认后缀名。用于对已知类型的文件进行标记。
    :param folder_path:
    :param suffix:
    :return:
    """
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


# 替换文件夹中的指定后缀名
def replace_suffix(folder_path, old_suffix, new_suffix):
    """
    替换指定文件夹中的指定后缀名。
    :param folder_path: 路径
    :param old_suffix: 要替换的后缀名
    :param new_suffix: 目标后缀名
    :return:
    """
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

# 将文件夹中的大写扩展名转换为小写
def extensions_to_lowercase(folder_path):
    """
    将指定文件夹中的大写扩展名转换为小写。
    :param folder_path:
    :return:
    """
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

# 截断文件名
def truncate_filenames(folder_path, max_bytes=250):
    """
    截断指定文件夹中文件名的字节数，用于处理一些系统上对文件名/路径名长度有限制的问题。
    :param folder_path:
    :param max_bytes:
    :return:
    """
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

# 删除空文件夹
def remove_empty_folders(folder_path):
    """
    删除指定文件夹中的空文件夹。
    :param folder_path:
    :return:
    """
    for root, dirs, files in os.walk(folder_path, topdown=False):
        # 遍历文件夹，从底层向上删除空文件夹
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
                print(f'Removed empty folder: {folder_path}')


def clean_multi_layer_path(folder_path):
    """
    处理指定文件夹中的无意义多层路径：如果某个文件夹中只有一个子文件夹，并且该子文件夹含有文件或其他文件夹，
    则将子文件夹中的内容移动到父文件夹中，并删除该子文件夹。
    :param folder_path: 目标文件夹路径
    :return: None
    """
    """
    效果类似：
    >tree /f
    
    D:.                                         D:.                    
    ├─新建文件夹                                     ├─新建文件夹                        
    │  └─a                                         │      新建文本文档.txt                       
    │          新建文本文档.txt                      │                                      
    │                                              ├─新建文件夹 (2)                  
    ├─新建文件夹 (2)                                 ├─新建文件夹 - 副本                            
    ├─新建文件夹 - 副本                  =》          │  │  新建文本文档.txt                             
    │  │  新建文本文档.txt                           │  │                                 
    │  │                                           │  └─a                     
    │  └─a                                         │          新建文本文档.txt                       
    │          新建文本文档.txt                      │                                      
    │                                              └─新建文件夹 - 副本 (2)                  
    └─新建文件夹 - 副本 (2)                                   新建文本文档.txt                                 
            新建文本文档.txt                                                             

    """
    for root, dirs, files in os.walk(folder_path, topdown=False):
        # 如果当前目录只有一个子文件夹且没有文件，且子文件夹非空
        if len(dirs) == 1 and len(files) == 0:
            sub_folder = dirs[0]
            sub_folder_path = os.path.join(root, sub_folder)

            # 检查子文件夹是否为空
            if os.path.exists(sub_folder_path) and os.listdir(sub_folder_path):
                # 将子文件夹中的所有内容移动到当前目录
                for item in os.listdir(sub_folder_path):
                    item_path = os.path.join(sub_folder_path, item)
                    new_item_path = os.path.join(root, item)

                    # 如果是文件，则直接移动
                    if os.path.isfile(item_path):
                        shutil.move(item_path, new_item_path)
                        print(f'Moved file: {item_path} -> {new_item_path}')
                    # 如果是文件夹，则递归移动文件夹内容
                    elif os.path.isdir(item_path):
                        shutil.move(item_path, new_item_path)
                        print(f'Moved folder: {item_path} -> {new_item_path}')

                # 删除空的子文件夹
                os.rmdir(sub_folder_path)
                print(f'Removed empty folder: {sub_folder_path}')
