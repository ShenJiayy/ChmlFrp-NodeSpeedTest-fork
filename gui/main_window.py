from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QListWidget, QListWidgetItem, QLabel, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from services.api_service import APIService
from .pages.node_test_page import NodeTestPage
from .pages.settings_page import SettingsPage
from .widgets.title_bar import TitleBar
from .widgets.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChmlFrp Node Speed Test")
        self.setMinimumSize(1000, 700)

        # Initialize services and user data
        self.api_service = APIService()
        self.user = self.api_service.get_stored_user()

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title bar
        self.title_bar = TitleBar()
        main_layout.addWidget(self.title_bar)

        # Content area
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.itemClicked.connect(self.on_sidebar_item_clicked)
        content_layout.addWidget(self.sidebar)

        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)

        # Create pages
        self.node_test_page = NodeTestPage(self.user, self.api_service)
        self.settings_page = SettingsPage(self.api_service)

        # Add pages to stack
        self.stacked_widget.addWidget(self.node_test_page)
        self.stacked_widget.addWidget(self.settings_page)

        main_layout.addWidget(content_widget)

        # Set initial page
        self.sidebar.setCurrentRow(0)
        self.stacked_widget.setCurrentIndex(0)

        # Load settings and user data
        self.load_settings()

    def load_settings(self):
        self.user = self.api_service.get_stored_user()
        self.node_test_page.set_user(self.user)
        self.settings_page.set_user(self.user)

    def on_sidebar_item_clicked(self, item):
        text = item.text()
        if text == "节点测试":
            self.stacked_widget.setCurrentIndex(0)
        elif text == "设置":
            self.stacked_widget.setCurrentIndex(1)

    def load_settings(self):
        # Load user settings, theme, etc.
        # For now, placeholder
        pass

    def closeEvent(self, event):
        # Save settings on close
        self.save_settings()
        event.accept()

    def save_settings(self):
        # Save user settings
        pass