from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QCheckBox, QPushButton, QGroupBox, QFormLayout, QSpinBox
)
from PyQt5.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Appearance section
        appearance_group = QGroupBox("外观设置")
        appearance_layout = QFormLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["浅色", "深色", "跟随系统"])
        appearance_layout.addRow("主题:", self.theme_combo)

        self.sidebar_mode_combo = QComboBox()
        self.sidebar_mode_combo.addItems(["经典", "悬浮", "悬浮固定"])
        appearance_layout.addRow("侧边栏模式:", self.sidebar_mode_combo)

        appearance_group.setLayout(appearance_layout)
        layout.addWidget(appearance_group)

        # Update section
        update_group = QGroupBox("更新设置")
        update_layout = QFormLayout()

        self.auto_check_updates = QCheckBox("自动检查更新")
        self.auto_check_updates.setChecked(True)
        update_layout.addRow(self.auto_check_updates)

        self.update_channel_combo = QComboBox()
        self.update_channel_combo.addItems(["稳定版", "测试版"])
        update_layout.addRow("更新频道:", self.update_channel_combo)

        update_group.setLayout(update_layout)
        layout.addWidget(update_group)

        # Background section
        background_group = QGroupBox("背景设置")
        background_layout = QFormLayout()

        self.background_type_combo = QComboBox()
        self.background_type_combo.addItems(["无", "图片", "视频"])
        background_layout.addRow("背景类型:", self.background_type_combo)

        self.effect_type_combo = QComboBox()
        self.effect_type_combo.addItems(["无", "磨砂玻璃", "半透明"])
        background_layout.addRow("效果类型:", self.effect_type_combo)

        background_group.setLayout(background_layout)
        layout.addWidget(background_group)

        layout.addStretch()

        # Save button
        save_btn = QPushButton("保存设置")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn, alignment=Qt.AlignCenter)

    def load_settings(self):
        # Load settings from config file
        pass

    def save_settings(self):
        # Save settings to config file
        pass