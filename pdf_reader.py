import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QFileDialog
import fitz  # PyMuPDF
from speed_reader import SpeedReader

class PDFReader(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Reader with SPRITZ Speed Reader')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.openButton = QPushButton('Open PDF', self)
        self.openButton.clicked.connect(self.openPDF)
        self.layout.addWidget(self.openButton)

        self.pdfLabel = QLabel('PDF Content Here', self)
        self.layout.addWidget(self.pdfLabel)

        self.speedReadButton = QPushButton('Speed Read', self)
        self.speedReadButton.clicked.connect(self.speedRead)
        self.layout.addWidget(self.speedReadButton)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def openPDF(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if fileName:
            self.loadPDF(fileName)

    def loadPDF(self, fileName):
        document = fitz.open(fileName)
        page = document.load_page(0)  # Load first page
        self.text = page.get_text()
        self.pdfLabel.setText(self.text)

    def speedRead(self):
        self.speedReader = SpeedReader(self.text)
        self.speedReader.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = PDFReader()
    reader.show()
    sys.exit(app.exec_())