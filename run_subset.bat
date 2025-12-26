@echo off
echo 正在安装 FontTools...
pip install fonttools

echo.
echo 正在开始字体压缩...
python subset_fonts.py

pause