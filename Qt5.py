import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, 
                           QPushButton, QLabel, QFrame, QDialog, QMessageBox,
                           QProgressBar)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QThread, pyqtSignal
import instaloader

class DownloadWorker(QThread):
    finished = pyqtSignal(bool, str, str)  # 传递下载成功或失败的消息和路径
    progress = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            L = instaloader.Instaloader()
            shortcode = self.url.split('/')[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)

            # 获取当前工作目录
            current_dir = os.getcwd()  # 获取程序所在的当前目录
            user_folder = os.path.join(current_dir, "InsDownload")  # 在当前目录创建 InsDownload 文件夹
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            # 获取发布日期，拼接文件夹
            post_date = post.date.strftime('%Y%m%d')
            post_folder = os.path.join(user_folder, f"{post_date}_{post.shortcode}")
            if not os.path.exists(post_folder):
                os.makedirs(post_folder)

            # 获取绝对路径
            post_folder = os.path.abspath(post_folder)
            print(f"目标路径：{post_folder}")  # 调试输出

            # 下载帖子
            self.progress.emit("正在下载...")
            L.download_post(post, target=post_folder)  # 使用绝对路径
            self.finished.emit(True, f"下载成功: {post.owner_username} 的帖子", post_folder)
            
        except Exception as e:
            self.finished.emit(False, f"下载失败: {str(e)}", "")

class DownloadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("下载提示")
        self.setFixedSize(400, 200)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.status_label = QLabel("正在下载中...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #1d1d1f;
                font-size: 16px;
                font-weight: 500;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #f5f5f7;
                border-radius: 10px;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #007AFF;
                border-radius: 10px;
            }
        """)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)

        info_label = QLabel("下载过程中界面可能暂时无响应\n这是正常现象，请耐心等待")
        info_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 13px;
            }
        """)
        info_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(info_label)
        
        self.setLayout(layout)

    def update_status(self, message):
        self.status_label.setText(message)

class ModernButton(QPushButton):
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"geometry")
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 20px;
                font-family: -apple-system;
                font-size: 14px;
                font-weight: 500;
                padding: 12px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
            QPushButton:pressed {{
                background-color: {color}aa;
            }}
        """)

    def enterEvent(self, event):
        self._animation.setDuration(100)
        self._animation.setEndValue(QRect(self.x()-2, self.y()-2, 
                                        self.width()+4, self.height()+4))
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDuration(100)
        self._animation.setEndValue(QRect(self.x()+2, self.y()+2, 
                                        self.width()-4, self.height()-4))
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        self._animation.start()
        super().leaveEvent(event)

class ModernInput(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #f5f5f5;
                border: 2px solid #e0e0e0;
                border-radius: 20px;
                padding: 12px 20px;
                font-family: -apple-system;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #007AFF;
                background-color: white;
            }
        """)

class ModernFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 25px;
                border: 1px solid #e0e0e0;
            }
        """)

class InstagramDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Instagram 下载器")
        self.setGeometry(100, 100, 480, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: -apple-system;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        container = ModernFrame()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(20)

        title = QLabel("Instagram 下载器")
        title.setStyleSheet("""
            QLabel {
                color: #1d1d1f;
                font-size: 24px;
                font-weight: bold;
                padding-bottom: 10px;
            }
        """)
        container_layout.addWidget(title, 0, Qt.AlignHCenter)

        self.url_input = ModernInput("请输入 Instagram 分享链接")
        container_layout.addWidget(self.url_input)

        self.download_button = ModernButton("下载", "#007AFF")
        self.download_button.clicked.connect(self.download_media)
        container_layout.addWidget(self.download_button)

        self.status_label = QLabel("准备就绪")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 13px;
                padding: 10px;
                background-color: #f5f5f7;
                border-radius: 10px;
            }
        """)
        self.status_label.setWordWrap(True)
        container_layout.addWidget(self.status_label)

        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def download_media(self):
        url = self.url_input.text()
        if not url:
            self.show_error("请输入有效的 Instagram 链接！")
            return

        self.dialog = DownloadDialog(self)
        self.dialog.setWindowModality(Qt.WindowModal)
        
        self.worker = DownloadWorker(url)
        self.worker.progress.connect(self.dialog.update_status)
        self.worker.finished.connect(self.download_finished)
        
        self.worker.start()
        self.dialog.exec_()

    def download_finished(self, success, message, download_folder):
        self.dialog.close()
        if success:
            self.show_success(message, download_folder)
        else:
            self.show_error(message)

    def show_error(self, message):
        self.status_label.setText(message)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #FF3B30;
                font-size: 13px;
                padding: 10px;
                background-color: #fff2f2;
                border-radius: 10px;
            }
        """)

    def show_success(self, message, download_folder):
        self.status_label.setText(message)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #34C759;
                font-size: 13px;
                padding: 10px;
                background-color: #f0fff0;
                border-radius: 10px;
            }
        """)

        # 在下载完成后弹出对话框提醒用户
        QMessageBox.information(self, "下载完成", f"下载已完成！文件保存在：\n{download_folder}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstagramDownloaderApp()
    window.show()
    sys.exit(app.exec_())
