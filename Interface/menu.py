
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView
from DB_connection.dbconnect import connect_to_Database

from Interface.export import Ui_Export
from Interface.reader_upd import Ui_Reader
from SQl_files.sqls import get_headers, print_table, select_where_id, update_table, insert_table, delete_from_table


class Ui_MenuWindow(object):
    def setupUi(self, MenuWindow, permission_key, login):

        MenuWindow.setObjectName("MenuWindow")
        MenuWindow.resize(1024, 558)
        MenuWindow.setStyleSheet("\n""color: white;")
        self.centralwidget = QtWidgets.QWidget(parent=MenuWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(20, 40, 821, 451))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 819, 449))
        self.scrollAreaWidgetContents.setStyleSheet("background-color:white;color:black;")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.tableWidget = QtWidgets.QTableWidget(parent=self.scrollAreaWidgetContents)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 821, 451))

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.tableWidget.setSizePolicy(size_policy)

        self.tableWidget.setStyleSheet("background-color:white;")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.comboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(860, 40, 151, 31))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)

        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("COLOR:BLACK;")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.buttonADD = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonADD.setGeometry(QtCore.QRect(860, 100, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.buttonADD.setFont(font)
        self.buttonADD.setStyleSheet("COLOR:BLACK;")
        self.buttonADD.setObjectName("pushButton")
        #ДОБАВЛЕНИЕ ЗАПИСИ
        self.buttonADD.clicked.connect(self.add_transaction)

        self.buttonCOMMIT = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonCOMMIT.setGeometry(QtCore.QRect(860, 150, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.buttonCOMMIT.setFont(font)
        self.buttonCOMMIT.setStyleSheet("COLOR:BLACK;")
        self.buttonCOMMIT.setObjectName("pushButton_2")
        #СОХРАНЯЕМ ИЗМЕНЕНИЯ В БАЗЕ ДАННЫХ
        self.buttonCOMMIT.clicked.connect(self.save_changes_to_database)

        self.buttonDELETE = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonDELETE.setGeometry(QtCore.QRect(860, 200, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.buttonDELETE.setFont(font)
        self.buttonDELETE.setStyleSheet("COLOR:BLACK;")
        self.buttonDELETE.setObjectName("pushButton_3")
        # УДАЛЯЕМ ДАННЫЕ
        self.buttonDELETE.clicked.connect(self.delete_selected_rows)

        self.buttonREADERFOUND = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonREADERFOUND.setGeometry(QtCore.QRect(860, 300, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.buttonREADERFOUND.setFont(font)
        self.buttonREADERFOUND.setStyleSheet("COLOR:BLACK;")
        self.buttonREADERFOUND.setObjectName("pushButton_6")
        # ЧИТАТЕЛЬСКИЙ БИЛЕТ
        self.buttonREADERFOUND.clicked.connect(self.reader_ticket_build)

        self.buttonEXIT = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonEXIT.setGeometry(QtCore.QRect(960, 520, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.buttonEXIT.setFont(font)
        self.buttonEXIT.setStyleSheet("COLOR:BLACK;")
        self.buttonEXIT.setObjectName("pushButton_4")
        # ВЫХОД
        self.buttonEXIT.clicked.connect(self.exit)

        self.buttonEXPORT = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonEXPORT.setGeometry(QtCore.QRect(860, 250, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.buttonEXPORT.setFont(font)
        self.buttonEXPORT.setStyleSheet("COLOR:BLACK;")
        self.buttonEXPORT.setObjectName("pushButton_5")
        #ЭКСПОРТ ТАБЛИЦЫ
        self.buttonEXPORT.clicked.connect(self.export_table)

        MenuWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MenuWindow)
        QtCore.QMetaObject.connectSlotsByName(MenuWindow)

        #выводим таблицу
        self.load_table_data()
        self.comboBox.currentIndexChanged.connect(self.load_table_data)

        self.login = login
        self.permission_key = permission_key

        self.setup_controls()

    # Устанавливаем доступность элементов в зависимости от permission_key
    def setup_controls(self):
        if self.permission_key == "r":
            self.buttonADD.setEnabled(False)
            self.buttonCOMMIT.setEnabled(False)
            self.buttonDELETE.setEnabled(False)

            for row in range(self.tableWidget.rowCount()):
                for col in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, col)
                    if item:
                        flags = item.flags()
                        flags &= ~QtCore.Qt.ItemFlag.ItemIsEditable
                        item.setFlags(flags)
    def retranslateUi(self, MenuWindow):
        _translate = QtCore.QCoreApplication.translate
        MenuWindow.setWindowTitle(_translate("MenuWindow", "Menu"))
        self.comboBox.setItemText(0, _translate("MenuWindow", "JOURNAL"))
        self.comboBox.setItemText(1, _translate("MenuWindow", "CLIENTS"))
        self.comboBox.setItemText(2, _translate("MenuWindow", "BOOK_TYPES"))
        self.comboBox.setItemText(3, _translate("MenuWindow", "BOOKS"))
        self.buttonADD.setText(_translate("MenuWindow", "Добавить строку"))
        self.buttonCOMMIT.setText(_translate("MenuWindow", "Сохранить"))
        self.buttonDELETE.setText(_translate("MenuWindow", "Удалить"))
        self.buttonEXIT.setText(_translate("MenuWindow", "EXIT"))
        self.buttonEXPORT.setText(_translate("MenuWindow", "Экспорт"))

        self.buttonREADERFOUND.setText(_translate("MenuWindow", "Читатели"))

    def load_table_data(self):
        selected_table = self.comboBox.currentText()

        try:
            column_names = get_headers(selected_table)

            self.tableWidget.setColumnCount(len(column_names))
            self.tableWidget.setHorizontalHeaderLabels(column_names)

            #Устанавливаем растягивание столбцов по содержимому
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            result = print_table(selected_table)

            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)

            # Получаем количество столбцов и строк
            column_count = len(column_names)
            row_count = len(result)

            # Устанавливаем количество строк в таблице
            self.tableWidget.setRowCount(row_count)

            # Заполняем таблицу данными из запроса
            for row_idx, row_data in enumerate(result):
                for col_idx, cell_data in enumerate(row_data):
                    if cell_data is None:
                        cell_data = 'NULL'

                    item = QTableWidgetItem(str(cell_data))
                    self.tableWidget.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.warning(None, "Warning", f"Failed to load table data: {str(e)}")

    def add_transaction(self):
        try:
            current_row_count = self.tableWidget.rowCount()
            self.tableWidget.insertRow(current_row_count)

            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(current_row_count, col)
                if item is None or item.text().strip() == '' or item.text().strip() == 'NULL':
                    # Если ячейка пуста, устанавливаем значение в None
                    self.tableWidget.setItem(current_row_count, col, QTableWidgetItem('NULL'))
        except Exception as e:
            QMessageBox.warning(None, "Предупреждение", f"Не удалось загрузить данные таблицы: {str(e)}")
            print(str(e))

    def get_table_data(self):
        # Получаем данные из таблицы

        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()

        table_data = []

        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.tableWidget.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            table_data.append(row_data)

        return table_data

    def save_changes_to_database(self):
        selected_table = self.comboBox.currentText()
        try:
            # Получаем имена колонок из таблицы, исключая те, у которых значения NULL
            column_names = [self.tableWidget.horizontalHeaderItem(col_idx).text()
                            for col_idx in range(self.tableWidget.columnCount())]

            table_data = self.get_table_data()

            for row_data in table_data:
                values = [val if val and val.lower() != 'null' else f'{val}' for val in row_data]
                placeholders = ', '.join(f'\'{val}\'' if val and val.lower() != 'null' and val != '' else 'NULL' for val in values)

                set_values = ', '.join(
                    [f'{col} = \'{val}\'' if val.lower() != 'null' and  val!=' '  else f'{col} = NULL' for col, val in
                     zip(column_names, values)])

                existing_record = select_where_id(id = values[0], table = selected_table)

                if existing_record:
                    update_table(table = selected_table, set_values = set_values, values = values)
                else:
                    insert_table(table = selected_table, headers = ', '.join(column_names), placeholders = placeholders)

            self.load_table_data()
        except Exception as e:
            QMessageBox.warning(None, "Warning", f"Failed to save changes: {str(e)}")
            self.load_table_data()

    def delete_selected_rows(self):
        selected_table = self.comboBox.currentText()
        selected_rows = self.tableWidget.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(None, "Warning", "No rows selected for deletion.")
            return

        try:
            for row in selected_rows:
                row_id = self.tableWidget.item(row.row(), 0).text()  #Предполагаем, что ID находится в первом столбце

                delete_from_table(selected_table, row_id)

            self.load_table_data()
        except Exception as e:
            QMessageBox.warning(None, "Warning", f"Failed to delete rows: {str(e)}")

    def export_table(self):
        selected_table = self.comboBox.currentText()

        self.export_window = Ui_Export()

        # Создаем окно MenuWindow на основе Ui_MenuWindow
        self.menu_window_window = QtWidgets.QMainWindow()
        self.export_window.setupUi(self.menu_window_window, table = selected_table)

        # Показываем окно MenuWindow
        self.menu_window_window.show()

    def exit(self):
        self.centralwidget.window().close()

    def reader_ticket_build(self):
        # Создаем экземпляр класса Ui_MenuWindow
        self.reader_window = Ui_Reader()

        # Создаем окно MenuWindow на основе Ui_MenuWindow
        self.menu_window_window = QtWidgets.QMainWindow()
        self.reader_window.setupUi(self.menu_window_window)

        # Показываем окно MenuWindow
        self.menu_window_window.show()
