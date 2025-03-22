"""
批量文件重命名工具

用于批量替换文件名中的指定字符。
支持预览修改结果和实际执行重命名操作。

Author: littleED090
Date: 2025/03/22
Version: 2.0.0

主要功能：
- 交互式文件夹选择
- 字符串替换预览功能
- 批量重命名执行
- 操作日志记录
- 错误处理与提示

依赖库：
- PySide6
- os 标准库


"""
import sys
import os
import shutil
from PySide6.QtWidgets import QApplication
from ui_components import FileRenamerApp

if __name__ == "__main__":
    app = QApplication([])
    window = FileRenamerApp()
    window.show()
    app.exec()
