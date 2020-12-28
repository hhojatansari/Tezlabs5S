from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import json
import shutil
from utils.logger import Logger


ext_dict = {
    "Images": ['JPG', 'PNG', 'GIF', 'WEBP', 'TIFF', 'BMP', 'INDD', 'JPEG', 'SVG', 'ICO'],
    "Audios": ['M4A', 'MP3', 'FLAC', 'WMA', 'AAC'],
    "Videos": ['WEBM', 'AVI', 'MOV', 'MKV', 'FLV', 'MP4'],
    "Documents": ['PDF', 'XLSX', 'XLSM', 'XLSB', 'XLTX', 'DOT', 'DOTX', 'DOCX', 'PPTX', 'PPT', 'PPS'],
    "Programs": ['EXE', 'MSI', 'BAT']
}


class Ui_MainWindow(object):
    def __init__(self):
        self.log = Logger()
        self.items_dict = {}
        self.dialog_browser = QtWidgets.QFileDialog()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.gb_add_item = QtWidgets.QGroupBox(self.centralwidget)
        self.lw_items = QtWidgets.QListWidget(self.centralwidget)
        self.cb_ext = QtWidgets.QComboBox(self.gb_add_item)
        self.btn_from = QtWidgets.QPushButton(self.gb_add_item)
        self.btn_to = QtWidgets.QPushButton(self.gb_add_item)
        self.btn_remove = QtWidgets.QPushButton(self.gb_add_item)
        self.btn_add = QtWidgets.QPushButton(self.gb_add_item)
        self.btn_apply = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exit = QtWidgets.QPushButton(self.centralwidget)
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.te_item_name = QtWidgets.QTextEdit(self.gb_add_item)
        self.te_ext = QtWidgets.QTextEdit(self.gb_add_item)
        self.te_to = QtWidgets.QTextEdit(self.gb_add_item)
        self.te_from = QtWidgets.QTextEdit(self.gb_add_item)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.a_about = QtWidgets.QAction(MainWindow)
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.msg = QtWidgets.QMessageBox()
        self.load_db()

    def setup_ui(self, MainWindow):
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists('Log'):
            os.makedirs('Log')

        MainWindow.setObjectName("Tezlabs 5S")
        MainWindow.setWindowIcon(QtGui.QIcon('imgs/icon.ico'))
        MainWindow.setFixedSize(927, 499)

        self.centralwidget.setObjectName("centralwidget")

        self.btn_exit.setGeometry(QtCore.QRect(760, 390, 131, 51))
        self.btn_exit.setObjectName("btn_exit")
        self.btn_exit.clicked.connect(MainWindow.close)
        self.btn_apply.setGeometry(QtCore.QRect(40, 390, 701, 51))
        self.btn_apply.setMouseTracking(False)
        self.btn_apply.setAcceptDrops(False)
        self.btn_apply.setAutoFillBackground(True)
        self.btn_apply.setIconSize(QtCore.QSize(20, 20))
        self.btn_apply.setAutoDefault(False)
        self.btn_apply.setDefault(False)
        self.btn_apply.setFlat(False)
        self.btn_apply.setObjectName("btn_apply")
        self.btn_apply.clicked.connect(self.apply)
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.btn_add.setFont(font)
        self.btn_add.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_add.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_add.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imgs/add.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add.setIcon(icon)
        self.btn_add.setIconSize(QtCore.QSize(35, 40))
        self.btn_add.setFlat(False)
        self.btn_add.setObjectName("btn_add")
        self.btn_add.clicked.connect(self.add_item)
        self.btn_from.setGeometry(QtCore.QRect(520, 62, 31, 28))
        self.btn_from.setObjectName("btn_from")
        self.btn_from.clicked.connect(self.brows_from)
        self.btn_add.setGeometry(QtCore.QRect(761, 20, 71, 51))
        self.btn_remove.setGeometry(QtCore.QRect(760, 80, 71, 51))
        self.btn_remove.setFont(font)
        self.btn_remove.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_remove.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_remove.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("imgs/remove.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_remove.setIcon(icon1)
        self.btn_remove.setIconSize(QtCore.QSize(35, 40))
        self.btn_remove.setFlat(False)
        self.btn_remove.setObjectName("btn_remove")
        self.btn_remove.clicked.connect(self.remove_item)
        self.btn_to.setGeometry(QtCore.QRect(520, 94, 31, 28))
        self.btn_to.setObjectName("btn_to")
        self.btn_to.clicked.connect(self.brows_to)

        self.lw_items.setGeometry(QtCore.QRect(640, 31, 251, 191))
        self.lw_items.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lw_items.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.lw_items.setSelectionRectVisible(False)
        self.lw_items.setObjectName("lw_items")
        self.lw_items.itemClicked.connect(self.lw_selected)

        self.logo.setGeometry(QtCore.QRect(60, 40, 516, 186))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("imgs/logo.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")

        self.gb_add_item.setGeometry(QtCore.QRect(40, 230, 851, 141))
        self.gb_add_item.setObjectName("gb_add_item")

        self.cb_ext.setGeometry(QtCore.QRect(600, 62, 91, 28))
        self.cb_ext.setObjectName("cb_ext")
        self.cb_ext.addItem("")
        self.cb_ext.addItem("")
        self.cb_ext.addItem("")
        self.cb_ext.addItem("")
        self.cb_ext.addItem("")
        self.cb_ext.addItem("")
        self.cb_ext.currentTextChanged.connect(self.change_combo)

        self.te_ext.setGeometry(QtCore.QRect(600, 94, 91, 28))
        self.te_ext.setObjectName("te_ext")
        self.te_ext.setDisabled(True)
        self.te_item_name.setGeometry(QtCore.QRect(30, 30, 151, 28))
        self.te_item_name.setObjectName("te_item_name")
        self.te_to.setGeometry(QtCore.QRect(30, 94, 471, 28))
        self.te_to.setObjectName("te_to")
        self.te_to.setReadOnly(True)
        self.te_from.setGeometry(QtCore.QRect(30, 62, 471, 28))
        self.te_from.setObjectName("te_from")
        self.te_from.setReadOnly(True)

        self.menubar.setGeometry(QtCore.QRect(0, 0, 927, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp.setObjectName("menuHelp")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStatusBar(self.statusbar)
        MainWindow.setCentralWidget(self.centralwidget)

        self.actionAbout.setObjectName("actionAbout")
        self.a_about.setObjectName("a_about")
        self.actionLoad.setObjectName("actionLoad")
        self.menuHelp.addAction(self.a_about)
        self.menubar.addAction(self.menuHelp.menuAction())
        self.a_about.triggered.connect(self.about_dialog)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tezlabs 5S 1.0.5"))
        self.btn_exit.setText(_translate("MainWindow", "Exit"))
        __sortingEnabled = self.lw_items.isSortingEnabled()
        self.lw_items.setSortingEnabled(True)
        self.lw_items.setSortingEnabled(__sortingEnabled)
        self.btn_apply.setText(_translate("MainWindow", "Apply"))
        self.gb_add_item.setTitle(_translate("MainWindow", "Item Informations"))
        self.te_ext.setPlaceholderText(_translate("MainWindow", "extension.."))
        self.cb_ext.setItemText(0, _translate("MainWindow", "Images"))
        self.cb_ext.setItemText(1, _translate("MainWindow", "Audios"))
        self.cb_ext.setItemText(2, _translate("MainWindow", "Videos"))
        self.cb_ext.setItemText(3, _translate("MainWindow", "Documents"))
        self.cb_ext.setItemText(4, _translate("MainWindow", "Programs"))
        self.cb_ext.setItemText(5, _translate("MainWindow", "Others"))
        self.te_item_name.setPlaceholderText(_translate("MainWindow", "Item Name"))
        self.te_to.setPlaceholderText(_translate("MainWindow", "To Directory.."))
        self.te_from.setPlaceholderText(_translate("MainWindow", "From Directory.."))
        self.btn_from.setText(_translate("MainWindow", "..."))
        self.btn_to.setText(_translate("MainWindow", "..."))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.a_about.setText(_translate("MainWindow", "About"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))

    def change_combo(self, e):
        if e == 'Others':
            self.te_ext.setDisabled(False)
        else:
            self.te_ext.setDisabled(True)

    def about_dialog(self):
        self.msg.setWindowTitle('About')
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        text = """<p>This program is written by <strong>Hosein Hojat Ansari</strong>, from Tabiat Zendeh Laboratories, IT
         department.</p> <p>You can get source code  from 
         <a href="https://github.com/hhojatansari/Tezlabs5S">here</a>.</p>"""
        self.msg.setText(text)
        self.msg.exec_()

    def add_item(self):
        if (self.te_item_name.toPlainText()) and \
                (self.te_from.toPlainText()) and \
                (self.te_to.toPlainText()) and \
                (self.te_ext.toPlainText() or self.cb_ext.currentText()):
            if self.cb_ext.currentText() == 'Others':
                if self.te_ext.toPlainText():
                    name = self.te_item_name.toPlainText() + ', Others-' + '.' + ''.join(filter(str.isalpha, self.te_ext.toPlainText()))
                    ext = self.te_ext.toPlainText()
                else:
                    self.statusbar.setStyleSheet("QStatusBar{color:red;}")
                    self.statusbar.showMessage('Fill fields.', msecs=5000)
                    return
            else:
                name = self.te_item_name.toPlainText() + ', ' + self.cb_ext.currentText()
                ext = self.cb_ext.currentText()

            if name in self.items_dict.keys():
                self.statusbar.setStyleSheet("QStatusBar{color:red;}")
                self.statusbar.showMessage('Item name already exists.', msecs=5000)
                return

            self.items_dict[name] = {
                'From': self.te_from.toPlainText(),
                'To': self.te_to.toPlainText(),
                'Extension': ext
            }

            self.write_db()
            self.lw_items.addItem(name)
            self.clear_info()
        else:
            self.statusbar.setStyleSheet("QStatusBar{color:red;}")
            self.statusbar.showMessage('Fill fields.', msecs=5000)

    def remove_item(self):
        current = self.lw_items.currentRow()
        if current is not -1:
            del self.items_dict[self.lw_items.currentItem().text()]
            self.lw_items.takeItem(current)
            self.write_db()
            self.clear_info()

    def brows_from(self):
        self.te_from.setText(
            self.dialog_browser.getExistingDirectory(directory=os.environ["HOMEPATH"] + os.sep + 'Desktop',
                                                     caption='Select an awesome directory')
        )

    def brows_to(self):
        self.te_to.setText(
            self.dialog_browser.getExistingDirectory(directory=os.environ["HOMEPATH"] + os.sep + 'Desktop',
                                                     caption='Select an awesome directory')
        )

    def lw_selected(self, item):
        self.te_from.setText(self.items_dict[item.text()]['From'])
        self.te_to.setText(self.items_dict[item.text()]['To'])
        self.te_item_name.setText(item.text().split(',')[0])

        if item.text().split(',')[1].split('-')[0].strip() == 'Others':
            self.te_ext.setEnabled(True)
            self.cb_ext.setCurrentText('Others')
            self.te_ext.setText(self.items_dict[item.text()]['Extension'])
        else:
            self.te_ext.clear()
            self.te_ext.setEnabled(False)
            self.cb_ext.setCurrentText(item.text().split(',')[1].split('-')[0].strip())
            self.cb_ext.setCurrentText(self.items_dict[item.text()]['Extension'].split(',')[0])

    def clear_info(self):
        self.te_ext.clear()
        self.te_from.clear()
        self.te_to.clear()
        self.te_item_name.clear()

    def load_db(self):
        try:
            if os.path.isfile('database/Tezlabs5S.json'):
                with open('database/Tezlabs5S.json') as db:
                    self.items_dict = json.load(db)
                    for i in self.items_dict:
                        self.lw_items.addItem(i)
                self.statusbar.clearMessage()
            else:
                self.statusbar.setStyleSheet("QStatusBar{color:red;}")
                self.statusbar.showMessage("Not found database file", msecs=5000)
        except:
            self.statusbar.setStyleSheet("QStatusBar{color:red;}")
            self.statusbar.showMessage(
                "May your 'Tezlabss.json' file damaged or corrupted.. Fix it if you know JSON, or delete PLZ :(")

    def write_db(self):
        with open('database/Tezlabs5S.json', 'w') as outfile:
            json.dump(self.items_dict, outfile, sort_keys=True, indent=4)

    def apply(self):
        falg = False
        try:
            for item in self.items_dict:
                if item.split(',')[1].split('-')[0].strip() == 'Others':
                    other_ext = ''.join(filter(str.isalpha, self.items_dict[item]['Extension']))
                    for file in os.listdir(self.items_dict[item]['From']):
                        if (file.endswith('.{}'.format(other_ext.upper()))) or\
                                (file.endswith('.{}'.format(other_ext.lower()))):
                            falg = True
                            shutil.move((self.items_dict[item]['From'] + os.altsep + file).strip(),
                                  self.items_dict[item]['To'].strip() + os.altsep + file)
                            self.log.write_to_log(
                                self.items_dict[item]['From'] + os.altsep + file + ' ~> ' +
                                self.items_dict[item]['To'].strip() + os.altsep + file
                            )
                else:
                    for e in ext_dict[item.split(',')[1].strip()]:
                        list_file = []
                        for file in os.listdir(self.items_dict[item]['From']):
                            if (file.endswith('.{}'.format(e))) or (file.endswith('.{}'.format(e.lower()))):
                                falg = True
                                shutil.move((self.items_dict[item]['From'] + os.altsep + file).strip(),
                                          self.items_dict[item]['To'].strip() + os.altsep + file)
                                self.log.write_to_log(
                                    (self.items_dict[item]['From'] + os.altsep + file).strip() + ' ~> ' +
                                    self.items_dict[item]['To'].strip() + os.altsep + file
                                )
            if falg:
                self.statusbar.setStyleSheet("QStatusBar{color:green;}")
                self.statusbar.showMessage('Files moved prefectly. check logs..', msecs=5000)
                self.log.write_to_log("~END||\n")
            else:
                self.statusbar.setStyleSheet("QStatusBar{color:green;}")
                self.statusbar.showMessage('Everything is ok :)', msecs=5000)
        except:
            self.statusbar.setStyleSheet("QStatusBar{color:red;}")
            self.statusbar.showMessage('Somethings is wrong.. contact with us, PLZ.')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
