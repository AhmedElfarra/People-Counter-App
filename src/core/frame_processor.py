import cv2
import numpy as np
import time
from PyQt5.QtCore import QObject, pyqtSignal
import psutil


class FrameProcessor(QObject):
    update_signal = pyqtSignal(np.ndarray, int, int, float, float, float)

    def __init__(self, model, tracker):
        super().__init__()
        self.model = model
        self.tracker = tracker
        self.track_positions = {}
        self.entering_count = 0
        self.exiting_count = 0
        self.line_start = None
        self.line_end = None
        self.last_time = time.time()
        self.frame_count = 0

    def is_intersect(self, p1, p2, p3, p4):
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

    def check_crossing(self, track_id):
        if len(self.track_positions[track_id]) < 2 or not self.line_start or not self.line_end:
            return None

        prev_pos, curr_pos = self.track_positions[track_id][:2]
        line_vec = (self.line_end[0] - self.line_start[0], self.line_end[1] - self.line_start[1])
        move_vec = (curr_pos[0] - prev_pos[0], curr_pos[1] - prev_pos[1])

        if not self.is_intersect(prev_pos, curr_pos, self.line_start, self.line_end):
            return None

        cross_product = line_vec[0] * move_vec[1] - line_vec[1] * move_vec[0]

        if cross_product > 0:
            return "entering"
        elif cross_product < 0:
            return "exiting"
        return None

    def process_frame(self, frame):
        current_time = time.time()
        self.frame_count += 1
        fps = self.frame_count / (current_time - self.last_time)
        if self.frame_count == 10:
            self.last_time = current_time
            self.frame_count = 0

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model(rgb_frame)
        detections = results.xyxy[0]
        bbs = [(x[:4].cpu().numpy(), x[4].cpu().item(), x[5].cpu().item()) for x in detections if int(x[5]) == 0]

        tracks = self.tracker.update_tracks(bbs, frame=rgb_frame)

        for track in tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue

            bbox = track.to_ltrb()
            center = ((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2)

            if track.track_id not in self.track_positions:
                self.track_positions[track.track_id] = []

            self.track_positions[track.track_id].append(center)
            if len(self.track_positions[track.track_id]) > 2:
                self.track_positions[track.track_id].pop(0)

            crossing = self.check_crossing(track.track_id)
            if crossing == "entering":
                self.entering_count += 1
            elif crossing == "exiting":
                self.exiting_count += 1

            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {track.track_id}", (int(bbox[0]), int(bbox[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

        if self.line_start and self.line_end:
            cv2.line(frame, self.line_start, self.line_end, (255, 0, 0), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        self.update_signal.emit(frame, self.entering_count, self.exiting_count, fps, cpu_usage, memory_usage)
