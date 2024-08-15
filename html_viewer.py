import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class HTMLViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HTML Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.browser = QWebEngineView()
        self.browser.setHtml("<h1>Welcome to the HTML Viewer</h1><p>Load an HTML file to view its content.</p>")

        self.load_button = QPushButton("Load HTML File")
        self.load_button.clicked.connect(self.load_html)

        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_html(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open HTML File", "", "HTML Files (*.html);;All Files (*)", options=options)
        if file_name:
            url = QUrl.fromLocalFile(file_name)
            self.browser.setUrl(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("HTML Viewer")
    viewer = HTMLViewer()
    viewer.show()
    sys.exit(app.exec_())
