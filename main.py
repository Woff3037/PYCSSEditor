import os
from pathlib import Path
import sys
import random
import shutil
from PySide2.QtCore import QFile
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QTextCursor
from PySide2.QtUiTools import QUiLoader

def explorer_start():
    os.system("explorer.exe")

class MyWidget(QMainWindow):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.ui = None
        self.given_file_path2 = None
        self.load_ui()

    redBG = 0
    greenBG = 0
    blueBG = 0
    redFG = 0
    greenFG = 0
    blueFG = 0
    hex_code_bg = hex(000000)
    hex_code_fg = hex(000000)
    css_files = {}
    filepath = ""
    filename = ""
    stylesheet = f"background-color: {QColor(redBG, greenBG, blueBG).name()}\n" \
                 f"color: {QColor(redFG, greenFG, blueFG).name()}"

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)  # Assign the loaded UI to a member variable
        self.setCentralWidget(self.ui)  # Set the loaded UI as the central widget

        self.ui.RedSlider_2.valueChanged.connect(self.assign_red_bg)
        self.ui.GreenSlider_2.valueChanged.connect(self.assign_green_bg)
        self.ui.BlueSlider_2.valueChanged.connect(self.assign_blue_bg)
        self.ui.RedSlider_3.valueChanged.connect(self.assign_red_fg)
        self.ui.GreenSlider_3.valueChanged.connect(self.assign_green_fg)
        self.ui.BlueSlider_3.valueChanged.connect(self.assign_blue_fg)
        self.ui.MarginSlider.valueChanged.connect(self.assign_margin)
        self.ui.PaddingSlider.valueChanged.connect(self.assign_padding)
        self.ui.pushButton.clicked.connect(self.assign_hex_bg2)
        self.ui.pushButton_8.clicked.connect(self.assign_hex_fg2)
        self.ui.pushButton_2.clicked.connect(self.css_path_get)
        self.ui.pushButton_3.clicked.connect(self.file_save)
        self.ui.pushButton_4.clicked.connect(self.css_file_display)
        self.ui.pushButton_5.clicked.connect(explorer_start)
        self.ui.pushButton_6.clicked.connect(self.merge_css_files)
        self.ui.pushButton_7.clicked.connect(self.folder_delete)
        self.ui.comboBox.currentIndexChanged.connect(self.display_file_contents)
        ui_file.close()

    def folder_delete(self):
        shutil.rmtree(self.filename)
        self.ui.comboBox.clear()
        self.ui.textEdit.setPlainText("")

    def assign_red_bg(self, red):
        self.redBG = red
        self.rgb_to_hex_bg()
        self.assign_hex_bg()

    def assign_green_bg(self, green):
        self.greenBG = green
        self.rgb_to_hex_bg()
        self.assign_hex_bg()

    def assign_blue_bg(self, blue):
        self.blueBG = blue
        self.rgb_to_hex_bg()
        self.assign_hex_bg()

    def assign_hex_bg(self):
        self.hex_code_bg = self.rgb_to_hex_bg()
        self.ui.lineEdit.setText(self.hex_code_bg)

    def assign_hex_bg2(self):
        self.hex_code_bg = self.ui.lineEdit.text()
        self.hex_to_rgb_bg(self.hex_code_bg)

    def assign_red_fg(self, red_fg):
        self.redFG = red_fg
        self.assign_hex_fg()

    def assign_green_fg(self, green_fg):
        self.greenFG = green_fg
        self.assign_hex_fg()

    def assign_blue_fg(self, blue_fg):
        self.blueFG = blue_fg
        self.assign_hex_fg()

    def assign_hex_fg(self):
        self.hex_code_fg = self.rgb_to_hex_fg()
        self.ui.lineEdit_3.setText(self.hex_code_fg)

    def assign_hex_fg2(self):
        self.hex_code_fg = self.ui.lineEdit_3.text()
        self.hex_to_rgb_fg(self.hex_code_fg)

    def hex_to_rgb_bg(self, hex_code):
        hex_code = hex_code.lstrip('#')
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        self.ui.RedSlider_2.setValue(r)
        self.ui.GreenSlider_2.setValue(g)
        self.ui.BlueSlider_2.setValue(b)

    def rgb_to_hex_bg(self):
        hex_code = '#{:02x}{:02x}{:02x}'.format(self.redBG, self.greenBG, self.blueBG)
        self.assign_color()
        return hex_code

    def hex_to_rgb_fg(self, hex_code):
        hex_code = hex_code.lstrip('#')
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        self.ui.RedSlider_3.setValue(r)
        self.ui.GreenSlider_3.setValue(g)
        self.ui.BlueSlider_3.setValue(b)

    def rgb_to_hex_fg(self):
        hex_code = '#{:02x}{:02x}{:02x}'.format(self.redFG, self.greenFG, self.blueFG)
        self.assign_color()
        return hex_code

    def style_sheet_refresh(self):
        self.stylesheet = f"background-color: {QColor(self.redBG, self.greenBG, self.blueBG).name()}; " \
                          f"color: {QColor(self.redFG, self.greenFG, self.blueFG).name()}"

    def assign_color(self):
        # if self.ui.label_5.styleSheet() == "" or self.ui.label_5.styleSheet() is None:
        #    stylesheet = self.ui.label_5.styleSheet()
        #    self.ui.label_5.setStyleSheet(
        #        f"{stylesheet}\n
        # else:
        self.style_sheet_refresh()
        self.ui.label_5.setStyleSheet(self.stylesheet)

    def assign_margin(self, margin_value):
        self.ui.label_5.setMargin(margin_value)

    def assign_padding(self, padding_value):
        self.ui.horizontalSpacer_4.setWidth(padding_value)
        self.ui.horizontalSpacer_5.setWidth(padding_value)

    def css_file_display(self):
        self.filepath = self.ui.lineEdit.text()
        self.ui.comboBox.addItems(self.filepath)

    def css_path_get(self):
        self.split_css_blocks(self.ui.lineEdit_2.text())
        self.populate_dropdown()

    def populate_dropdown(self):
        file_names = os.listdir(self.filename)
        # Add the file names to the dropdown
        self.ui.comboBox.addItems(file_names)

    def file_save(self):
        with open(self.filepath, 'w') as file:
            file.write(self.ui.textEdit.toPlainText())

    def display_file_contents(self, index):
        selected_file = self.ui.comboBox.itemText(index)
        if selected_file:
            self.filepath = os.path.join(self.filename, selected_file)  # Specify the directory path here
            with open(self.filepath, 'r') as file:
                file_content = file.read()
                self.ui.textEdit.setPlainText(file_content)
                self.ui.textEdit.moveCursor(QTextCursor.Start)  # Scroll to the top of the text

    def merge_css_files(self):
        # Get a list of all split CSS files in the directory
        css_files = [file for file in os.listdir(self.filename) if file.endswith('.css')]

        # Sort the file names in ascending order
        css_files.sort()
        file_name = self.given_file_path2
        # Create or overwrite the output file
        with open(file_name, 'w') as output_file:
            for css_file in css_files:
                # Read the content of each split CSS file
                with open(os.path.join(self.filename, css_file), 'r') as input_file:
                    css_content = input_file.read()

                # Write the content to the output file
                output_file.write(css_content)
                self.folder_delete()

    def split_css_blocks(self, file_path):
        self.given_file_path2 = file_path
        # Read the CSS file
        with open(file_path, 'r') as file:
            css_content = file.read()

        # Split CSS content into blocks
        css_blocks = css_content.split('}')

        # Create a directory to store the split CSS files
        is_it_exist = True
        output_directory = ""
        while is_it_exist:
            output_dir = str(random.randint(0, 10000))
            for i in os.listdir(os.getcwd()):
                if i == output_dir:
                    is_it_exist = True
                else:
                    is_it_exist = False
                    output_directory = output_dir
        print(output_directory)
        self.filename = output_directory
        os.makedirs(output_directory, exist_ok=True)

        # Write each block into a separate CSS file
        for i, block in enumerate(css_blocks):
            # Remove any leading/trailing whitespace and ignore empty blocks
            block = block.strip()
            if block:
                # Create a file name based on the block index
                file_name = f'block_{i}.css'
                output_file = os.path.join(output_directory, file_name)

                # Write the block content into the separate CSS file
                with open(output_file, 'w') as output:
                    output.write(block + '}')

                print(f'Split block {i} saved as {file_name}')

if __name__ == "__main__":
    app = QApplication([])
    my_widget = MyWidget()
    my_widget.setMinimumSize(800, 600)
    my_widget.show()
    sys.exit(app.exec_())
