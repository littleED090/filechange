from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QLineEdit, QLabel, QFileDialog, QMessageBox, QGroupBox, QTableWidget,
    QTableWidgetItem, QSpinBox, QComboBox
)
from file_operations import FileOperations
from rename_logic import RenameLogic

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
        self.btn_add_folder = QPushButton("添加文件夹")
        self.btn_add_folder.clicked.connect(self.add_folder)
        self.btn_clear = QPushButton("清空列表")
        self.btn_clear.clicked.connect(self.clear_files)

        btn_layout.addWidget(self.btn_add_files)
        btn_layout.addWidget(self.btn_add_folder)
        btn_layout.addWidget(self.btn_clear)

        layout.addLayout(btn_layout)
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

        self.base_name_input = QLineEdit()
        self.base_name_input.setPlaceholderText("输入基础命名规则（可选）")
        self.regex_pattern_input = QLineEdit()
        self.regex_pattern_input.setPlaceholderText("输入正则表达式")
        self.find_text_input = QLineEdit()
        self.replace_text_input = QLineEdit()
        find_replace_layout = QHBoxLayout()
        find_replace_layout.addWidget(QLabel("查找:"))
        find_replace_layout.addWidget(self.find_text_input)
        find_replace_layout.addWidget(QLabel("替换为:"))
        find_replace_layout.addWidget(self.replace_text_input)

        self.delete_start_spin = self.create_spinbox("删除开头字符数", 0)
        self.delete_end_spin = self.create_spinbox("删除结尾字符数", 0)
        self.date_format_input = QLineEdit()
        self.date_format_input.setPlaceholderText("输入日期格式（如%Y-%m-%d）")
        self.start_num_spin = self.create_spinbox("起始序号", 1)
        self.step_spin = self.create_spinbox("步长", 1)
        self.extension_input = QLineEdit()
        self.extension_input.setPlaceholderText("输入新的扩展名")
        self.case_conversion_combo = QComboBox()
        self.case_conversion_combo.addItems(["无", "转为大写", "转为小写"])

        layout.addWidget(QLabel("基础命名规则:"))
        layout.addWidget(self.base_name_input)
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
        layout.addWidget(QLabel("大小写转换:"))
        layout.addWidget(self.case_conversion_combo)

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

    def create_spinbox(self, label, default):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        spin = QSpinBox()
        spin.setValue(default)
        layout.addWidget(spin)
        return layout

    # 文件操作
    def add_files(self):
        FileOperations.add_files(self)

    def add_folder(self):
        FileOperations.add_folder(self)

    def clear_files(self):
        FileOperations.clear_files(self)

    def filter_files(self):
        FileOperations.filter_files(self)

    # 生成预览
    def generate_preview(self):
        RenameLogic.generate_preview(self)

    # 应用更改
    def apply_renaming(self):
        RenameLogic.apply_renaming(self)

    # 移动文件
    def move_files(self):
        FileOperations.move_files(self)

    # 删除文件
    def delete_files(self):
        FileOperations.delete_files(self)

    # 复制文件
    def copy_files(self):
        FileOperations.copy_files(self)