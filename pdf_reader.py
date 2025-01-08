import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QTextEdit, QFileDialog, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
import fitz  # PyMuPDF
from speed_reader import SpeedReader

class PDFReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Reader with SPRITZ Speed Reader')
        self.setGeometry(100, 100, 800, 600)
        self.setAcceptDrops(True)  # Enable drag-and-drop

        self.layout = QVBoxLayout()

        self.openButton = QPushButton('Open PDF', self)
        self.openButton.clicked.connect(self.openPDF)
        self.layout.addWidget(self.openButton)

        self.pdfViewer = QTextEdit(self)
        self.pdfViewer.setReadOnly(True)
        self.pdfViewer.mousePressEvent = self.handleMousePressEvent
        self.layout.addWidget(self.pdfViewer)

        self.speedReadButton = QPushButton('Speed Read', self)
        self.speedReadButton.clicked.connect(self.speedRead)
        self.layout.addWidget(self.speedReadButton)

        container = QWidget()
        container.setLayout(self.layout)

        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

    def openPDF(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if fileName:
            self.loadPDF(fileName)

    def loadPDF(self, fileName):
        self.document = fitz.open(fileName)
        self.page_index = 0
        self.loadPage()

    def loadPage(self):
        page = self.document.load_page(self.page_index)
        self.text = page.get_text("text").replace('-\n', '').replace('\n', ' ')
        self.pdfViewer.setPlainText(self.text)

    def nextPage(self):
        if self.page_index < len(self.document) - 1:
            self.page_index += 1
            self.loadPage()
            return True
        return False

    def speedRead(self):
        self.speedReader = SpeedReader(self.text, delay_sentence=0.1, delay_paragraph=0.22, parent=self)
        self.speedReader.show()

    def scrollToWord(self, word):
        cursor = self.pdfViewer.textCursor()
        cursor.movePosition(cursor.Start)
        if cursor.hasSelection():
            while cursor.hasSelection():
                cursor = self.pdfViewer.document().find(word, cursor)
                if not cursor.hasSelection():
                    break
                self.pdfViewer.setTextCursor(cursor)
                self.pdfViewer.ensureCursorVisible()
                return True
        return False

    def handleMousePressEvent(self, event):
        cursor = self.pdfViewer.cursorForPosition(event.pos())
        cursor.select(QTextCursor.WordUnderCursor)
        clicked_word = cursor.selectedText()
        if clicked_word:
            if self.speedReader:
                self.speedReader.jumpToWord(clicked_word)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            fileName = urls[0].toLocalFile()
            if fileName.lower().endswith('.pdf'):
                self.loadPDF(fileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = PDFReader()
    reader.show()
    sys.exit(app.exec_())
