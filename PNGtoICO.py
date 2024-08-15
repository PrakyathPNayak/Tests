#copied code, so if you want to edit the code, just feed it through gpt, everything should be stadnart

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PIL import Image

class PNGtoICOConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PNG to ICO Converter')
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.label1 = QLabel('Select PNG file:')
        self.layout.addWidget(self.label1)

        self.png_path_edit = QLineEdit(self)
        self.layout.addWidget(self.png_path_edit)

        self.browse_button1 = QPushButton('Browse', self)
        self.browse_button1.clicked.connect(self.browse_png_file)
        self.layout.addWidget(self.browse_button1)

        self.label2 = QLabel('Select output directory:')
        self.layout.addWidget(self.label2)

        self.output_dir_edit = QLineEdit(self)
        self.layout.addWidget(self.output_dir_edit)

        self.browse_button2 = QPushButton('Browse', self)
        self.browse_button2.clicked.connect(self.browse_output_directory)
        self.layout.addWidget(self.browse_button2)

        self.convert_button = QPushButton('Convert to ICO', self)
        self.convert_button.clicked.connect(self.convert_to_ico)
        self.layout.addWidget(self.convert_button)

        self.status_label = QLabel('', self)
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

    def browse_png_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PNG File", "", "PNG Files (*.png);;All Files (*)", options=options)
        if file_path:
            self.png_path_edit.setText(file_path)

    def browse_output_directory(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory", options=options)
        if directory:
            self.output_dir_edit.setText(directory)

    def convert_to_ico(self):
        png_path = self.png_path_edit.text()
        output_dir = self.output_dir_edit.text()

        if not png_path or not output_dir:
            self.status_label.setText("Please select a PNG file and output directory.")
            return

        icon_name = os.path.splitext(os.path.basename(png_path))[0] + '.ico'
        ico_path = os.path.join(output_dir, icon_name)

        try:
            self.convert_png_to_ico(png_path, ico_path)
            self.status_label.setText(f"Converted {png_path} to {ico_path}")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def convert_png_to_ico(self, png_path, ico_path, icon_sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]):
        img = Image.open(png_path)
        img.save(ico_path, format='ICO', sizes=icon_sizes)
        print(f"Converted {png_path} to {ico_path}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = PNGtoICOConverter()
    converter.show()
    sys.exit(app.exec_())
