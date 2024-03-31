import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QDragEnterEvent, QDropEvent, QFontMetrics

class ClickableLabel(QLabel):
    def __init__(self, url, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.url = url
        self.setText(url)

        # Set style
        self.setStyleSheet("QLabel { background-color : white; padding: 2px; }")
        self.setOpenExternalLinks(False)  # Handle clicks manually

        # Set fixed size and elide text
        self.setMaximumWidth(280)  # Adjust based on your UI needs
        fm = QFontMetrics(self.font())
        elidedText = fm.elidedText(url, Qt.TextElideMode.ElideMiddle, self.maximumWidth())
        self.setText(elidedText)

    def mousePressEvent(self, event):
        QDesktopServices.openUrl(QUrl(self.url))



class UrlCollector(QWidget):
    def __init__(self):
        super().__init__()
        self.max_urls = 10  # default url memory size
        self.url_slots = [None] * self.max_urls
        self.all_urls = []  # Initialize the master list of URLs
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.memorySizeComboBox = QComboBox()
        self.memorySizeComboBox.addItems(["2", "5", "10", "20"])
        self.memorySizeComboBox.setCurrentText(str(self.max_urls))  # Set the default value
        self.memorySizeComboBox.currentTextChanged.connect(self.memorySizeChanged)  # Connect to handler
        self.memorySizeComboBox.currentTextChanged.connect(self.onMemorySizeChanged)
        self.layout.addWidget(self.memorySizeComboBox)

        self.setAcceptDrops(True)
        
        # Initialize URL slots with placeholders
        for _ in range(self.max_urls):
            label = QLabel()
            label.setStyleSheet("background-color: gray;")  # Gray color for empty slots
            self.layout.addWidget(label)
        
        self.saveButton = QPushButton("Save URLs")
        self.saveButton.clicked.connect(self.saveUrls)
        self.layout.addWidget(self.saveButton)
        
        self.loadButton = QPushButton("Load URLs")
        self.loadButton.clicked.connect(self.loadUrls)
        self.layout.addWidget(self.loadButton)

        self.clearButton = QPushButton("Clear URLs")
        self.clearButton.clicked.connect(self.clearUrls)
        self.layout.addWidget(self.clearButton)

        self.setGeometry(100, 100, 300, 200)
        self.setFixedSize(300, 800)  # This locks the window size
        self.setWindowTitle('URL Collector')
        self.show()


    def memorySizeChanged(self, newSize):
        newSize = int(newSize)
        if newSize != self.max_urls:
            # Adjust the size of the url_slots list
            if newSize < self.max_urls:
                self.url_slots = self.url_slots[:newSize]  # Trim the list if reducing size
            else:
                # Extend the list with None values if increasing size
                self.url_slots += [None] * (newSize - len(self.url_slots))
            self.max_urls = newSize
            self.updateUI()  # Update the UI to reflect the change


    def onMemorySizeChanged(self, newSize):
        newSize = int(newSize)
        self.max_urls = newSize
        if len(self.all_urls) > self.max_urls:
            # If the stack is larger than the new max size, truncate the excess URLs
            self.all_urls = self.all_urls[:self.max_urls]
        self.updateStackStatus()



    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() or event.mimeData().hasText():
            event.acceptProposedAction()


    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                urlString = url.toString()
                # Handle file URLs differently from web URLs
                if urlString.startswith('file://'):
                    self.loadUrlsFromFile(urlString[len('file://'):])  # Remove the 'file://' prefix
                elif urlString.startswith('http://') or urlString.startswith('https://'):
                    self.addUrl(urlString)
        self.updateUI()


    def updateUI(self):
        # Clear existing URL display labels
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, ClickableLabel) or isinstance(widget, QLabel):
                self.layout.removeWidget(widget)
                widget.deleteLater()

        # Add memory size selection combo box again since it was removed
        self.layout.addWidget(self.memorySizeComboBox)

        # Re-add URL slots based on the current memory size
        for i, url in enumerate(self.url_slots):
            if url is not None:
                label = ClickableLabel(url)
            else:
                label = QLabel()
                label.setStyleSheet("background-color: gray;")
            self.layout.addWidget(label)

        # Make sure the save, load, and clear buttons are at the bottom
        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.loadButton)
        self.layout.addWidget(self.clearButton)


    def clearUrls(self):
        self.url_slots = [None] * self.max_urls  # Reset slots to empty
        self.updateUI()


    def saveUrls(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save URLs", "", "Text Files (*.txt)")
        if fileName:
            with open(fileName, 'w') as file:
                for url in self.url_slots:
                    if url is not None:  # Ensure only non-None URLs are written
                        file.write(url + '\n')


    def loadUrlsFromFile(self, filePath):
        try:
            with open(filePath, 'r') as file:
                loaded_urls = [line.strip() for line in file.readlines() if line.strip()]
            
            # Update self.all_urls with loaded URLs
            self.all_urls = loaded_urls

            # If the loaded file has more URLs than the current max, adjust the memory size
            if len(loaded_urls) > self.max_urls:
                # Find the appropriate memory size option
                new_memory_size = min([size for size in [2, 5, 10, 20] if size >= len(loaded_urls)], default=20)
                self.memorySizeComboBox.setCurrentText(str(new_memory_size))  # This triggers adjustMemorySize via its connected signal
            else:
                self.updateSlots()  # Update slots without changing the memory size if not necessary
        except Exception as e:
            print(f"Error loading URLs from file: {e}")


    def addUrl(self, urlString):
        if urlString not in self.all_urls:
            self.all_urls.append(urlString)
            self.updateSlots()



    def adjustMemorySize(self, required_size):
        for i in range(self.memorySizeComboBox.count()):
            if int(self.memorySizeComboBox.itemText(i)) >= required_size:
                self.memorySizeComboBox.setCurrentIndex(i)
                break
        self.max_urls = int(self.memorySizeComboBox.currentText())
        self.updateSlots()  # Ensure slots are updated based on the new size

    def updateSlots(self):
        self.url_slots = self.all_urls[:self.max_urls] + [None] * max(0, self.max_urls - len(self.all_urls))
        self.updateUI()


    def loadUrls(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Load URLs", "", "Text Files (*.txt)")
        if fileName:
            with open(fileName, 'r') as file:
                loaded_urls = [line.strip() for line in file.readlines() if line.strip()]
            
            # Determine the required memory size based on loaded URLs
            required_memory_size = len(loaded_urls)
            if required_memory_size > self.max_urls:
                # Find the closest matching option in the combo box
                for i in range(self.memorySizeComboBox.count()):
                    if int(self.memorySizeComboBox.itemText(i)) >= required_memory_size:
                        self.memorySizeComboBox.setCurrentIndex(i)
                        break
            self.url_slots = loaded_urls + [None] * (self.max_urls - len(loaded_urls))
            self.updateUI()

def main():
    app = QApplication(sys.argv)
    ex = UrlCollector()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()