## 仓库说明
参考：iizyd/SourceHanSansCN-TTF-Min，有需要别的字体可以自行链接下载https://github.com/iizyd/SourceHanSansCN-TTF-Min.git

## 仓库介绍
一、dist文件夹中已经是精简后的google Noto字体，可直接使用;源文件采用2024年更新的文件。
二、工具使用：
    1、需要准备好python环境，并安装fonttools-pyftsubset工具，pip install fonttools
    2、把源OTF文件放到脚本根目录，直接运行run_subset.bat
    3、脚本会自动根据content.txt文件中的内容进行压缩，并生成对应的TTF文件
