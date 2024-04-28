import cv2
from PyQt5.QtCore import QThread
from core.frame_processor import FrameProcessor

class VideoThread(QThread):
    def __init__(self, model, tracker):
        super().__init__()
        self.model = model
        self.tracker = tracker
        self.processor = FrameProcessor(model, tracker)
        self.running = False

    def run(self):
        self.running = True
        cap = cv2.VideoCapture(0)

        while self.running:
            ret, frame = cap.read()
            if ret:
                self.processor.process_frame(frame)
            else:
                break
        cap.release()

    def stop(self):
        self.running = False
        self.wait()

    def set_line(self, start, end):
        self.processor.line_start = start
        self.processor.line_end = end

    def clear_line(self):
        self.processor.line_start = None
        self.processor.line_end = None
