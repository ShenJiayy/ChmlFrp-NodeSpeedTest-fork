from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class Sidebar(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setStyleSheet("""
            QListWidget {
                background-color: #1a202c;
                color: white;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 15px;
                border-bottom: 1px solid #2d3748;
            }
            QListWidget::item:selected {
                background-color: #3182ce;
            }
            QListWidget::item:hover {
                background-color: #2d3748;
            }
        """)

        # Add items
        self.add_item("节点测试", "network")
        self.add_item("设置", "settings")

    def add_item(self, text, icon_name=None):
        item = QListWidgetItem(text)
        item.setFont(QFont("Arial", 12))
        # If you have icons, set them here
        # if icon_name:
        #     item.setIcon(QIcon(f"icons/{icon_name}.png"))
        self.addItem(item)