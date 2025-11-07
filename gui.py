import sys
import cv2
import time
import numpy as np
from threading import Thread
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer


class CameraThread:
    def __init__(self, source=0):
        self.capture = cv2.VideoCapture(source)
        self.running = False
        self.frame = None
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = Thread(target=self.update, daemon=True)
            self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.capture.read()
            if ret:
                self.frame = frame
            time.sleep(1 / 30)  # 30 FPS

    def stop(self):
        self.running = False
        self.capture.release()


class GymLyticsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GymLytics")
        self.setGeometry(100, 100, 800, 600)

        # Виджеты
        self.video_label = QLabel(self)
        self.exercise_selector = QComboBox(self)
        self.exercise_selector.addItems(["Squat", "Pushup", "Plank", "Lunges", "Shoulder Tap"])

        self.start_button = QPushButton("Старт камеры", self)
        self.stop_button = QPushButton("Стоп камеры", self)
        self.exit_button = QPushButton("Выход", self)

        # Расположение
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.exercise_selector)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.exit_button)
        self.setLayout(layout)

        # Камера
        self.camera = CameraThread()

        # Таймер для обновления видео
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Подключение кнопок
        self.start_button.clicked.connect(self.start_camera)
        self.stop_button.clicked.connect(self.stop_camera)
        self.exit_button.clicked.connect(self.close_app)

    def start_camera(self):
        self.camera.start()
        self.timer.start(30)  # Обновление каждые 30 мс

    def stop_camera(self):
        self.timer.stop()
        self.camera.stop()
        self.video_label.clear()

    def update_frame(self):
        if self.camera.frame is not None:
            frame = cv2.cvtColor(self.camera.frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qimg))

    def close_app(self):
        self.stop_camera()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GymLyticsApp()
    window.show()
    sys.exit(app.exec())
