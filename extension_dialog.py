from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import json
import os
from utils.logger import Logger


class Extension(object):
    def __init__(self, Dialog):
        self.ext_dict = {}
        Dialog.setWindowIcon(QtGui.QIcon('imgs/icon.ico'))
        self.reply = None
        self.changes = False
        self.log = Logger()

        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.setObjectName("Dialog")
        Dialog.resize(424, 376)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.le_gp = QtWidgets.QLineEdit(self.groupBox)
        self.lw_gp = QtWidgets.QListWidget(self.groupBox)
        self.btn_del_gp = QtWidgets.QPushButton(self.groupBox)
        self.btn_add_gp = QtWidgets.QPushButton(self.groupBox)
        self.btn_add_ext = QtWidgets.QPushButton(Dialog)
        self.le_ext = QtWidgets.QLineEdit(Dialog)
        self.lw_ext = QtWidgets.QListWidget(Dialog)
        self.btn_del_ext = QtWidgets.QPushButton(Dialog)
        self.btn_ok = QtWidgets.QPushButton(Dialog)
        self.btn_cancel = QtWidgets.QPushButton(Dialog)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.btn_ok.clicked.connect(self.ok)
        self.btn_ok.clicked.connect(Dialog.close)
        self.btn_cancel.clicked.connect(lambda: self.cancel(Dialog))
        self.btn_cancel.clicked.connect(Dialog.close)
        self.btn_add_gp.clicked.connect(self.add_group)
        self.le_gp.returnPressed.connect(self.add_group)
        self.btn_del_gp.clicked.connect(lambda: self.del_group(Dialog))
        self.btn_add_ext.clicked.connect(self.add_ext)
        self.le_ext.returnPressed.connect(self.add_ext)
        self.btn_del_ext.clicked.connect(self.del_ext)
        self.lw_gp.itemClicked.connect(self.lw_gp_selected)

    def setup_ui(self):
        self.groupBox.setGeometry(QtCore.QRect(30, 30, 221, 261))
        self.groupBox.setObjectName("groupBox")
        self.le_gp.setGeometry(QtCore.QRect(10, 20, 131, 25))
        self.le_gp.setObjectName("le_gp")
        self.lw_gp.setGeometry(QtCore.QRect(10, 60, 201, 191))
        self.lw_gp.setObjectName("lw_gp")
        self.btn_del_gp.setGeometry(QtCore.QRect(180, 20, 25, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btn_del_gp.setFont(font)
        self.btn_del_gp.setStyleSheet("color: red")
        self.btn_del_gp.setObjectName("btn_del_gp")

        self.btn_add_gp.setGeometry(QtCore.QRect(150, 20, 25, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_add_gp.setFont(font)
        self.btn_add_gp.setStyleSheet("color: rgb(85, 170, 0)")
        self.btn_add_gp.setObjectName("btn_add_gp")
        self.btn_add_gp.setFocus()
        self.btn_add_ext.setGeometry(QtCore.QRect(330, 50, 25, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_add_ext.setFont(font)
        self.btn_add_ext.setStyleSheet("color: rgb(85, 170, 0)")
        self.btn_add_ext.setObjectName("btn_add_ext")
        self.le_ext.setGeometry(QtCore.QRect(260, 50, 61, 25))
        self.le_ext.setObjectName("le_ext")
        self.lw_ext.setGeometry(QtCore.QRect(260, 90, 131, 191))
        self.lw_ext.setObjectName("lw_ext")
        self.btn_del_ext.setGeometry(QtCore.QRect(360, 50, 25, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btn_del_ext.setFont(font)
        self.btn_del_ext.setStyleSheet("color: red")
        self.btn_del_ext.setObjectName("btn_del_ext")
        self.btn_ok.setGeometry(QtCore.QRect(290, 320, 100, 31))
        self.btn_ok.setObjectName("btn_ok")
        self.btn_cancel.setGeometry(QtCore.QRect(175, 320, 100, 31))
        self.btn_cancel.setObjectName("btn_cancel")

        self.btn_add_gp.setAutoDefault(False)
        self.btn_del_gp.setAutoDefault(False)
        self.btn_add_ext.setAutoDefault(False)
        self.btn_del_ext.setAutoDefault(False)
        self.btn_cancel.setAutoDefault(False)
        self.btn_ok.setAutoDefault(False)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Custom Extension Group"))
        self.groupBox.setTitle(_translate("Dialog", "Group Name"))
        self.btn_del_gp.setText(_translate("Dialog", "x"))
        self.btn_add_gp.setText(_translate("Dialog", "+"))
        self.btn_add_ext.setText(_translate("Dialog", "+"))
        self.btn_del_ext.setText(_translate("Dialog", "x"))
        self.btn_ok.setText(_translate("Dialog", "Ok"))
        self.btn_cancel.setText(_translate("Dialog", "Cancel"))

    def basteshod(self):
        print('Heyyyyyyyyyy')

    def add_group(self):
        self.lw_gp.setStyleSheet('')
        if not self.le_gp.text():
            self.le_gp.setStyleSheet('border: 2px solid red;')
        else:
            self.changes = True
            self.le_gp.setStyleSheet('')
            ext_name = ''.join(filter(str.isalnum, self.le_gp.text()))
            self.lw_gp.addItem(ext_name)
            self.ext_dict[ext_name] = []
        self.le_gp.clear()

    def del_group(self, dialog):
        self.le_gp.setStyleSheet('')
        current = self.lw_gp.currentRow()
        if current != -1:
            current_text = self.lw_gp.currentItem().text()
            self.reply = QMessageBox.question(dialog, 'Remove Group Extension?',
                                              "Are you sure remove '{}' extension group?".format(current_text),
                                         QMessageBox.Yes, QMessageBox.No)
            self.lw_gp.setStyleSheet('')
        else:
            self.lw_gp.setStyleSheet('border: 2px solid red;')
            return

        if self.reply == QMessageBox.No:
            return
        else:
            self.changes = True
            self.lw_gp.takeItem(current)
            del self.ext_dict[current_text]
            self.lw_ext.clear()

    def add_ext(self):
        self.lw_ext.setStyleSheet('')
        if not self.le_ext.text():
            self.le_ext.setStyleSheet('border: 2px solid red;')
            return
        else:
            for en in self.ext_dict:
                for ext in self.ext_dict[en]:
                    if self.le_ext.text() == ext:
                        it = self.lw_gp.findItems(en, QtCore.Qt.MatchExactly)
                        if it:
                            self.lw_gp.setCurrentItem(it[0])
                            self.lw_gp_selected(it[0])
                            self.lw_ext.setStyleSheet('border: 2px solid red;')
                        return
            self.le_ext.setStyleSheet('')
            ext_name = ''.join(filter(str.isalnum, self.le_ext.text()))
            self.changes = True

        if self.lw_gp.currentRow() == -1:
            self.lw_gp.setStyleSheet('border: 2px solid red;')
            return
        else:
            self.lw_gp.setStyleSheet('')

        self.lw_ext.addItem(ext_name)

        self.ext_dict[self.lw_gp.currentItem().text()].append(ext_name)
        self.le_ext.clear()

    def del_ext(self):
        self.clear_style()
        current = self.lw_ext.currentRow()
        if current == -1:
            self.lw_ext.setStyleSheet('border: 2px solid red;')
            return
        else:
            self.changes = True
            self.lw_ext.setStyleSheet('')
        self.ext_dict[self.lw_gp.currentItem().text()].remove(self.lw_ext.currentItem().text())
        self.lw_ext.takeItem(current)

    def ok(self):
        self.clear_style()
        self.clear_item()
        self.write_ext_db()

    def cancel(self, dialog):
        self.clear_style()
        self.clear_item()

        if self.changes:
            self.reply = QMessageBox.question(dialog, 'Exit',
                                              "Do you want to save changes?",
                                              QMessageBox.Yes, QMessageBox.No)
            if self.reply == QMessageBox.Yes:
                self.write_ext_db()
        self.changes = False
        dialog.close()

    def clear_style(self):
        self.lw_gp.setStyleSheet('')
        self.le_gp.setStyleSheet('')
        self.lw_ext.setStyleSheet('')
        self.le_ext.setStyleSheet('')

    def clear_item(self):
        self.lw_gp.clear()
        self.le_gp.clear()
        self.lw_ext.clear()
        self.le_ext.clear()

    def lw_gp_selected(self, item):
        self.clear_style()
        self.lw_ext.clear()
        if item.text():
            for i in self.ext_dict[item.text()]:
                self.lw_ext.addItem(i)

    def write_ext_db(self):
        with open('database/Extension.json', 'w') as outfile:
            json.dump(self.ext_dict, outfile, sort_keys=True, indent=4)

    def read_ext_db(self):
        try:
            if os.path.isfile('database/Extension.json'):
                with open('database/Extension.json') as db:
                    self.ext_dict = json.load(db)
                    for i in self.ext_dict:
                        self.lw_gp.addItem(i)
                    return self.ext_dict
            else:
                self.log.write_to_log("Not found extension database file..")
        except:
            self.log.write_to_log(
                "May your 'Extension.json' file damaged or corrupted.. Fix it if you know JSON, or delete PLZ :(")

    def reload_ext_ui(self, event):
        self.clear_style()
        self.read_ext_db()

    def close(self, e):
        self.clear_style()
        self.clear_item()