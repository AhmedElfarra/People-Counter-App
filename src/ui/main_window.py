import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage, QPixmap
import torch
from core.video_thread import VideoThread
from deep_sort_realtime.deepsort_tracker import DeepSort
from tools.ws_client import WebSocketClient

class MainWindow(QMainWindow):
    def __init__(self, model_path='models/yolov5s6.pt'):
        super().__init__()
        self.setWindowTitle("People Counter with System Stats")
        self.setGeometry(100, 100, 1200, 800)
        
        # Load the model with the specified path
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        self.tracker = DeepSort(max_age=10, nn_budget=25, override_track_class=None)
        self.ws_client = WebSocketClient("ws://127.0.0.1:8000/ws")

        self.initUI()
        self.initCamera()
        

    def initUI(self):
        self.drawing = False
        self.line_start = QPoint()
        self.line_end = QPoint()

        main_layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(960, 720)  # Enlarged webcam display
        main_layout.addWidget(self.image_label)

        self.count_label = QLabel("Entering: 0, Exiting: 0", self)
        self.stats_label = QLabel("FPS: 0, CPU: 0%, Memory: 0%", self)
        main_layout.addWidget(self.count_label)
        main_layout.addWidget(self.stats_label)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()
        self.draw_button = QPushButton('Draw Line', self)
        self.erase_button = QPushButton('Erase Line', self)
        self.draw_button.clicked.connect(self.toggleDrawing)
        self.erase_button.clicked.connect(self.eraseLine)
        button_layout.addWidget(self.draw_button)
        button_layout.addWidget(self.erase_button)
        
        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def initCamera(self):
        self.thread = VideoThread(self.model, self.tracker)
        if self.thread.processor:
            self.thread.processor.update_signal.connect(self.updateUI)
        else:
            print("Processor is not initialized.")
        self.thread.start()

    def toggleDrawing(self):
        self.drawing = not self.drawing
        if not self.drawing:
            self.thread.set_line((self.line_start.x(), self.line_start.y()), (self.line_end.x(), self.line_end.y()))

    def eraseLine(self):
        self.thread.clear_line()
        self.line_start = QPoint()
        self.line_end = QPoint()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.line_start = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.line_end = event.pos()
            self.update()

    def updateUI(self, frame, entering_count, exiting_count, fps, cpu_usage, memory_usage):
        self.count_label.setText(f"Entering: {entering_count}, Exiting: {exiting_count}")
        self.stats_label.setText(f"FPS: {fps:.2f}, CPU: {cpu_usage}%, Memory: {memory_usage}%")
        self.ws_client.update_counts(entering_count, exiting_count)

        h, w, ch = frame.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(convert_to_Qt_format)
        self.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.thread.stop()
        super().closeEvent(event)