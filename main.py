

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
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QLabel, QFileDialog,
    QMessageBox, QGroupBox, QTableWidget, QTableWidgetItem, QSpinBox, QComboBox
)


class FileRenamerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("批量文件重命名工具")
        self.setGeometry(100, 100, 800, 600)

        # 初始化变量
        self.selected_files = []
        self.rename_rules = []

        # 创建主界面组件
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()

        # 文件选择区域
        self.create_file_selection_group()

        # 重命名规则区域
        self.create_rename_rules_group()

        # 预览区域
        self.create_preview_group()

        # 操作按钮
        self.create_action_buttons()

        self.main_widget.setLayout(self.layout)

    def create_file_selection_group(self):
        group = QGroupBox("文件选择")
        layout = QVBoxLayout()

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)

        btn_layout = QHBoxLayout()
        self.btn_add_files = QPushButton("添加文件")
        self.btn_add_files.clicked.connect(self.add_files)
        self.btn_clear = QPushButton("清空列表")
        self.btn_clear.clicked.connect(self.clear_files)

        btn_layout.addWidget(self.btn_add_files)
        btn_layout.addWidget(self.btn_clear)

        layout.addLayout(btn_layout)
        # 新增搜索框和按钮
        self.search_input = QLineEdit()
        self.search_btn = QPushButton("搜索")
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        self.search_btn.clicked.connect(self.filter_files)
        layout.addLayout(search_layout)
        layout.addWidget(self.file_list)
        group.setLayout(layout)
        self.layout.addWidget(group)

    def create_rename_rules_group(self):
        group = QGroupBox("重命名规则")
        layout = QVBoxLayout()

        # 正则表达式匹配
        self.regex_pattern_input = QLineEdit()
        self.regex_pattern_input.setPlaceholderText("输入正则表达式")

        # 查找替换
        self.find_text_input = QLineEdit()
        self.replace_text_input = QLineEdit()
        find_replace_layout = QHBoxLayout()
        find_replace_layout.addWidget(QLabel("查找:"))
        find_replace_layout.addWidget(self.find_text_input)
        find_replace_layout.addWidget(QLabel("替换为:"))
        find_replace_layout.addWidget(self.replace_text_input)

        # 删除字符
        self.delete_start_spin = self.create_spinbox("删除开头字符数", 0)
        self.delete_end_spin = self.create_spinbox("删除结尾字符数", 0)

        # 自动日期
        self.date_format_input = QLineEdit()
        self.date_format_input.setPlaceholderText("输入日期格式（如%Y-%m-%d）")

        # 编号设置
        self.start_num_spin = self.create_spinbox("起始序号", 1)
        self.step_spin = self.create_spinbox("步长", 1)

        # 扩展名处理
        self.extension_input = QLineEdit()
        self.extension_input.setPlaceholderText("输入新的扩展名")

        # 新增：大小写替换选项
        self.case_conversion_combo = QComboBox()
        self.case_conversion_combo.addItems(["无", "转为大写", "转为小写"])
        layout.addWidget(QLabel("大小写转换:"))
        layout.addWidget(self.case_conversion_combo)

        layout.addWidget(QLabel("正则表达式匹配:"))
        layout.addWidget(self.regex_pattern_input)
        layout.addWidget(QLabel("查找替换:"))
        layout.addLayout(find_replace_layout)
        layout.addWidget(QLabel("删除字符:"))
        layout.addLayout(self.delete_start_spin)
        layout.addLayout(self.delete_end_spin)
        layout.addWidget(QLabel("自动日期:"))
        layout.addWidget(self.date_format_input)
        layout.addWidget(QLabel("编号设置:"))
        layout.addLayout(self.start_num_spin)
        layout.addLayout(self.step_spin)
        layout.addWidget(QLabel("扩展名处理:"))
        layout.addWidget(self.extension_input)

        group.setLayout(layout)
        self.layout.addWidget(group)

    def create_preview_group(self):
        group = QGroupBox("预览")
        layout = QVBoxLayout()

        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(2)
        self.preview_table.setHorizontalHeaderLabels(["原文件名", "新文件名"])
        self.preview_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.preview_table)
        group.setLayout(layout)
        self.layout.addWidget(group)

    def create_action_buttons(self):
        btn_layout = QHBoxLayout()
        self.btn_preview = QPushButton("生成预览")
        self.btn_preview.clicked.connect(self.generate_preview)
        self.btn_apply = QPushButton("应用更改")
        self.btn_apply.clicked.connect(self.apply_renaming)

        # 新增：移动、删除、复制按钮
        self.btn_move = QPushButton("移动文件")
        self.btn_move.clicked.connect(self.move_files)
        self.btn_delete = QPushButton("删除文件")
        self.btn_delete.clicked.connect(self.delete_files)
        self.btn_copy = QPushButton("复制文件")
        self.btn_copy.clicked.connect(self.copy_files)

        btn_layout.addWidget(self.btn_preview)
        btn_layout.addWidget(self.btn_apply)
        btn_layout.addWidget(self.btn_move)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_copy)
        self.layout.addLayout(btn_layout)

    # 工具方法
    def create_spinbox(self, label, default):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        spin = QSpinBox()
        spin.setValue(default)
        layout.addWidget(spin)
        return layout

    # 文件操作
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择文件")
        if files:
            self.selected_files.extend(files)
            self.file_list.addItems(files)

    def clear_files(self):
        self.selected_files = []
        self.file_list.clear()
        self.preview_table.setRowCount(0)

    # 生成预览
    def generate_preview(self):
        self.preview_table.setRowCount(0)
        base_name = self.base_name_input.text()
        start_num = self.start_num_spin.itemAt(1).widget().value()
        step = self.step_spin.itemAt(1).widget().value()
        replace_from = self.replace_from.text()
        replace_to = self.replace_to.text()
        regex_pattern = self.regex_pattern_input.text()
        delete_start = self.delete_start_spin.itemAt(1).widget().value()
        delete_end = self.delete_end_spin.itemAt(1).widget().value()
        date_format = self.date_format_input.text()
        extension = self.extension_input.text()
        case_conversion = self.case_conversion_combo.currentText()

        current_num = start_num

        for i, file_path in enumerate(self.selected_files):
            original_name = os.path.basename(file_path)
            new_name = original_name

            # 应用正则表达式匹配
            if regex_pattern:
                import re
                new_name = re.sub(regex_pattern, '', new_name)

            # 应用查找替换规则
            if replace_from:
                new_name = new_name.replace(replace_from, replace_to)

            # 删除指定数量的开头和结尾字符
            new_name = new_name[delete_start:]  # 先处理开头删除
            if delete_end > 0:
                new_name = new_name[:-delete_end]  # 再处理结尾删除

            # 应用自动日期
            if date_format:
                from datetime import datetime
                new_name = f"{new_name}_{datetime.now().strftime(date_format)}"

            # 应用基础命名规则
            if base_name:
                ext = os.path.splitext(new_name)[1]
                new_base = base_name.replace("{n}", str(current_num))
                new_name = f"{new_base}{ext}"
                current_num += step

            # 应用扩展名处理
            if extension:
                new_name = os.path.splitext(new_name)[0] + "." + extension

            # 新增：应用大小写转换
            if case_conversion == "转为大写":
                new_name = new_name.upper()
            elif case_conversion == "转为小写":
                new_name = new_name.lower()

            self.preview_table.insertRow(i)
            self.preview_table.setItem(i, 0, QTableWidgetItem(original_name))
            self.preview_table.setItem(i, 1, QTableWidgetItem(new_name))

    # 应用更改
    def apply_renaming(self):
        if self.preview_table.rowCount() == 0:
            QMessageBox.warning(self, "警告", "请先生成预览!")
            return

        # 执行重命名
        success_count = 0
        errors = []

        for row in range(self.preview_table.rowCount()):
            original = self.preview_table.item(row, 0).text()
            new_name = self.preview_table.item(row, 1).text()

            # 查找原始文件路径
            original_path = next((f for f in self.selected_files if os.path.basename(f) == original), None)

            if original_path:
                try:
                    directory = os.path.dirname(original_path)
                    new_path = os.path.join(directory, new_name)

                    # 处理文件名冲突
                    counter = 1
                    while os.path.exists(new_path):
                        base, ext = os.path.splitext(new_name)
                        new_path = os.path.join(directory, f"{base} ({counter}){ext}")
                        counter += 1

                    shutil.move(original_path, new_path)
                    success_count += 1
                except Exception as e:
                    errors.append(f"重命名 {original} 失败: {str(e)}")

        # 显示结果
        result_msg = f"成功重命名 {success_count} 个文件"
        if errors:
            result_msg += f"\n\n错误:\n" + "\n".join(errors)
        QMessageBox.information(self, "完成", result_msg)

        # 清空数据
        self.clear_files()

    # 新增：移动文件功能
    def move_files(self):
        destination_dir = QFileDialog.getExistingDirectory(self, "选择目标文件夹")
        if not destination_dir:
            return

        success_count = 0
        errors = []

        for file_path in self.selected_files:
            try:
                shutil.move(file_path, destination_dir)
                success_count += 1
            except Exception as e:
                errors.append(f"移动 {file_path} 失败: {str(e)}")

        result_msg = f"成功移动 {success_count} 个文件"
        if errors:
            result_msg += f"\n\n错误:\n" + "\n".join(errors)
        QMessageBox.information(self, "完成", result_msg)

    # 新增：删除文件功能
    def delete_files(self):
        confirm = QMessageBox.question(self, "确认", "确定要删除选中的文件吗？", QMessageBox.Yes | QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return

        success_count = 0
        errors = []

        for file_path in self.selected_files:
            try:
                os.remove(file_path)
                success_count += 1
            except Exception as e:
                errors.append(f"删除 {file_path} 失败: {str(e)}")

        result_msg = f"成功删除 {success_count} 个文件"
        if errors:
            result_msg += f"\n\n错误:\n" + "\n".join(errors)
        QMessageBox.information(self, "完成", result_msg)

    # 新增：复制文件功能
    def copy_files(self):
        destination_dir = QFileDialog.getExistingDirectory(self, "选择目标文件夹")
        if not destination_dir:
            return

        success_count = 0
        errors = []

        for file_path in self.selected_files:
            try:
                shutil.copy(file_path, destination_dir)
                success_count += 1
            except Exception as e:
                errors.append(f"复制 {file_path} 失败: {str(e)}")

        result_msg = f"成功复制 {success_count} 个文件"
        if errors:
            result_msg += f"\n\n错误:\n" + "\n".join(errors)
        QMessageBox.information(self, "完成", result_msg)

    def filter_files(self):
        keyword = self.search_input.text().lower()
        self.file_list.clear()
        filtered_files = [f for f in self.selected_files if keyword in os.path.basename(f).lower()]
        self.file_list.addItems([os.path.basename(f) for f in filtered_files])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileRenamerApp()
    window.show()
    sys.exit(app.exec())
