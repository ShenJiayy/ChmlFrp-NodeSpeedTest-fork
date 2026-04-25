import json
import os

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QCheckBox, QPushButton, QGroupBox, QFormLayout, QSpinBox, QDialog
)
from PyQt5.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self, api_service):
        super().__init__()
        self.api_service = api_service
        self.user = None
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

        # Login section
        login_group = QGroupBox("登录")
        login_layout = QVBoxLayout()
        self.login_status_label = QLabel("未登录")
        login_layout.addWidget(self.login_status_label)

        login_buttons = QHBoxLayout()
        self.login_btn = QPushButton("登录")
        self.login_btn.clicked.connect(self.open_login_dialog)
        self.logout_btn = QPushButton("退出登录")
        self.logout_btn.clicked.connect(self.logout)
        login_buttons.addWidget(self.login_btn)
        login_buttons.addWidget(self.logout_btn)
        login_layout.addLayout(login_buttons)

        login_group.setLayout(login_layout)
        layout.addWidget(login_group)

        layout.addStretch()

        # Save button
        save_btn = QPushButton("保存设置")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn, alignment=Qt.AlignCenter)

    def load_settings(self):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config.json'))
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.theme_combo.setCurrentText(self.map_theme_value(config.get('theme', '浅色')))
            self.sidebar_mode_combo.setCurrentText(self.map_sidebar_value(config.get('sidebar_mode', '经典')))
            self.auto_check_updates.setChecked(config.get('auto_check_updates', True))
            self.update_channel_combo.setCurrentText(self.map_update_channel(config.get('update_channel', '稳定版')))
            self.background_type_combo.setCurrentText(self.map_background_type(config.get('background_type', '无')))
            self.effect_type_combo.setCurrentText(self.map_effect_type(config.get('effect_type', '无')))
        self.update_login_status()

    def set_user(self, user):
        self.user = user
        self.update_login_status()

    def update_login_status(self):
        if self.user and self.user.get('accessToken'):
            username = self.user.get('username', '已登录用户')
            self.login_status_label.setText(f"已登录: {username}")
            self.logout_btn.setEnabled(True)
        else:
            self.login_status_label.setText("未登录")
            self.logout_btn.setEnabled(False)

    def open_login_dialog(self):
        from gui.dialogs.login_dialog import LoginDialog

        dialog = LoginDialog(self.api_service, self)
        if dialog.exec_() == QDialog.Accepted:
            self.user = self.api_service.get_stored_user()
            self.update_login_status()

    def logout(self):
        self.api_service.clear_user()
        self.user = None
        self.update_login_status()

    def save_settings(self):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config.json'))
        config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

        config['theme'] = self.theme_combo.currentText()
        config['sidebar_mode'] = self.sidebar_mode_combo.currentText()
        config['auto_check_updates'] = self.auto_check_updates.isChecked()
        config['update_channel'] = self.update_channel_combo.currentText()
        config['background_type'] = self.background_type_combo.currentText()
        config['effect_type'] = self.effect_type_combo.currentText()

        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def map_theme_value(self, value):
        return {
            'light': '浅色',
            'dark': '深色',
            'system': '跟随系统'
        }.get(value, value)

    def map_sidebar_value(self, value):
        return {
            'classic': '经典',
            'floating': '悬浮',
            'floating_fixed': '悬浮固定'
        }.get(value, value)

    def map_update_channel(self, value):
        return {
            'stable': '稳定版',
            'beta': '测试版'
        }.get(value, value)

    def map_background_type(self, value):
        return {
            'none': '无',
            'image': '图片',
            'video': '视频'
        }.get(value, value)

    def map_effect_type(self, value):
        return {
            'none': '无',
            'frosted': '磨砂玻璃',
            'translucent': '半透明'
        }.get(value, value)
