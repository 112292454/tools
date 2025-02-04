import os
import sys
import subprocess

def extract_files(path):
    extracted_files = []
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.zip') or file.endswith('.7z') or file.endswith('.rar'):
                    extracted_files.append(os.path.join(root, file))
    elif os.path.isfile(path) and (path.endswith('.zip') or path.endswith('.7z') or path.endswith('.rar')):
        extracted_files.append(path)

    return extracted_files

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_folder_or_file> [additional_arguments...]\n"
              "And the additional arguments are exactly same as the 7z program"
              "Example: python script.py /path/to/folder -pav783661 '-xr!*.url'  '-xr!*.txt'")
        sys.exit(1)

    path = sys.argv[1]
    extracted_files = extract_files(path)

    for file_path in extracted_files:
        dirname = os.path.splitext(file_path)[0]
        if os.path.exists(dirname):
            print(f"Directory {dirname} already exists. Skipping extraction.")
            continue

        os.makedirs(dirname)
        command = ['7z', 'x', file_path, f"-o{dirname}"] + sys.argv[2:]
        subprocess.run(command)
# print("example: \n\npython ~/unzip.py  ./黑丝御姐骑乘-vid99gkozlu.rar -pav783661 '-xr!*.url'  '-xr!*.txt'  ")
if __name__ == "__main__":
    main()
