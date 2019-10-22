# -*- coding: utf-8 -*-
# @Time    : 2019/10/21 10:57
# @Author  : Akarrin
# @Github  : https://github.com/akarrin
# @FileName: ph_logo.py
# @Software: PyCharm

from PIL import Image, ImageDraw, ImageFont
import sys
from pathlib import  Path



LEFT_PART_VERTICAL_BLANK_MULTIPLY_FONT_HEIGHT = 2
LEFT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH = 1 / 4
RIGHT_PART_VERTICAL_BLANK_MULTIPLY_FONT_HEIGHT = 1
RIGHT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH = 1 / 4
RIGHT_PART_RADII = 10
BG_COLOR = '#000000'
BOX_COLOR = '#F7971D'
LEFT_TEXT_COLOR = '#FFFFFF'
RIGHT_TEXT_COLOR = '#000000'
FONT_SIZE = 50



def create_left_part_img(text: str, font_size: int):
    font = ImageFont.truetype('ArialEnUnicodeBold.ttf', font_size)
    font_width, font_height = font.getsize(text)
    offset_y = font.font.getsize(text)[1][1]
    blank_height = font_height * LEFT_PART_VERTICAL_BLANK_MULTIPLY_FONT_HEIGHT
    right_blank = int(font_width / len(text) * LEFT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH)
    img_height = font_height + offset_y + blank_height * 2
    image_width = font_width + right_blank
    image_size = image_width, img_height
    image = Image.new('RGBA', image_size, BG_COLOR)
    draw = ImageDraw.Draw(image)
    draw.text((0, blank_height), text, fill=LEFT_TEXT_COLOR, font=font)
    return image


def create_right_part_img(text: str, font_size: int):
    radii = RIGHT_PART_RADII
    font = ImageFont.truetype('ArialEnUnicodeBold.ttf', font_size)
    font_width, font_height = font.getsize(text)
    offset_y = font.font.getsize(text)[1][1]
    blank_height = font_height * RIGHT_PART_VERTICAL_BLANK_MULTIPLY_FONT_HEIGHT
    left_blank = int(font_width / len(text) * RIGHT_PART_HORIZONTAL_BLANK_MULTIPLY_FONT_WIDTH )
    image_width = font_width + 2 * left_blank
    image_height = font_height + offset_y + blank_height * 2
    image = Image.new('RGBA', (image_width, image_height), BOX_COLOR)
    draw = ImageDraw.Draw(image)
    draw.text((left_blank, blank_height), text, fill=RIGHT_TEXT_COLOR, font=font)

    # 圆
    magnify_time = 10
    magnified_radii = radii * magnify_time
    circle = Image.new('L', (magnified_radii * 2, magnified_radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, magnified_radii * 2, magnified_radii * 2), fill=255)  # 画白色圆形

    # 画4个角（将整圆分离为4个部分）
    magnified_alpha_width = image_width * magnify_time
    magnified_alpha_height = image_height * magnify_time
    alpha = Image.new('L', (magnified_alpha_width, magnified_alpha_height), 255)
    alpha.paste(circle.crop((0, 0, magnified_radii, magnified_radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((magnified_radii, 0, magnified_radii * 2, magnified_radii)),
                (magnified_alpha_width - magnified_radii, 0))  # 右上角
    alpha.paste(circle.crop((magnified_radii, magnified_radii, magnified_radii * 2, magnified_radii * 2)),
                (magnified_alpha_width - magnified_radii, magnified_alpha_height - magnified_radii))  # 右下角
    alpha.paste(circle.crop((0, magnified_radii, magnified_radii, magnified_radii * 2)),
                (0, magnified_alpha_height - magnified_radii))  # 左下角
    alpha = alpha.resize((image_width, image_height), Image.ANTIALIAS)
    image.putalpha(alpha)
    return image


def combine_img(left_text:str, right_text, font_size:int, out_put_path:str):
    left_img = create_left_part_img(left_text, font_size)
    right_img = create_right_part_img(right_text, font_size)
    blank = 30
    bg_img_width = left_img.width + right_img.width + blank * 2
    bg_img_height = left_img.height
    bg_img = Image.new('RGBA', (bg_img_width, bg_img_height), BG_COLOR)
    bg_img.paste(left_img, (blank, 0))
    bg_img.paste(right_img, (blank + left_img.width, int((bg_img_height - right_img.height) / 2)), mask=right_img)
    bg_img.save(out_put_path)


def make_ph_style_logo():
    input_params_nums = len(sys.argv)
    if input_params_nums == 1:
        print("请输入需要转换为p**n h*b风格的文本,如'Bilibili 舞蹈区'")
    elif input_params_nums == 2:
        print("请用空格分开文本,如'Bilibili 舞蹈区'")
    elif input_params_nums == 3:
        left_text = sys.argv[1]
        right_text = sys.argv[2]
        img_name = f'{left_text} {right_text}.png'
        out_put_path = str(Path.home() / 'Desktop' / img_name)
        combine_img(left_text, right_text, FONT_SIZE, out_put_path)
        print(f"已成功导出至{out_put_path}")
    else:
        print("只能输入空格隔开的两端文本")

if __name__ == "__main__":
    make_ph_style_logo()