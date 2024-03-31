# PathPiler URL Collector
![image](https://github.com/decanbay/PathPiler/assets/20815862/9bc034b2-d8ea-468a-8336-1c892f89b279)
![image](https://github.com/decanbay/PathPiler/assets/20815862/eb1f848b-a84d-45ab-8f10-80e17782b3b2)

I have created this for myself as I was getting distracted with the number of tabs and Could not limit myself.
Just drag your URL from your browser for queue, and click back on to deque.
It only queues unique URLs so that you can not queue the same url.

This is to store URLs in a First-In-First-Out (FIFO) manner, view the current queue capacity.

Compiled on Ubuntu 22.04
Binary file can be downloaded from here

https://github.com/decanbay/PathPiler/releases
chmod +x PathPiler

Double click or

./PathPiler


## Features

- **URL Queue Management**: Add URLs to a queue with a simple drag-and-drop interface.
- **FIFO Access**: Retrieve and open the oldest URL in the queue with just a click.
- **Capacity Display**: Visual indicator of the current queue status, showing how many URLs are stored versus the total capacity.
- **Dynamic Capacity**: Users can adjust the queue capacity as needed, with visual feedback changing from green to red as the queue fills up.
- **Unique URLs**: Only Unique URLs are stored.

## Getting Started

To get started with URL Collector, follow these steps:

 **either run with python (needs pyqt6) or crete an execuatable using pyinstaller
   
1. **Run URL Collector**: Double-click the executable to run the application.
2. **Add URLs**: Drag and drop URLs into the application window to add them to the queue.
3. **Open URLs**: Click on the capacity indicator to open and remove the oldest URL from the queue.

## Building from Source

If you prefer to build URL Collector from source, you will need Python and PyQt installed on your system. Follow these steps:

```
# Clone the repository
To get an executable 
pyinstaller --onefile --windowed --exclude-module _ssl --exclude-module pyqt5 PathPiler.py

OR

# Navigate to the project directory
pip install PyQt6

# Run the application
python url_collector.py
