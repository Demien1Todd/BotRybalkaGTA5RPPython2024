import sys
import time
import pyautogui
from random import randint
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon

class Worker(QThread):
    update_status = pyqtSignal(str, str)
    key_pressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = False
        self.key_pressed.connect(self.stop)

    def run(self):
        red = (255, 0, 0)
        green = (0, 150, 100)
        rad = 150

        while self.running:
            mon = pyautogui.screenshot()
            pixR = mon.getpixel((1050 - 1, 900 - 1))
            pixD = mon.getpixel((660 - 1, 1053 - 1))

            if pixR == red:
                self.update_status.emit("Работаю...", "yellow")
                pyautogui.click(1920 / 2 + randint(-rad, rad) / 2, 1080 / 2 + randint(-rad, rad) / 2, duration=0.16)
                for ii in range(randint(4, 8)):
                    pyautogui.click()
            else:
                self.update_status.emit(f"Ожидание...", "white")

            ver = 1 - (abs(green[0] - pixD[0]) + abs(green[1] - pixD[1]) + abs(green[2] - pixD[2])) / 3 / 255
            if ver > 0.93:
                self.update_status.emit("+ Рыба!", "green")
                pyautogui.press('i')
                pyautogui.click(1760, 380, duration=0.5)
                pyautogui.click(1760, 450, duration=0.5)
                time.sleep(5)

            time.sleep(0.1)

        self.update_status.emit("Работа завершена", "red")

    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ㅤ")
        self.setGeometry(100, 100, 400, 70)
        self.setFixedSize(400, 90)

        # Установка иконки для окна
        self.setWindowIcon(QIcon("D:/Projects/BotyPython/botrybka/1112.png"))

        # Удаление верхней рамки окна
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Установка фона и стиля
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E2123; /* Цвет верхней рамки окна */
            }
            QLabel {
                color: #fff;
                font-size: 16px;
            }
        """)

        font = QFont("SF Pro Display")
        font.setPointSize(12)
        font.setBold(True)

        self.icon_label = QLabel()
        pixmap = QPixmap("D:/Projects/BotyPython/botrybka/111.png")  # Укажите путь к иконке удочки
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setFixedSize(75, 75)
        self.icon_label.setScaledContents(True)
        self.layout.addWidget(self.icon_label)

        self.info_layout = QVBoxLayout()
        self.info_layout.setSpacing(0)  # Устанавливает расстояние между виджетами внутри QVBoxLayout
        self.info_layout.setContentsMargins(0, 0, 0, 0)  # Устанавливает отступы вокруг QVBoxLayout
        self.layout.addLayout(self.info_layout)

        self.title_label = QLabel("Фишбот")
        self.title_label.setFont(font)
        self.info_layout.addWidget(self.title_label)

        self.status_label = QLabel("Бот выключен")
        self.status_label.setFont(font)
        self.info_layout.addWidget(self.status_label)

        self.worker = None

    def toggle_bot(self):
        if self.worker and self.worker.running:
            self.worker.stop()
            self.worker.wait()
            self.worker = None
            self.update_status("Бот выключен", "red")
        else:
            self.worker = Worker()
            self.worker.update_status.connect(self.update_status)
            self.worker.running = True
            self.worker.start()
            self.update_status("Бот включен", "green")

    def update_status(self, status, color):
        self.status_label.setText(f"{status}")
        self.status_label.setStyleSheet(f"color: {color}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F4:
            self.toggle_bot()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # Положение окна в правом верхнем углу
    screen = app.primaryScreen()
    screen_geometry = screen.geometry()
    window_width = 400
    window_height = 90
    window.move(screen_geometry.width() - window_width, 0)

    window.show()
    sys.exit(app.exec())
