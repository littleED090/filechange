import os
import re
import shutil
from datetime import datetime
from PySide6.QtWidgets import QMessageBox

class RenameLogic:
    @staticmethod
    def generate_preview(app):
        app.preview_table.setRowCount(0)
        base_name = app.base_name_input.text()
        start_num = app.start_num_spin.itemAt(1).widget().value()
        step = app.step_spin.itemAt(1).widget().value()
        replace_from = app.find_text_input.text()
        replace_to = app.replace_text_input.text()
        regex_pattern = app.regex_pattern_input.text()
        delete_start = app.delete_start_spin.itemAt(1).widget().value()
        delete_end = app.delete_end_spin.itemAt(1).widget().value()
        date_format = app.date_format_input.text()
        extension = app.extension_input.text()
        case_conversion = app.case_conversion_combo.currentText()

        current_num = start_num

        for i, file_path in enumerate(app.selected_files):
            original_name = os.path.basename(file_path)
            new_name = original_name

            if regex_pattern:
                new_name = re.sub(regex_pattern, '', new_name)
            if replace_from:
                new_name = new_name.replace(replace_from, replace_to)
            new_name = new_name[delete_start:]
            if delete_end > 0:
                new_name = new_name[:-delete_end]
            if date_format:
                new_name = f"{new_name}_{datetime.now().strftime(date_format)}"
            if base_name:
                ext = os.path.splitext(new_name)[1]
                new_base = base_name.replace("{n}", str(current_num))
                new_name = f"{new_base}{ext}"
                current_num += step
            if extension:
                new_name = os.path.splitext(new_name)[0] + "." + extension
            if case_conversion == "转为大写":
                new_name = new_name.upper()
            elif case_conversion == "转为小写":
                new_name = new_name.lower()

            app.preview_table.insertRow(i)
            app.preview_table.setItem(i, 0, QTableWidgetItem(original_name))
            app.preview_table.setItem(i, 1, QTableWidgetItem(new_name))

    @staticmethod
    def apply_renaming(app):
        if app.preview_table.rowCount() == 0:
            QMessageBox.warning(app, "警告", "请先生成预览!")
            return

        success_count = 0
        errors = []

        for row in range(app.preview_table.rowCount()):
            original = app.preview_table.item(row, 0).text()
            new_name = app.preview_table.item(row, 1).text()
            original_path = next((f for f in app.selected_files if os.path.basename(f) == original), None)

            if original_path:
                try:
                    directory = os.path.dirname(original_path)
                    new_path = os.path.join(directory, new_name)
                    counter = 1
                    while os.path.exists(new_path):
                        base, ext = os.path.splitext(new_name)
                        new_path = os.path.join(directory, f"{base} ({counter}){ext}")
                        counter += 1
                    shutil.move(original_path, new_path)
                    success_count += 1
                except Exception as e:
                    errors.append(f"重命名 {original} 失败: {str(e)}")

        result_msg = f"成功重命名 {success_count} 个文件"
        if errors:
            result_msg += f"\n\n错误:\n" + "\n".join(errors)
        QMessageBox.information(app, "完成", result_msg)
        app.clear_files()