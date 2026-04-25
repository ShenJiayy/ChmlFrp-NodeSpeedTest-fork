from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TitleBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QWidget {
                background-color: #2d3748;
                color: white;
                border-bottom: 1px solid #4a5568;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)

        # Title
        title = QLabel("ChmlFrp Node Speed Test")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)

        layout.addStretch()

        # Window controls (minimize, maximize, close)
        # For simplicity, we'll skip these for now
        # In a real app, you'd add buttons here