import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                            QFileDialog, QMessageBox, QCheckBox, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
import subprocess
import re

class GitHubCloneGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitHub仓库克隆工具")
        self.setMinimumSize(600, 280)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title_label = QLabel("GitHub仓库克隆工具")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # 仓库URL输入
        url_layout = QHBoxLayout()
        url_label = QLabel("仓库URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入GitHub仓库URL (例如: https://github.com/用户名/仓库名.git)")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # 目标目录选择
        dir_layout = QHBoxLayout()
        dir_label = QLabel("目标目录:")
        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("选择克隆目标目录")
        self.browse_button = QPushButton("浏览...")
        self.browse_button.clicked.connect(self.browse_directory)
        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(self.browse_button)
        layout.addLayout(dir_layout)

        # 代理选项
        proxy_layout = QHBoxLayout()
        self.proxy_checkbox = QCheckBox("使用代理加速")
        self.proxy_checkbox.setChecked(True)  # 默认启用代理
        self.proxy_combo = QComboBox()
        self.proxy_combo.addItems([
            "https://mirror.ghproxy.com/",
            "https://ghproxy.com/",
            "https://gh.api.99988866.xyz/"
        ])
        proxy_layout.addWidget(self.proxy_checkbox)
        proxy_layout.addWidget(self.proxy_combo)
        layout.addLayout(proxy_layout)

        # 克隆按钮
        self.clone_button = QPushButton("开始克隆")
        self.clone_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.clone_button.clicked.connect(self.clone_repository)
        layout.addWidget(self.clone_button)

        # 状态标签
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

    def browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择目标目录")
        if dir_path:
            self.dir_input.setText(dir_path)

    def get_repo_name(self, url):
        """从URL中提取仓库名称"""
        # 移除代理前缀（如果有）
        for proxy in ["mirror.ghproxy.com/", "ghproxy.com/", "gh.api.99988866.xyz/"]:
            if proxy in url:
                url = url.split("github.com/", 1)[1]
                break
        else:
            url = url.split("github.com/", 1)[-1]
        # 移除.git后缀
        url = url.rstrip('.git')
        # 获取最后一个/后的内容作为仓库名
        return url.split('/')[-1]

    def get_clone_url(self, url):
        """处理克隆URL，根据是否使用代理返回最终的URL"""
        # 确保URL格式正确
        if not url.startswith(('http://', 'https://')):
            url = 'https://github.com/' + url
        
        # 如果URL不包含.git后缀，添加它
        if not url.endswith('.git'):
            url = url + '.git'

        if self.proxy_checkbox.isChecked():
            # 移除可能存在的其他代理前缀
            for proxy in ["mirror.ghproxy.com/", "ghproxy.com/", "gh.api.99988866.xyz/"]:
                if proxy in url:
                    url = url.replace(proxy, "")
            
            # 添加选择的代理
            selected_proxy = self.proxy_combo.currentText()
            if "github.com" in url:
                return f"{selected_proxy}{url}"
        return url

    def clone_repository(self):
        url = self.url_input.text().strip()
        target_dir = self.dir_input.text().strip()

        if not url:
            QMessageBox.warning(self, "错误", "请输入GitHub仓库URL")
            return

        try:
            # 获取仓库名称和处理后的URL
            repo_name = self.get_repo_name(url)
            clone_url = self.get_clone_url(url)
            
            if target_dir:
                # 检查目标目录是否存在
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                # 检查目标目录中是否已存在同名项目
                potential_repo_path = os.path.join(target_dir, repo_name)
                if os.path.exists(potential_repo_path):
                    QMessageBox.warning(self, "错误", f"目标目录已存在名为 {repo_name} 的文件夹！")
                    return
                
                os.chdir(target_dir)

            self.status_label.setText(f"正在克隆仓库: {url}")
            self.status_label.setStyleSheet("color: blue")
            QApplication.processEvents()

            # 显示正在使用的URL
            print(f"克隆URL: {clone_url}")
            
            result = subprocess.run(['git', 'clone', clone_url], 
                                  capture_output=True, 
                                  text=True)
            
            if result.returncode != 0:
                raise subprocess.CalledProcessError(
                    result.returncode, 
                    ['git', 'clone'], 
                    result.stdout, 
                    result.stderr
                )
            
            self.status_label.setText("克隆完成！")
            self.status_label.setStyleSheet("color: green")
            QMessageBox.information(self, "成功", "仓库克隆成功！")

        except subprocess.CalledProcessError as e:
            error_msg = f"克隆失败:\n{e.stderr if e.stderr else str(e)}"
            self.status_label.setText("克隆失败")
            self.status_label.setStyleSheet("color: red")
            QMessageBox.critical(self, "错误", error_msg)
            
            # 如果是代理问题，提示切换代理
            if "unable to access" in str(e) or "connection reset" in str(e).lower():
                QMessageBox.information(
                    self, 
                    "提示", 
                    "连接似乎出现问题，建议尝试:\n1. 切换其他代理\n2. 暂时关闭代理\n3. 检查网络连接"
                )
        except Exception as e:
            self.status_label.setText(f"发生错误: {e}")
            self.status_label.setStyleSheet("color: red")
            QMessageBox.critical(self, "错误", f"发生错误: {e}")

def main():
    app = QApplication(sys.argv)
    window = GitHubCloneGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()