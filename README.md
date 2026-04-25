# ChmlFrp Node Speed Test - Python Version

<div align="center">

**快速测试节点延迟，帮助用户选择最优节点**

[![License](https://img.shields.io/github/license/zhengddzz/ChmlFrp-NodeSpeedTest)](LICENSE)

</div>

---

## ✨ 核心功能

### 🔍 节点自动探测
支持调用 API 扫描 ChmlFrp 可用节点列表，快速获取节点的基础信息（如节点地区、运营商、在线状态），无需手动查询。

### 🎯 多维度筛选
提供 VIP 节点、国内国外、UDP 支持等筛选条件，用户可根据自身网络环境和需求，精准定位符合要求的节点，提高效率。

### ⚡ 节点测速评估
内置本地简单测速功能，对筛选后的节点进行延迟和下载速度检测，直观展示本地到节点的连接质量，辅助选择最优节点。

### 📌 其他特性
- **结果持久化** - 测试结果自动保存
- **批量测试** - 支持批量测试多个节点
- **历史记录** - 查看节点测试历史

## 📥 安装运行

### 依赖要求
- Python 3.7+
- PyQt5
- requests

### 安装步骤
1. 克隆或下载项目
2. 安装依赖：
```bash
pip install -r requirements.txt
```
3. 运行应用：
```bash
python main.py
```

## 🛠️ 技术栈

- **GUI**: PyQt5
- **网络**: requests
- **打包**: PyInstaller

## 📁 项目结构

```
├── main.py                 # 程序入口
├── gui/                    # GUI组件
│   ├── main_window.py      # 主窗口
│   ├── widgets/           # 基础组件
│   ├── pages/             # 页面组件
│   └── dialogs/           # 对话框
├── services/              # 业务服务
│   ├── api_service.py     # API服务
│   └── speed_test_service.py  # 测速服务
├── config.json            # 配置文件
└── requirements.txt       # 依赖文件
```
- **后端**: Rust + Tauri
- **构建**: GitHub Actions

## 📝 开发

```bash
# 安装依赖
pnpm install

# 开发模式
pnpm tauri dev

# 构建
pnpm tauri build
```

## 🌿 分支管理

| 分支 | 说明 |
|------|------|
| `main` | 生产分支，稳定版本代码 |
| `develop` | 开发分支，日常开发在此进行 |

### 提交规范

请遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复 Bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `chore:` 构建/工具变更

### 合并到生产分支

当 `develop` 分支开发完成并测试通过后，合并到 `main` 分支：

```bash
# 切换到生产分支
git checkout main

# 合并开发分支
git merge develop

# 推送到远程
git push origin main
```

合并后会自动触发 GitHub Actions 构建并发布新版本。

## 📄 许可证

[MIT License](LICENSE)

## 🙏 致谢

- [Tauri](https://tauri.app/) - 跨平台桌面应用框架
- [ChmlFrp](https://chmlfrp.cn/) - 免费内网穿透服务
