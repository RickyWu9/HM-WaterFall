#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图片水印添加工具
根据PRD要求实现以下功能：
1. 读取指定目录下所有图片的EXIF信息中的拍摄时间
2. 将拍摄时间作为水印文本添加到图片上
3. 支持自定义水印的字体大小、颜色和位置
4. 将添加水印后的图片保存到新目录中
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import piexif
from datetime import datetime
import argparse


def get_exif_date(image_path):
    """
    从图片的EXIF信息中提取拍摄日期
    """
    try:
        exif_dict = piexif.load(image_path)
        if 'Exif' in exif_dict:
            # 查找日期时间标签
            for tag in ['DateTimeOriginal', 'DateTime']:
                if piexif.ExifIFD[tag] in exif_dict['Exif']:
                    date_str = exif_dict['Exif'][piexif.ExifIFD[tag]].decode('utf-8')
                    # 解析日期字符串并返回YYYY-MM-DD格式
                    dt = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    return dt.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"读取{image_path}的EXIF信息时出错: {e}")
    return None


def add_watermark(image_path, output_path, watermark_text, font_size=20, 
                  font_color=(255, 255, 255), position='bottom_right'):
    """
    在图片上添加水印
    """
    try:
        # 打开图片
        image = Image.open(image_path)
        
        # 创建绘图对象
        draw = ImageDraw.Draw(image)
        
        # 设置字体
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # 如果无法加载指定字体，则使用默认字体
            font = ImageFont.load_default()
        
        # 获取文本尺寸
        text_width, text_height = draw.textsize(watermark_text, font=font)
        
        # 根据位置参数计算水印位置
        image_width, image_height = image.size
        
        if position == 'top_left':
            x, y = 10, 10
        elif position == 'top_center':
            x, y = (image_width - text_width) // 2, 10
        elif position == 'top_right':
            x, y = image_width - text_width - 10, 10
        elif position == 'center':
            x, y = (image_width - text_width) // 2, (image_height - text_height) // 2
        elif position == 'bottom_left':
            x, y = 10, image_height - text_height - 10
        elif position == 'bottom_center':
            x, y = (image_width - text_width) // 2, image_height - text_height - 10
        else:  # 默认为右下角
            x, y = image_width - text_width - 10, image_height - text_height - 10
        
        # 绘制水印
        draw.text((x, y), watermark_text, font=font, fill=font_color)
        
        # 保存图片
        image.save(output_path)
        print(f"已为{image_path}添加水印并保存到{output_path}")
        
    except Exception as e:
        print(f"处理图片{image_path}时出错: {e}")


def process_images_in_directory(input_dir, font_size=20, font_color=(255, 255, 255), 
                               position='bottom_right'):
    """
    处理目录中的所有图片
    """
    # 支持的图片格式
    supported_formats = ('.jpg', '.jpeg', '.png')
    
    # 创建输出目录
    output_dir = os.path.join(input_dir, f"{os.path.basename(input_dir)}_watermark")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 遍历目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            # 获取水印文本（拍摄日期）
            watermark_text = get_exif_date(input_path)
            
            if watermark_text:
                add_watermark(input_path, output_path, watermark_text, 
                            font_size, font_color, position)
            else:
                print(f"无法从{filename}中提取拍摄日期，跳过处理")


def main():
    parser = argparse.ArgumentParser(description='为图片添加基于拍摄时间的水印')
    parser.add_argument('input_dir', help='包含图片的目录路径')
    parser.add_argument('--font_size', type=int, default=20, help='字体大小 (默认: 20)')
    parser.add_argument('--font_color', nargs=3, type=int, default=[255, 255, 255], 
                       help='字体颜色RGB值 (默认: 255 255 255)')
    parser.add_argument('--position', choices=['top_left', 'top_center', 'top_right', 
                                              'center', 'bottom_left', 'bottom_center', 'bottom_right'], 
                       default='bottom_right', help='水印位置 (默认: bottom_right)')
    
    args = parser.parse_args()
    
    # 检查输入目录是否存在
    if not os.path.isdir(args.input_dir):
        print(f"错误: 目录 {args.input_dir} 不存在")
        sys.exit(1)
    
    # 处理图片
    process_images_in_directory(
        args.input_dir, 
        args.font_size, 
        tuple(args.font_color), 
        args.position
    )

if __name__ == "__main__":
    main()