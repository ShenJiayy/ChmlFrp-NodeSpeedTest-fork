from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QProgressBar, QTextEdit,
    QCheckBox, QSpinBox, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from services.speed_test_service import SpeedTestService

class BatchTestDialog(QDialog):
    def __init__(self, nodes, parent=None):
        super().__init__(parent)
        self.nodes = nodes
        self.speed_test_service = SpeedTestService()
        self.results = []

        self.setWindowTitle("批量速度测试")
        self.setModal(True)
        self.resize(800, 600)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Options
        options_group = QGroupBox("测试选项")
        options_layout = QFormLayout()

        self.test_latency_cb = QCheckBox("测试延迟")
        self.test_latency_cb.setChecked(True)
        options_layout.addRow(self.test_latency_cb)

        self.test_speed_cb = QCheckBox("测试下载速度")
        self.test_speed_cb.setChecked(True)
        options_layout.addRow(self.test_speed_cb)

        self.test_size_spin = QSpinBox()
        self.test_size_spin.setRange(1, 100)
        self.test_size_spin.setValue(10)
        self.test_size_spin.setSuffix(" MB")
        options_layout.addRow("测试文件大小:", self.test_size_spin)

        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # Progress
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("准备开始测试...")
        layout.addWidget(self.status_label)

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            "节点名称", "延迟(ms)", "下载速度(Mbps)", "状态", "错误"
        ])
        layout.addWidget(self.results_table)

        # Logs
        self.logs_text = QTextEdit()
        self.logs_text.setMaximumHeight(150)
        self.logs_text.setReadOnly(True)
        layout.addWidget(self.logs_text)

        # Buttons
        buttons_layout = QHBoxLayout()

        self.start_btn = QPushButton("开始测试")
        self.start_btn.clicked.connect(self.start_test)
        buttons_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("停止测试")
        self.stop_btn.clicked.connect(self.stop_test)
        self.stop_btn.setEnabled(False)
        buttons_layout.addWidget(self.stop_btn)

        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(self.close_btn)

        layout.addLayout(buttons_layout)

    def start_test(self):
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.results = []

        # Start testing in thread
        # For now, placeholder
        pass

    def stop_test(self):
        self.speed_test_service.abort()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def update_progress(self, progress):
        self.progress_bar.setValue(int(progress * 100))
        self.status_label.setText(progress.message)

        # Update logs
        logs_text = ""
        for log in progress.logs:
            logs_text += f"[{log.type}] {log.message}\n"
        self.logs_text.setPlainText(logs_text)

    def test_completed(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("测试完成")