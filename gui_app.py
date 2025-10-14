from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

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

# Make screen expand with window
screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

# -------------------- Buttons --------------------
btn_cam = QPushButton("Use Camera")
btn_upload = QPushButton("Upload Video")
btn_ip = QPushButton("Enter IP")

# Button styling
for btn in [btn_cam, btn_upload, btn_ip]:
    btn.setFixedHeight(40)
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
button_layout.setAlignment(Qt.AlignCenter)        # Space between buttons

main_layout = QVBoxLayout()
main_layout.addWidget(title)
main_layout.addWidget(screen, stretch=1)
main_layout.addLayout(button_layout)
main_layout.setAlignment(button_layout, Qt.AlignBottom)
main_layout.setContentsMargins(20, 20, 20, 20)  # Optional padding

window.setLayout(main_layout)
window.resize(700, 500)
window.show()
sys.exit(app.exec_())
