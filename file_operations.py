import os
import shutil
from PySide6.QtWidgets import QFileDialog, QMessageBox

class FileOperations:
    @staticmethod
    def add_files(app):
        files, _ = QFileDialog.getOpenFileNames(app, "选择文件")
        if files:
            app.selected_files.extend(files)
            app.file_list.addItems([os.path.basename(f) for f in files])

    @staticmethod
    def add_folder(app):
        folder = QFileDialog.getExistingDirectory(app, "选择文件夹")
        if folder:
            files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            app.selected_files.extend(files)
            app.file_list.addItems([os.path.basename(f) for f in files])

    @staticmethod
    def clear_files(app):
        app.selected_files = []
        app.file_list.clear()
        app.preview_table.setRowCount(0)

    @staticmethod
    def filter_files(app):
        keyword = app.search_input.text().lower()
        app.file_list.clear()
        filtered_files = [f for f in app.selected_files if keyword in os.path.basename(f).lower()]
        app.file_list.addItems([os.path.basename(f) for f in filtered_files])

    @staticmethod
    def move_files(app):
        destination_dir = QFileDialog.getExistingDirectory(app, "选择目标文件夹")
        if not destination_dir:
            return
        FileOperations._perform_operation(app, destination_dir, shutil.move, "移动")

    @staticmethod
    def delete_files(app):
        confirm = QMessageBox.question(app, "确认", "确定要删除选中的文件吗？", QMessageBox.Yes | QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return
        FileOperations._perform_operation(app, None, os.remove, "删除")

    @staticmethod
    def copy_files(app):
        destination_dir = QFileDialog.getExistingDirectory(app, "选择目标文件夹")
        if not destination_dir:
            return
        FileOperations._perform_operation(app, destination_dir, shutil.copy, "复制")

    @staticmethod
    def _perform_operation(app, destination_dir, operation, action_name):
        success_count = 0
        errors = []

        for file_path in app.selected_files:
            try:
                if destination_dir:
                    operation(file_path, destination_dir)
                else:
                    operation(file_path)
                success_count += 1
            except Exception as e:
                errors.append(f"{action_name} {file_path} 失败: {str(e)}")

        result_msg = f"成功{action_name} {success_count} 个文件"
        if errors:
            result_msg += f"\n\n错误:\n" + "\n".join(errors)
        QMessageBox.information(app, "完成", result_msg)