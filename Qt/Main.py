import base64

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot, QTimer
import cv2
from PyQt5.QtGui import QImage, QPixmap

from UserHolder import UserHolder, User
from page import login, register, homepage
import sys
from sqlUtils import sqlUtils
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QButtonGroup, QFileDialog

from EnterPoint import run_api, identify


class Login(QMainWindow, login.Ui_login_MainWindow):
    # 初始化UI
    def __init__(self):
        super(Login, self).__init__()
        self.homePage = None
        self.PageOfRegister = None
        self.initUI()

    # 装载UI 并绑定事件
    def initUI(self):
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.changePage)
        self.pushButton.clicked.connect(self.login)
        self.lineEdit_2.returnPressed.connect(self.login)

    # 页面跳转事件 关闭本窗口
    def changePage(self):
        self.hide()
        self.PageOfRegister = Register()
        self.PageOfRegister.show()

    # 登录事件
    def login(self):
        user = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if user != "" and password != "":
            result, now_user = sqlUtils.Login((user, password))
            if result == 1:
                self.homePage = HomePage()
                # 数据持久化 不保存密码
                userDTO = User(now_user[0], now_user[1], now_user[3], now_user[4])
                UserHolder.saveUser(user=userDTO)
                self.homePage.show()
                self.close()
            else:
                QMessageBox.critical(self, "错误", "账号或密码错误")
        else:
            QMessageBox.critical(self, "错误", "请正确输入！")


