from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QComboBox, QLineEdit, QLabel, QProgressBar, QCheckBox,
    QHeaderView, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from services.api_service import APIService
from services.speed_test_service import SpeedTestService
from gui.dialogs.batch_test_dialog import BatchTestDialog
from gui.dialogs.node_history_dialog import NodeHistoryDialog

class NodeTestPage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.nodes = []
        self.api_service = APIService()
        self.speed_test_service = SpeedTestService()

        self.init_ui()
        self.load_nodes()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Toolbar
        toolbar = QHBoxLayout()

        # Refresh button
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.load_nodes)
        toolbar.addWidget(self.refresh_btn)

        # Test all button
        self.test_all_btn = QPushButton("测试全部")
        self.test_all_btn.clicked.connect(self.test_all_nodes)
        toolbar.addWidget(self.test_all_btn)

        # Batch test button
        self.batch_test_btn = QPushButton("批量测试")
        self.batch_test_btn.clicked.connect(self.show_batch_test_dialog)
        toolbar.addWidget(self.batch_test_btn)

        toolbar.addStretch()

        # Filters
        self.region_combo = QComboBox()
        self.region_combo.addItems(["全部", "国内", "国外"])
        self.region_combo.currentTextChanged.connect(self.filter_nodes)
        toolbar.addWidget(QLabel("地区:"))
        toolbar.addWidget(self.region_combo)

        self.user_type_combo = QComboBox()
        self.user_type_combo.addItems(["全部", "VIP", "普通"])
        self.user_type_combo.currentTextChanged.connect(self.filter_nodes)
        toolbar.addWidget(QLabel("用户类型:"))
        toolbar.addWidget(self.user_type_combo)

        # Search
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索节点...")
        self.search_edit.textChanged.connect(self.filter_nodes)
        toolbar.addWidget(QLabel("搜索:"))
        toolbar.addWidget(self.search_edit)

        layout.addLayout(toolbar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "选择", "ID", "名称", "地区", "分组", "延迟", "下载速度", "状态"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        # Progress bar for testing
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

    def load_nodes(self):
        # Load nodes from API
        try:
            self.nodes = self.api_service.fetch_nodes()
            self.update_table()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"加载节点失败: {str(e)}")

    def update_table(self):
        self.table.setRowCount(len(self.nodes))
        for row, node in enumerate(self.nodes):
            # Checkbox for selection
            checkbox = QCheckBox()
            self.table.setCellWidget(row, 0, checkbox)

            # Node data
            self.table.setItem(row, 1, QTableWidgetItem(str(node.get('id', ''))))
            self.table.setItem(row, 2, QTableWidgetItem(node.get('name', '')))
            self.table.setItem(row, 3, QTableWidgetItem(node.get('area', '')))
            self.table.setItem(row, 4, QTableWidgetItem(node.get('nodegroup', '')))

            # Test results (placeholder)
            self.table.setItem(row, 5, QTableWidgetItem("-"))
            self.table.setItem(row, 6, QTableWidgetItem("-"))
            self.table.setItem(row, 7, QTableWidgetItem("未测试"))

    def filter_nodes(self):
        # Implement filtering logic
        pass

    def test_all_nodes(self):
        # Implement test all
        pass

    def show_batch_test_dialog(self):
        dialog = BatchTestDialog(self.nodes, self)
        dialog.exec_()

    def show_node_history(self, node, test_type):
        dialog = NodeHistoryDialog(node, test_type, self)
        dialog.exec_()