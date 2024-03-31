from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider
from PyQt6.QtGui import QDesktopServices, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt, QUrl
import sys

class UrlCollector(QWidget):
    def __init__(self):
        super().__init__()
        self.all_urls = []  # Initialize the list to hold URLs
        self.max_urls = 5  # Set default memory size
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Slider for selecting memory size
        self.memorySizeSlider = QSlider(Qt.Orientation.Horizontal)
        self.memorySizeSlider.setMinimum(0)  # Minimum slider value
        self.memorySizeSlider.setMaximum(3)  # Maximum slider value (for 4 positions)
        self.memorySizeSlider.setTickInterval(1)  # Step size
        self.memorySizeSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.memorySizeSlider.setValue(1)  # Default position (5)
        self.memorySizeSlider.valueChanged.connect(self.onMemorySizeChanged)  # Connect signal
        self.layout.addWidget(self.memorySizeSlider)
        # Stack status display
        self.stackStatus = QLabel("0/5")
        self.stackStatus.setStyleSheet("""
            QLabel {
                background-color: lightgreen;
                border-radius: 20px;
                font-size: 16px;
                color: black;
                padding: 10px;
            }
        """)

        self.stackStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stackStatus.setFixedHeight(50)
        self.stackStatus.mousePressEvent = self.retrieveTopUrl
        self.layout.addWidget(self.stackStatus)

        self.setGeometry(100, 100, 300, 150)
        self.setWindowTitle('URL FIFO Stack')
        self.setAcceptDrops(True)
        self.show()


    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            urlString = url.toString()
            if urlString.startswith('http://') or urlString.startswith('https://'):
                if urlString not in self.all_urls and len(self.all_urls) < self.max_urls:
                    self.all_urls.append(urlString)
                    self.updateStackStatus()

    def updateStackStatus(self):
        fullness = len(self.all_urls) / self.max_urls
        red = int(255 * fullness)
        green = 255 - red
        color = f'rgb({red}, {green}, 0)'
        self.stackStatus.setText(f"{len(self.all_urls)}/{self.max_urls}")
        self.stackStatus.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border-radius: 20px;
                font-size: 16px;
                color: black;
                padding: 10px;
            }}
        """)

    def retrieveTopUrl(self, event):
        if self.all_urls:
            topUrl = self.all_urls.pop(0)
            QDesktopServices.openUrl(QUrl(topUrl))
            self.updateStackStatus()


    def onMemorySizeChanged(self, value):
        # Map slider positions to memory sizes
        memory_sizes = [2, 5, 10, 20]
        newSize = memory_sizes[value]
        self.max_urls = newSize
        # Update display accordingly
        if len(self.all_urls) > self.max_urls:
            # Adjust the list of URLs if it exceeds the new maximum
            self.all_urls = self.all_urls[:self.max_urls]
        self.updateStackStatus()


def main():
    app = QApplication(sys.argv)
    ex = UrlCollector()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
