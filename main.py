#!/usr/bin/env python3
"""
ChmlFrp Node Speed Test - Python/PyQt5 Version
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui.main_window import MainWindow

def main():
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("ChmlFrp Node Speed Test")
    app.setApplicationVersion("1.0.0")

    # Set application icon if available
    # app.setWindowIcon(QIcon("icon.png"))

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()