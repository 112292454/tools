def process_file(input_file, output_file):
    try:
        # 读取文件内容
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 去重并保持顺序
        unique_lines = list(dict.fromkeys(line.strip() for line in lines))

        # 写入输出文件，每行间隔一个空行
        with open(output_file, 'w', encoding='utf-8') as file:
            for line in unique_lines:
                file.write(line + '\n\n')  # 每行后面增加一个空行

        print(f"处理完成，结果已保存到 {output_file}")
    except FileNotFoundError:
        print(f"文件 {input_file} 未找到，请检查路径。")
    except Exception as e:
        print(f"发生错误：{e}")


# 示例调用
if __name__ == "__main__":
    input_file_path = "trackers.txt"  # 替换为你的输入文件路径
    output_file_path = "trackers_unique.txt"  # 替换为你的输出文件路径
    process_file(input_file_path, output_file_path)
