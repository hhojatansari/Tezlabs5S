from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from item_dialog import Item
from utils.logger import Logger
import os
import json
import shutil


clean_text = """
      _                           _ 
  ___| | ___  __ _ _ __   ___  __| |
 / __| |/ _ \/ _` | '_ \ / _ \/ _` |
| (__| |  __/ (_| | | | |  __/ (_| |
 \___|_|\___|\__,_|_| |_|\___|\__,_|


    """


class MainWindow(object):
    def __init__(self, window):
        self.log = Logger()
        self.items_dict = {}
        window.setObjectName("MainWindow")
        window.setFixedSize(565, 631)
        self.statusbar = QtWidgets.QStatusBar(window)
        window.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(window)
        self.centralwidget = QtWidgets.QWidget(window)
        window.setCentralWidget(self.centralwidget)
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.btn_exit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_about = QtWidgets.QPushButton(self.centralwidget)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.lw_items = QtWidgets.QListWidget(self.groupBox)
        self.btn_remove = QtWidgets.QPushButton(self.groupBox)
        self.btn_edit = QtWidgets.QPushButton(self.groupBox)
        self.btn_new = QtWidgets.QPushButton(self.groupBox)
        self.btn_clean = QtWidgets.QPushButton(self.groupBox)
        self.lb_f = QtWidgets.QLabel(self.groupBox)
        self.lb_t = QtWidgets.QLabel(self.groupBox)
        self.lb_e = QtWidgets.QLabel(self.groupBox)
        self.lb_from = QtWidgets.QLabel(self.groupBox)
        self.lb_to = QtWidgets.QLabel(self.groupBox)
        self.lb_ext = QtWidgets.QLabel(self.groupBox)
        self.msg = QtWidgets.QMessageBox()

        self.retranslate_ui(window)

        self.item_dialog = QtWidgets.QDialog()
        self.item_ui = Item(self.item_dialog)
        self.item_ui.setup_ui()
        self.item_ui.btn_item_ok.clicked.connect(self.load_items)

        self.btn_about.clicked.connect(self.about_dialog)
        self.btn_exit.clicked.connect(window.close)
        self.btn_new.clicked.connect(self.open_new_item)
        self.btn_edit.clicked.connect(self.open_edit_item)
        self.btn_remove.clicked.connect(self.remove_item)
        self.lw_items.itemClicked.connect(self.lw_selected)
        self.btn_clean.clicked.connect(self.clean)
        self.item_ui.lb_cgp.mousePressEvent = self.item_ui.open_gp_ext

    def setup_ui(self):
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists('Log'):
            os.makedirs('Log')

        self.load_items()

        main_window.setObjectName("Tezlabs 5S 1.1.0")
        main_window.setWindowIcon(QtGui.QIcon('imgs/icon.ico'))

        self.centralwidget.setObjectName("centralwidget")
        self.logo.setGeometry(QtCore.QRect(25, 30, 516, 186))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("imgs/logo.png"))
        self.logo.setScaledContents(False)
        self.logo.setOpenExternalLinks(False)
        self.logo.setObjectName("logo")
        self.btn_exit.setGeometry(QtCore.QRect(410, 540, 111, 41))
        self.btn_exit.setObjectName("btn_exit")
        self.btn_about.setGeometry(QtCore.QRect(40, 540, 111, 41))
        self.btn_about.setObjectName("btn_about")
        self.groupBox.setGeometry(QtCore.QRect(40, 220, 481, 310))
        self.groupBox.setObjectName("groupBox")
        self.lw_items.setGeometry(QtCore.QRect(20, 30, 281, 151))
        self.lw_items.setObjectName("lw_items")
        self.btn_remove.setGeometry(QtCore.QRect(340, 130, 101, 28))
        self.btn_remove.setObjectName("btn_remove")
        self.btn_edit.setGeometry(QtCore.QRect(340, 95, 101, 28))
        self.btn_edit.setObjectName("btn_edit")
        self.btn_new.setGeometry(QtCore.QRect(340, 60, 101, 28))
        self.btn_new.setObjectName("btn_new")
        self.btn_clean.setGeometry(QtCore.QRect(20, 240, 441, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_clean.setFont(font)
        self.btn_clean.setObjectName("btn_clean")
        self.lb_f.setGeometry(QtCore.QRect(20, 200, 40, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lb_f.setFont(font)
        self.lb_f.setObjectName("lb_f")
        self.lb_e.setGeometry(QtCore.QRect(20, 185, 70, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lb_e.setFont(font)
        self.lb_e.setObjectName("lb_e")

        self.lb_t.setGeometry(QtCore.QRect(20, 215, 31, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lb_t.setFont(font)
        self.lb_t.setObjectName("lb_t")
        self.lb_from.setGeometry(QtCore.QRect(100, 200, 251, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lb_from.setFont(font)
        self.lb_from.setText("")
        self.lb_from.setObjectName("lb_from")

        self.lb_ext.setGeometry(QtCore.QRect(100, 185, 251, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lb_ext.setFont(font)
        self.lb_ext.setText("")
        self.lb_ext.setObjectName("lb_from")

        self.lb_to.setGeometry(QtCore.QRect(100, 215, 251, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lb_to.setFont(font)
        self.lb_to.setText("")
        self.lb_to.setObjectName("lb_to")
        self.statusbar.setObjectName("statusbar")

    def retranslate_ui(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("MainWindow", "Tezlabs 5S 1.1.1"))
        self.btn_exit.setText(_translate("MainWindow", "Exit"))
        self.btn_about.setText(_translate("MainWindow", "About"))
        self.groupBox.setTitle(_translate("MainWindow", "Item Management"))
        self.btn_remove.setText(_translate("MainWindow", "Remove Item"))
        self.btn_edit.setText(_translate("MainWindow", "Edit Item"))
        self.btn_new.setText(_translate("MainWindow", "New Item"))
        self.btn_clean.setText(_translate("MainWindow", "Clean"))
        self.lb_f.setText(_translate("MainWindow", "From:"))
        self.lb_t.setText(_translate("MainWindow", "To:"))
        self.lb_e.setText(_translate("MainWindow", "Extension:"))

    def open_new_item(self):
        self.lw_items.setStyleSheet('')
        self.clear_item_info()
        self.item_dialog.setWindowTitle('Add new Item')
        self.item_ui.read_ext_db()
        self.item_ui.read_item_db()
        self.item_dialog.show()

    def open_edit_item(self):
        self.lw_items.setStyleSheet('')
        if self.lw_items.currentRow() == -1:
            self.lw_items.setStyleSheet('border: 2px solid red;')
            return
        else:
            self.lw_items.setStyleSheet('')
        self.clear_item_info()
        self.item_dialog.setWindowTitle('Edit Item')
        self.item_ui.read_item_db()
        self.item_ui.read_ext_db()
        self.item_ui.load_item(self.lw_items.currentItem().text())
        self.item_dialog.show()

    def write_db(self):
        with open('database/Items.json', 'w') as outfile:
            json.dump(self.items_dict, outfile, sort_keys=True, indent=4)

    def load_items(self):
        self.lw_items.clear()
        try:
            if os.path.isfile('database/Items.json'):
                with open('database/Items.json') as db:
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
                "May your 'Tezlabs.json' file damaged or corrupted.. Fix it if you know JSON, or delete PLZ :(")

    def remove_item(self):
        if self.lw_items.currentRow() == -1:
            self.lw_items.setStyleSheet('border: 2px solid red;')
            return
        else:
            self.lw_items.setStyleSheet('')

        self.clear_item_info()
        current = self.lw_items.currentRow()
        current_text = self.lw_items.currentItem().text()
        reply = QMessageBox.question(main_window, 'Remove Item',
                                     "Are you sure remove '{}' item?".format(current_text),
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if current is not -1:
                del self.items_dict[self.lw_items.currentItem().text()]
                self.lw_items.takeItem(current)
                self.write_db()

    def lw_selected(self, item):
        ext = self.item_ui.ext_ui.read_ext_db()[self.items_dict[item.text()]['Extension']]
        self.lb_ext.setText('[' + self.items_dict[item.text()]['Extension'] + '] ' + " ".join(['.'+str(elem) for elem in ext]))
        self.lb_from.setText(self.items_dict[item.text()]['From'])
        self.lb_to.setText(self.items_dict[item.text()]['To'])

    def clear_item_info(self):
        self.lb_ext.clear()
        self.lb_from.clear()
        self.lb_to.clear()

    def clean(self):
        flag = False
        yes_to_all = False
        no_to_all = False

        items = self.item_ui.read_item_db()
        ext = self.item_ui.read_ext_db()
        if items:
            for item in items:
                try:
                    for file in os.listdir(items[item]['From']):
                        for e in ext[items[item]['Extension']]:
                            if (file.endswith('.{}'.format(e.upper()))) or (file.endswith('.{}'.format(e.lower()))):
                                try:
                                    from_base = (items[item]['From'] + os.altsep).strip()
                                    to_base = (items[item]['To'].strip() + os.altsep).strip()

                                    if os.path.isfile(to_base + file):
                                        if yes_to_all:
                                            shutil.move(from_base + file, to_base + file)
                                            self.log.write_to_log(
                                                self.items_dict[item]['From'] + os.altsep + file + ' ~> ' +
                                                self.items_dict[item]['To'].strip() + os.altsep + file
                                            )
                                            continue
                                        if no_to_all:
                                            break

                                        reply = QMessageBox.question(
                                            main_window, 'Replace or Skip Files',
                                            "The destination already has a file named {}.\n".format(file) +
                                            "Are you sure you want to replace it?",
                                            QMessageBox.Yes| QMessageBox.No| QMessageBox.YesToAll | QMessageBox.NoToAll
                                        )

                                        if reply == QMessageBox.Yes:
                                            flag = True
                                            shutil.move(
                                                from_base + file,
                                                to_base + file
                                            )
                                            self.log.write_to_log(
                                                self.items_dict[item]['From'] + os.altsep + file + ' ~> ' +
                                                self.items_dict[item]['To'].strip() + os.altsep + file
                                            )
                                        elif reply == QMessageBox.No:
                                            break
                                        elif reply == QMessageBox.YesToAll:
                                            flag = True
                                            shutil.move(
                                                from_base + file,
                                                to_base + file
                                            )
                                            self.log.write_to_log(
                                                self.items_dict[item]['From'] + os.altsep + file + ' ~> ' +
                                                self.items_dict[item]['To'].strip() + os.altsep + file
                                            )
                                            yes_to_all = True
                                        elif reply == QMessageBox.NoToAll:
                                            no_to_all = True
                                    else:
                                        flag =True
                                        shutil.move(
                                            from_base + file,
                                            to_base + file
                                        )
                                        self.log.write_to_log(
                                            self.items_dict[item]['From'] + os.altsep + file + ' ~> ' +
                                            self.items_dict[item]['To'].strip() + os.altsep + file
                                        )
                                except Exception as inst:
                                    print("Move Files Exception:\n{}\n{}\n{}".format(type(inst), inst.args, inst))
                                    self.log.write_to_log(
                                        "Move Files Exception:\n{}\n{}\n{}".format(type(inst), inst.args, inst)
                                    )
                except Exception as inst:

                    self.log.write_to_log(
                        "Move Files Exception:\n{}\n{}\n{}".format(type(inst), inst.args, inst)
                    )
                    self.statusbar.setStyleSheet("QStatusBar{color:red;}")
                    self.statusbar.showMessage("Something wrong with '{}' item, Check log.".format(item), msecs=5000)
            print(flag)
            if flag:
                self.statusbar.setStyleSheet("QStatusBar{color:green;}")
                self.statusbar.showMessage('Files moved prefectly. check logs..', msecs=5000)
                self.log.write_to_log(clean_text)
            else:
                self.statusbar.setStyleSheet("QStatusBar{color:green;}")
                self.statusbar.showMessage('Everything is ok :)', msecs=5000)
        else:
            self.statusbar.setStyleSheet("")
            self.statusbar.showMessage('There are no items.', msecs=5000)

    def about_dialog(self):
        self.msg.setWindowTitle('About')
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        text = """<p>This program is written by <strong>Hosein Hojat Ansari</strong>, from Tabiat Zendeh Laboratories, IT
         department.</p> <p>You can get source code  from
         <a href="https://github.com/hhojatansari/Tezlabs5S">here</a>.</p>"""
        self.msg.setText(text)
        self.msg.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_ui = MainWindow(main_window)
    main_ui.setup_ui()
    main_window.show()
    sys.exit(app.exec_())
