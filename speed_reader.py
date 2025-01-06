from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QApplication
from PyQt5.QtCore import QTimer, Qt
import sys

class SpeedReader(QWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text.split()
        self.index = 0
        self.wpm = 300

        self.initUI()

    def initUI(self):
        self.setWindowTitle('SPRITZ Speed Reader')
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.wordLabel = QLabel('', self)
        self.wordLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.wordLabel)

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

    def startReading(self):
        self.timer.start(60000 // self.wpm)

    def stopReading(self):
        self.timer.stop()

    def displayNextWord(self):
        if self.index < len(self.text):
            self.displayWordWithORP(self.text[self.index])
            self.index += 1
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = SpeedReader("This is an example text for SPRITZ style speed reading.")
    reader.show()
    sys.exit(app.exec_())