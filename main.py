from PyQt6 import QtWidgets
from DB_connection.dbconnect import connect_to_Database

from Interface.login import Ui_Login

conn =  connect_to_Database();
if conn:
    conn.close()


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)

app = QtWidgets.QApplication([])
application = MyWindow()
application.show()
app.exec()