class Register(QMainWindow, register.Ui_register_MainWindow):
    # 初始化UI
    def __init__(self):
        super(Register, self).__init__()
        self.PageOfLogin = None
        self.initUI()

    # 装载UI 并绑定事件
    def initUI(self):
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.changePage)
        self.pushButton.clicked.connect(self.register)

    # 页面跳转事件 关闭本窗口 打开登录窗口
    def changePage(self):
        self.PageOfLogin = Login()
        self.PageOfLogin.show()
        self.hide()

    # 注册事件
    def register(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        confirmPassword = self.lineEdit_3.text()
        if username != "" and password != "" and confirmPassword != "":
            if password == confirmPassword:
                result = sqlUtils.register((username, password))
                if result == 1:
                    QMessageBox.information(self, '消息', '注册成功请返回登录', QMessageBox.Yes)
                else:
                    QMessageBox.critical(self, "错误", "注册失败！请重试")
            else:
                QMessageBox.critical(self, "错误", "两次输入不一致！")
        else:
            QMessageBox.critical(self, "错误", "请正确输入！")


class HomePage(QMainWindow, homepage.Ui_homePage_MainWindow):
    # 初始化UI
    def __init__(self):
        super(HomePage, self).__init__()
        self.camera_opened = None
        self.tableWidgets = None
        self.init()
        self.cap = None

    # 装在UI并且绑定事件
    def init(self):
        self.setupUi(self)
        # 页面跳转槽函数
        self.home_button.clicked.connect(self.changePage)
        self.identify_button.clicked.connect(self.changePage)
        self.information_button.clicked.connect(self.changePage)
        self.app_button.clicked.connect(self.changePage)
        self.stackedWidget.currentChanged.connect(self.close_video_when_change)
        # 定义视频流刷新定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        # 每次点击信息按钮更新UserHolder
        self.information_button.clicked.connect(self.solve_show_uploaded_content)
        self.api = run_api.run()

    # 主页堆栈窗口跳转函数
    def changePage(self):
        sender = self.sender().objectName()  # 获取当前信号 sender
        index = {
            'home_button': 0,
            'identify_button': 1,
            'information_button': 2,
            'app_button': 3,
        }
        self.stackedWidget.setCurrentIndex(index[sender])  # 根据信号 index 设置所显示的页面

    # 人脸识别 开始检测槽函数
    @pyqtSlot()
    def on_identify_start_button_clicked(self):
        """
        Open video input and start mask detect
        """
        # 使用 cv2.CAP_DSHOW 标识符可以让 VideoCapture API 使用 DirectShow API 来访问摄像头设备，从而解决一些摄像头在使用 VideoCapture 时可能遇到的问题，
        # 例如设备驱动不稳定、分辨率设置问题等等。
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.timer.start(30)
        self.camera_opened = True

    # 人脸识别 结束检测 槽函数
    @pyqtSlot()
    def on_identify_exit_button_clicked(self):
        """
        Close video input
        """
        self.timer.stop()
        self.cap.release()
        self.vedio_label.setText("Waiting open your camera...")

    @pyqtSlot()
    def on_identify_compare_button_clicked(self):
        """
        Compared with the face information in the database
        """
        if not self.camera_opened:  # 如果摄像头未打开，则返回
            print('error')
            return
        ret, frame = self.cap.read()
        if ret:
            retval, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            def get_current_user():
                user = UserHolder.getUser()
                username = user.username
                return username
            identify.main(jpg_as_text, get_current_user())
            print(identify.main(jpg_as_text, get_current_user()))
        else:
            print('error')

    # 视频流定时更新渲染函数
    def update_frame(self):
        frame = run_api.run()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.vedio_label.setPixmap(pixmap)

    # 解决页面跳转的时候 没有手动关闭视频流的问题
    def close_video_when_change(self, index):
        if index != 1:
            if self.cap is not None:
                self.timer.stop()
                self.cap.release()
                self.vedio_label.setText("Waiting open your camera...")

    # 上传文件
    @pyqtSlot()
    def on_upload_img_clicked(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\', 'Image files (*.jpg *.png *.jpeg)')

        if fileName:
            print(fileName)  # todo 此处参数fileName即为上传头像的本地路径
            pix = QPixmap(fileName).scaled(221, 250, QtCore.Qt.KeepAspectRatio)
            self.uploaded_img.setPixmap(pix)  # 渲染到QLabel
            # 以rb模式打开文件
            file = open(fileName, "rb")
            data = file.read()
            file.close()
            # 转换图片为base64
            self.b64_string = base64.b64encode(data).decode('utf-8')

    @pyqtSlot()
    def on_upload_button_ok_clicked(self):
        # 获取输入的name
        name = self.lineEdit.text()
        # 获取当前用户
        now_user = UserHolder.getUser()
        # 保存base64编码和用户名到数据库
        is_success = sqlUtils.save_photo_name(self.b64_string, now_user.userId, name)
        if is_success:
            QMessageBox.information(self, '消息', '上传成功', QMessageBox.Yes)
        else:
            QMessageBox.critical(self, "错误", "上传失败，请重试！")

    # 已经存在显示图片
    def solve_show_uploaded_content(self):
        # 更新当前的UserHolder
        result, now_user = sqlUtils.update_userHolder(UserHolder.getUser().userId)
        userDTO = User(now_user[0], now_user[1], now_user[3], now_user[4])
        UserHolder.saveUser(user=userDTO)
        # 获取最新的User
        now_user = UserHolder.getUser()
        # 判断photo和name字段是否存在
        if len(now_user.photo) != 0 or len(now_user.name) != 0:
            # 都存在 需要展示 调用show_content_if_uploaded函数
            img_str = now_user.photo
            imgdata = base64.b64decode(img_str)  # 解码字符串
            pixmap = QPixmap()  # 创建一个QPixmap对象
            pixmap.loadFromData(imgdata)  # 从二进制数据加载图片
            pixmap = pixmap.scaled(221, 250, QtCore.Qt.KeepAspectRatio)  # 缩放
            self.uploaded_img.setPixmap(pixmap)  # 渲染到QLabel
            # 名字的回显
            self.lineEdit.setText(now_user.name)
        # 都不存在 不做操作


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 创建页面实例
    PageOfLogin = Login()
    # 登录页面的show
    PageOfLogin.show()
    sys.exit(app.exec_())
