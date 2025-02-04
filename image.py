from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def convert_png_to_jpg(png_path, jpg_path, quality=82):
    try:
        # 打开PNG图像
        image = Image.open(png_path)

        # 转换为RGB模式（如果PNG是RGBA模式）
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # 保存为JPG图像
        image.save(jpg_path, 'JPEG', quality=quality)
        print(f"成功将 {png_path} 转换为 {jpg_path}，画质压缩级别: {quality}")
    except Exception as e:
        print(f"转换失败: {str(e)}")


from PIL import Image

def crop_image(image_path, output_path,l,r,u,b ):
    try:
        # 打开图像
        image = Image.open(image_path)

        # 获取图像的宽度和高度
        width, height = image.size

        # 计算裁剪的区域
        left=width*l
        right = width*r
        top=height*u
        bottom = height*b

        # right = width - width // 3  # 右1/3
        # bottom = height - height // 6  # 下5/6

        # 裁剪图像
        cropped_image = image.crop((left, top, right, bottom))

        # 保存裁剪后的图像
        cropped_image.save(output_path)
        print(f"成功裁剪图像并保存到：{output_path}")
    except Exception as e:
        print(f"裁剪图像失败：{str(e)}")


# 使用示例
png_path = './xyz_grid-0000-56456.png'  # 输入的PNG图像路径
jpg_path = './xyz_grid-0000-56456.jpg'  # 输出的JPG图像路径
jpg_edit_path = './xyz_grid-0000-56456-edited.jpg'  # 输出的JPG图像路径

quality = 82  # 自定义的画质压缩级别（0-100，100为最高质量）

# convert_png_to_jpg(png_path, jpg_path, quality)

crop_image(jpg_path, jpg_edit_path,0.66,1,0.2,1)