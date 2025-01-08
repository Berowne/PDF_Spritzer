from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
import sys
import time

class SpeedReader(QWidget):
    def __init__(self, text, delay_sentence=0.1, delay_paragraph=0.22, parent=None):
        super().__init__()
        self.text = text
        self.words = self.splitTextIntoWords(text)
        self.index = 0
        self.wpm = 300
        self.delay_sentence = delay_sentence
        self.delay_paragraph = delay_paragraph
        self.parent = parent

        self.initUI()

    def initUI(self):
        self.setWindowTitle('SPRITZ Speed Reader')
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.wordLayout = QHBoxLayout()

        self.backButton = QPushButton(self)
        self.backButton.setIcon(QIcon('back.png'))  # Replace 'back.png' with your back icon file path
        self.backButton.setFixedSize(50, 200)
        self.backButton.clicked.connect(self.back10s)
        self.wordLayout.addWidget(self.backButton)

        self.wordLabel = QLabel(f'WPM: {self.wpm}', self)
        self.wordLabel.setAlignment(Qt.AlignCenter)
        self.wordLayout.addWidget(self.wordLabel)

        self.forwardButton = QPushButton(self)
        self.forwardButton.setIcon(QIcon('forward.png'))  # Replace 'forward.png' with your forward icon file path
        self.forwardButton.setFixedSize(50, 200)
        self.forwardButton.clicked.connect(self.forward10s)
        self.wordLayout.addWidget(self.forwardButton)

        self.layout.addLayout(self.wordLayout)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(100)
        self.slider.setMaximum(1000)
        self.slider.setValue(self.wpm)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(100)
        self.slider.valueChanged.connect(self.setWPM)
        self.layout.addWidget(self.slider)

        self.startButton = QPushButton('Start', self)
        self.startButton.clicked.connect(self.startReading)
        self.layout.addWidget(self.startButton)

        self.stopButton = QPushButton('Stop', self)
        self.stopButton.clicked.connect(self.stopReading)
        self.layout.addWidget(self.stopButton)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.displayNextWord)

        self.setLayout(self.layout)

    def setWPM(self, value):
        self.wpm = value
        self.wordLabel.setText(f'WPM: {self.wpm}')

    def startReading(self):
        self.timer.start(60000 // self.wpm)

    def stopReading(self):
        self.timer.stop()

    def splitTextIntoWords(self, text):
        return text.split()

    def displayNextWord(self):
        if self.index < len(self.words):
            word = self.words[self.index]
            self.displayWordWithORP(word)
            if self.parent:
                self.parent.scrollToWord(word)
            self.index += 1

            if self.isEndOfSentence(word):
                time.sleep(self.delay_sentence)
            if self.isEndOfParagraph(word):
                time.sleep(self.delay_paragraph)
                self.scrollBackground()

        else:
            if self.parent and self.parent.nextPage():
                self.text = self.parent.text
                self.words = self.splitTextIntoWords(self.text)
                self.index = 0
                self.displayNextWord()
            else:
                self.timer.stop()

    def displayWordWithORP(self, word):
        formattedText = ''
        orpIndex = self.findORPIndex(word)
        for i, char in enumerate(word):
            if i == orpIndex:
                formattedText += f'<span style="color:red;">{char}</span>'
            else:
                formattedText += char
        self.wordLabel.setText(f"<html><body><p style='font-size:24px;'>{formattedText}</p></body></html>")

    def findORPIndex(self, word):
        vowels = "aeiouAEIOU"
        for i, char in enumerate(word):
            if char in vowels:
                return i
        return 0  # If no vowels are found, highlight the first character

    def isEndOfSentence(self, word):
        return word.endswith('.')

    def isEndOfParagraph(self, word):
        return word[-1] in ".!?" if word.strip()[-1] in ".!?" else False

    def scrollBackground(self):
        # Implement scrolling behavior to scroll half a page at a time
        pass

    def back10s(self):
        self.index = max(0, self.index - (self.wpm // 6))

    def forward10s(self):
        self.index = min(len(self.words) - 1, self.index + (self.wpm // 6))

    def jumpToWord(self, word):
        word_list = self.text.split()
        try:
            self.index = word_list.index(word, self.index)
            self.displayNextWord()
        except ValueError:
            pass  # If the word is not found, do nothing

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = SpeedReader("This is an example text for SPRITZ style speed reading.")
    reader.show()
    sys.exit(app.exec_())
