import os
import sys
import subprocess

process_type=['jpg','png']

def compress_image(input_file, output_file, max_long_edge, compression_level):
    ffmpeg_command = (f"ffmpeg -loglevel error -threads 16 -y -i '{input_file}' -vf 'scale=w=if(gte(iw\,ih)\,min(iw\,{max_long_edge})\,-1):h=if(gte(iw\,ih)\,-1\,min(ih\,{max_long_edge})):flags=lanczos' "
                      f"-pix_fmt yuvj420p -color_range tv -qmin 1 -q:v {compression_level} '{output_file}'")
    subprocess.run(ffmpeg_command, shell=True)

def compress_images_in_directory(input_dir, max_long_edge, compression_level):
    if not os.path.isdir(input_dir):
        compress_image(input_dir, input_dir.replace('png', 'jpg'), max_long_edge, compression_level)
        return

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.jpg') or file.lower().endswith('.png'):
                input_path = os.path.join(root, file)
                print('Processing \t '+input_path)
                compress_image(input_path, input_path.replace('png','jpg'), max_long_edge, compression_level)

max_long_edge=5000

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compress_images.py input_dir max_long_edge")
        sys.exit(1)
    elif len(sys.argv) < 3:
        print("Usage: python compress_images.py input_dir [max_long_edge=5000pixel]")
        # sys.exit(1)
    else:
        max_long_edge = int(sys.argv[2])

    input_dir = sys.argv[1]
    compression_level = 2

    compress_images_in_directory(input_dir, max_long_edge, compression_level)

    print("图片压缩完成")