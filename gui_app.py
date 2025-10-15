from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QImage, QPixmap
from ultralytics import YOLO
import cv2
import sys

# -------------------- AI model --------------------
model = YOLO("/Users/manojvihar/Developer/Fire/runs/detect/train/weights/best.pt")

# -------------------- App --------------------
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("FireSense")

# -------------------- Title Label --------------------
title = QLabel("🔥 Fire Detection System 🔥")
title.setAlignment(Qt.AlignCenter)
title.setFont(QFont("Arial", 30, QFont.Bold))

# -------------------- Screen Area --------------------
screen = QLabel()
screen.setStyleSheet("background-color: black; border: 2px solid #333; border-radius: 10px;")
screen.setAlignment(Qt.AlignCenter)
screen.setMinimumSize(700, 400)
screen.setSizePolicy(screen.sizePolicy().Expanding, screen.sizePolicy().Expanding)

# -------------------- Buttons --------------------
btn_cam = QPushButton("Use Camera")
btn_upload = QPushButton("Upload Video")
btn_ip = QPushButton("Enter IP")
btn_reset = QPushButton("Reset")

for btn in [btn_cam, btn_upload, btn_ip, btn_reset]:
    btn.setFixedHeight(40)
    if btn == btn_reset:
        btn.setStyleSheet("""
            QPushButton {
                background-color: grey;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFA500;
            }
        """)
    else:
        btn.setStyleSheet("""
            QPushButton {
                background-color: #DC4D01;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFA500;
            }
        """)

# -------------------- Layouts --------------------
button_layout = QHBoxLayout()
button_layout.addWidget(btn_cam)
button_layout.addWidget(btn_upload)
button_layout.addWidget(btn_ip)
button_layout.addWidget(btn_reset)
button_layout.setAlignment(Qt.AlignCenter)

main_layout = QVBoxLayout()
main_layout.addWidget(title)
main_layout.addWidget(screen, stretch=1)
main_layout.addLayout(button_layout)
main_layout.setAlignment(button_layout, Qt.AlignBottom)
main_layout.setContentsMargins(20, 20, 20, 20)
window.setLayout(main_layout)
window.resize(850, 600)

# -------------------- Video / Camera Variables --------------------
cap = None
timer = QTimer()

# -------------------- Frame Processing --------------------
def process_frame():
    global cap
    if cap is None:
        return

    ret, frame = cap.read()
    if not ret:
        timer.stop()
        if cap:
            cap.release()
            cap = None
        return

    # YOLO inference
    results = model(frame)
    annotated_frame = results[0].plot()

    # Convert to QImage
    frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
    h, w, ch = frame_rgb.shape
    bytes_per_line = ch * w
    qimg = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

    # Scale to current QLabel size (keeps aspect ratio)
    pixmap = QPixmap.fromImage(qimg)
    screen_width = screen.width()
    screen_height = screen.height()
    screen.setPixmap(pixmap.scaled(screen_width, screen_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))

# Connect timer once
timer.timeout.connect(process_frame)

# -------------------- Upload Video --------------------
def upload_video():
    global cap, timer
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(
        window,
        "Select Video File",
        "",
        "Video Files (*.mp4 *.avi *.mov)",
        options=options
    )
    if file_path:
        if cap:
            cap.release()
        cap = cv2.VideoCapture(file_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30  # fallback if FPS is 0
        timer.start(int(1000 / fps))

# -------------------- Use Camera --------------------
def use_camera():
    global cap, timer
    if cap:
        cap.release()
    cap = cv2.VideoCapture(0)  # Built-in camera
    fps = 30
    timer.start(int(1000 / fps))

# -------------------- Use IP Camera --------------------
def enter_ip():
    global cap, timer
    ip_address, ok = QInputDialog.getText(window, "IP Camera", "Enter IP or RTSP stream URL:")
    if ok and ip_address.strip():
        if cap:
            cap.release()
        cap = cv2.VideoCapture(ip_address.strip())
        fps = 30
        timer.start(int(1000 / fps))

# -------------------- Reset Screen --------------------
def reset_screen():
    global cap, timer
    if timer.isActive():
        timer.stop()
    if cap:
        cap.release()
        cap = None
    screen.clear()
    screen.setStyleSheet("background-color: black; border: 2px solid #333; border-radius: 10px;")

# -------------------- Buttons --------------------
btn_upload.clicked.connect(upload_video)
btn_cam.clicked.connect(use_camera)
btn_ip.clicked.connect(enter_ip)
btn_reset.clicked.connect(reset_screen)

# -------------------- Show Window --------------------
window.show()
sys.exit(app.exec_())
