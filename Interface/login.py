from PyQt6 import QtCore, QtGui, QtWidgets
import hashlib
from PyQt6.QtWidgets import QMessageBox
from DB_connection.dbconnect import connect_to_Database
from Interface.menu import Ui_MenuWindow
from SQl_files.sqls import get_pass


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(400, 274)
        Login.setStyleSheet("background-color:lightgray;")
        self.centralwidget = QtWidgets.QWidget(parent=Login)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 361, 251))
        self.groupBox.setStyleSheet("background-color:white;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(40, 90, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(40, 130, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(110, 90, 201, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 130, 201, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(parent=self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(140, 190, 75, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.check_login)

        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setGeometry(QtCore.QRect(130, 40, 300, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        Login.setCentralWidget(self.centralwidget)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Login"))
        self.label_2.setText(_translate("Login", "Логин"))
        self.label_3.setText(_translate("Login", "Пароль"))
        self.pushButton.setText(_translate("Login", "Войти"))
        self.label.setText(_translate("Login", "Вход в систему"))

    def check_login(self):
        input_login = self.lineEdit.text()
        input_password = self.lineEdit_2.text()
        try:
            # Создаем новое соединение и курсор

            result = get_pass(input_login)

            if result:
                input_password_hash = hashlib.md5(input_password.encode()).hexdigest()
                hashed_password_from_DB = result[0][0]

                key_permission = result[0][1]
                if input_password_hash == hashed_password_from_DB:
                    QMessageBox.information(None, "Success", "Authentication successfully.")
                    # Создаем экземпляр класса Ui_MenuWindow
                    self.menu_window = Ui_MenuWindow()

                    # Создаем окно MenuWindow на основе Ui_MenuWindow
                    self.menu_window_window = QtWidgets.QMainWindow()
                    self.menu_window.setupUi(self.menu_window_window, permission_key=key_permission, login=input_login)

                    # Показываем окно MenuWindow
                    self.menu_window_window.show()

                    # Закрываем текущее окно входа
                    self.centralwidget.window().close()
                else:
                    QMessageBox.warning(None, "Warning", "Wrong login or password. Check input data!")
            else:
                QMessageBox.warning(None, "Warning", "Wrong login or password. Check input data!")
        except Exception as e:
            QMessageBox.warning(None, "Warning", f"Something went wrong: {str(e)}")
            print(str(e))
