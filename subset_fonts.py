#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from fontTools.ttLib import TTFont

# 源字体目录和目标输出目录
SRC_ROOT = "."
DIST_ROOT = "./dist"

# 字符集文件路径
CONTENT_FILE = "./content.txt"

def convert_to_ttf(input_path, output_path):
    """将字体文件转换为TTF格式"""
    try:
        font = TTFont(input_path)
        font.save(output_path)
        font.close()
        return True
    except Exception as e:
        print(f"❌ 转换为TTF失败: {e}")
        return False

def subset_fonts():
    # 创建目标目录
    dist_dir = Path(DIST_ROOT)
    dist_dir.mkdir(exist_ok=True)
    
    # 获取当前目录下的所有 .otf 和 .ttf 字体文件
    font_files = []
    for ext in ["*.otf", "*.ttf"]:
        font_files.extend(Path(SRC_ROOT).glob(ext))
    
    if not font_files:
        print("❌ 未找到任何字体文件")
        return
    
    print(f"找到 {len(font_files)} 个字体文件")
    
    for font_file in font_files:
        # 获取字体文件名（不含扩展名）
        file_name = font_file.stem
        original_ext = font_file.suffix.lower()
        
        # 压缩后的字体文件路径（保持原格式）
        compressed_output = dist_dir / font_file.name
        
        print(f"正在压缩字体: {font_file.name}")
        
        # 使用 pyftsubset 命令压缩字体
        cmd = [
            "pyftsubset",
            str(font_file),
            f"--text-file={CONTENT_FILE}",
            f"--output-file={compressed_output}"
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✅ 成功生成压缩字体: {compressed_output}")
            
            # 检查输出文件大小
            if compressed_output.exists():
                original_size = font_file.stat().st_size
                new_size = compressed_output.stat().st_size
                print(f"   原始大小: {original_size / 1024 / 1024:.2f} MB")
                print(f"   压缩后大小: {new_size / 1024 / 1024:.2f} MB")
                print(f"   压缩率: {(1 - new_size / original_size) * 100:.2f}%")
                
                # 将压缩后的字体转换为TTF格式
                ttf_output = dist_dir / f"{file_name}.ttf"
                print(f"正在转换为TTF格式: {file_name}.ttf")
                
                if convert_to_ttf(compressed_output, ttf_output):
                    # 检查TTF文件大小
                    if ttf_output.exists():
                        ttf_size = ttf_output.stat().st_size
                        print(f"✅ 成功生成TTF字体: {ttf_output}")
                        print(f"   TTF大小: {ttf_size / 1024 / 1024:.2f} MB")
                else:
                    print(f"❌ 转换TTF失败: {file_name}.ttf")
                    
        except subprocess.CalledProcessError as e:
            print(f"❌ 压缩字体 {font_file.name} 失败: {e}")
            if e.stderr:
                print(f"   错误信息: {e.stderr}")
        except FileNotFoundError:
            print("❌ 未找到 pyftsubset 命令。请确保已安装 fonttools: pip install fonttools")
            return
    
    print(f"✅ 所有字体处理完成，已保存至 {DIST_ROOT} 目录。")

if __name__ == "__main__":
    subset_fonts()