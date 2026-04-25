from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self, api_service, parent=None):
        super().__init__(parent)
        self.api_service = api_service
        self.setWindowTitle("登录")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("请输入 access token 或 Bearer 令牌："))

        self.token_edit = QLineEdit()
        self.token_edit.setPlaceholderText("Bearer ... 或 直接填写 accessToken")
        layout.addWidget(self.token_edit)

        button_layout = QHBoxLayout()
        self.login_btn = QPushButton("登录")
        self.login_btn.clicked.connect(self.on_login)
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

    def on_login(self):
        token = self.token_edit.text().strip()
        if not token:
            QMessageBox.warning(self, "登录失败", "请填写令牌后再登录。")
            return

        try:
            self.api_service.login_with_token(token)
            QMessageBox.information(self, "登录成功", "令牌已保存，您已登录。")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "登录失败", str(e))
