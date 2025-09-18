# HM-WaterFall

一个基于Python的图片水印添加工具，可以自动从图片的EXIF信息中提取拍摄时间，并将其作为水印添加到图片上。

## 功能特点

- 自动读取图片EXIF信息中的拍摄时间
- 支持自定义水印的字体大小、颜色和位置
- 批量处理目录中的所有图片
- 将处理后的图片保存到新目录中

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python watermark_adder.py <图片目录路径> [选项]
```

### 选项

- `--font_size`: 字体大小 (默认: 20)
- `--font_color`: 字体颜色RGB值 (默认: 255 255 255)
- `--position`: 水印位置 (默认: bottom_right)
  - 可选值: top_left, top_center, top_right, center, bottom_left, bottom_center, bottom_right

### 示例

```bash
# 基本使用
python watermark_adder.py /path/to/images

# 自定义字体大小和颜色
python watermark_adder.py /path/to/images --font_size 30 --font_color 255 0 0

# 更改水印位置
python watermark_adder.py /path/to/images --position top_left
```

## 输出

处理后的图片将保存在原目录下的`<目录名>_watermark`子目录中。