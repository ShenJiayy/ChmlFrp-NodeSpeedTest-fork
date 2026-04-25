from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox
)
from PyQt5.QtCore import Qt

class NodeHistoryDialog(QDialog):
    def __init__(self, node, test_type, parent=None):
        super().__init__(parent)
        self.node = node
        self.test_type = test_type  # "latency" or "speed"

        self.setWindowTitle(f"{node.get('name', '')} - 历史记录")
        self.setModal(True)
        self.resize(600, 400)

        self.init_ui()
        self.load_history()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Info
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel(f"节点: {self.node.get('name', '')}"))
        info_layout.addWidget(QLabel(f"地区: {self.node.get('area', '')}"))
        info_layout.addStretch()
        layout.addLayout(info_layout)

        # Test type selector
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("测试类型:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["延迟", "下载速度"])
        self.type_combo.setCurrentText("延迟" if self.test_type == "latency" else "下载速度")
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()
        layout.addLayout(type_layout)

        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels([
            "时间", "结果", "成功", "错误"
        ])
        layout.addWidget(self.history_table)

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(close_btn)

        layout.addLayout(buttons_layout)

    def on_type_changed(self, text):
        self.test_type = "latency" if text == "延迟" else "speed"
        self.load_history()

    def load_history(self):
        # Load history from storage
        # For now, placeholder
        self.history_table.setRowCount(0)