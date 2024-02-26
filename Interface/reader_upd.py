from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QMessageBox
from DB_connection.dbconnect import connect_to_Database
from SQl_files.sqls import get_headers, get_reader_menu_table


class Ui_Reader(object):
    def setupUi(self, Reader):
        Reader.setObjectName("Reader")
        Reader.resize(976, 486)
        self.centralwidget = QtWidgets.QWidget(parent=Reader)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(600, 70, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(600, 30, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.lineLAST_NAME = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineLAST_NAME.setGeometry(QtCore.QRect(700, 70, 241, 21))
        self.lineLAST_NAME.setObjectName("lineLAST_NAME")

        self.lineFIRST_NAME = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineFIRST_NAME.setGeometry(QtCore.QRect(700, 30, 241, 21))
        self.lineFIRST_NAME.setObjectName("lineFIRST_NAME")

        self.buttonHistory = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonHistory.setGeometry(QtCore.QRect(600, 120, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.buttonHistory.setFont(font)
        self.buttonHistory.setObjectName("buttonHistory")

        #ИСТОРИЯ ЧИТАТЕЛЯ
        self.buttonHistory.clicked.connect(self.books_history)

        self.popularBooks = QtWidgets.QPushButton(parent=self.centralwidget)
        self.popularBooks.setGeometry(QtCore.QRect(600, 170, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.popularBooks.setFont(font)
        self.popularBooks.setObjectName("pushButton_3")

        #ТОП 3 КНИГИ ПО БИЛИОТЕКЕ
        self.popularBooks.clicked.connect(self.top_books)

        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 20, 571, 441))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 569, 439))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.tableView = QtWidgets.QTableView(parent=self.scrollAreaWidgetContents)
        self.tableView.setGeometry(QtCore.QRect(0, 0, 571, 451))
        self.tableView.setObjectName("tableView")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(780, 120, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        #КОЛ-ВО КНИГ
        self.pushButton_3.clicked.connect(self.cnt_books)

        self.showFine = QtWidgets.QPushButton(parent=self.centralwidget)
        self.showFine.setGeometry(QtCore.QRect(780, 170, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.showFine.setFont(font)
        self.showFine.setObjectName("pushButton_3")

        #ШТРАФЫ
        self.showFine.clicked.connect(self.show_fine)


        self.pushButton_5 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(910, 450, 61, 31))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("COLOR:BLACK;")
        self.pushButton_5.setObjectName("pushButton_5")

        # EXIT
        self.pushButton_5.clicked.connect(self.exit)

        Reader.setCentralWidget(self.centralwidget)

        self.retranslateUi(Reader)
        QtCore.QMetaObject.connectSlotsByName(Reader)

    def retranslateUi(self, Reader):
        _translate = QtCore.QCoreApplication.translate
        Reader.setWindowTitle(_translate("Reader", "Reader"))
        self.label_2.setText(_translate("Reader", "Фамилия"))
        self.label_3.setText(_translate("Reader", "Имя"))
        self.buttonHistory.setText(_translate("Reader", "История"))
        self.pushButton_3.setText(_translate("Reader", "Количество книг"))
        self.pushButton_5.setText(_translate("Reader", "EXIT"))
        self.showFine.setText(_translate("Reader", "Штраф"))
        self.popularBooks.setText(_translate("Reader", "ТОП книг"))
    def exit(self):
        self.centralwidget.window().close()

    def top_books(self):
        self.books('popular_books()')
    def show_fine(self):
        self.books('sum_fines_in_period()')
    def books_history(self):
        self.books('books_and_readers')
    def cnt_books(self):
        self.books('readers_and_count_of_books')

    def books(self, table_name):
        last = self.lineLAST_NAME.text()
        first = self.lineFIRST_NAME.text()

        try:
            column_names = get_headers(table_name)
            result = get_reader_menu_table(table_name,last,first )

            # Отображаем результат в tableView
            self.display_result_in_table(result,column_names)

        except Exception as e:
            QMessageBox.warning(None, "Warning", f"Failed to load table data: {str(e)}")

    def display_result_in_table(self, result, headers):
        self.tableView.setModel(None)

        # Создаем модель для отображения данных в tableView
        model = QStandardItemModel()

        model.setHorizontalHeaderLabels(headers)

        # Добавляем данные в модель
        for row in result:
            items = [QStandardItem(str(item)) for item in row]
            model.appendRow(items)

        self.tableView.setModel(model)

        # Растягиваем таблицу по ширине и высоте
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableView.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Растягиваем содержимое по размерам контента
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()

        # Устанавливаем растягивание последнего столбца по горизонтали
        last_column = len(headers) - 1
        self.tableView.horizontalHeader().setSectionResizeMode(last_column, QtWidgets.QHeaderView.ResizeMode.Stretch)
