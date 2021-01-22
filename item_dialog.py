from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from extension_dialog import Extension
import os
import json
from utils.logger import Logger


class Item(object):
    def __init__(self, dialog):
        self.edit = False
        self.items = {}
        self.extension = {}
        self.log = Logger()
        dialog.setWindowIcon(QtGui.QIcon('imgs/icon.ico'))

        self.statusbar = QtWidgets.QStatusBar(dialog)
        self.le_name = QtWidgets.QLineEdit(dialog)
        self.lb_name = QtWidgets.QLabel(dialog)
        self.lb_from = QtWidgets.QLabel(dialog)
        self.lb_to = QtWidgets.QLabel(dialog)
        self.le_from = QtWidgets.QLineEdit(dialog)
        self.le_to = QtWidgets.QLineEdit(dialog)
        self.btn_from = QtWidgets.QPushButton(dialog)
        self.btn_to = QtWidgets.QPushButton(dialog)
        self.lb_ext = QtWidgets.QLabel(dialog)
        self.cb_item = QtWidgets.QComboBox(dialog)
        self.btn_item_cancel = QtWidgets.QPushButton(dialog)
        self.btn_item_ok = QtWidgets.QPushButton(dialog)
        self.lb_cgp = QtWidgets.QLabel(dialog)
        self.dialog_browser = QtWidgets.QFileDialog()

        dialog.setObjectName("Dialog")
        dialog.resize(513, 230)
        dialog.setFocusPolicy(QtCore.Qt.ClickFocus)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)

        self.setup_ui()

        self.ext_dialog = QtWidgets.QDialog()
        self.ext_ui = Extension(self.ext_dialog)
        self.ext_ui.setup_ui()
        self.ext_dialog.closeEvent = self.ext_ui.close
        self.ext_ui.btn_ok.clicked.connect(self.read_ext_db)

        self.btn_item_cancel.clicked.connect(dialog.close)
        self.btn_item_ok.clicked.connect(lambda: self.ok_item_dialog(dialog))
        self.btn_from.clicked.connect(self.brows_from)
        self.btn_to.clicked.connect(self.brows_to)
        self.btn_item_cancel.clicked.connect(self.cancel)

        self.retranslate_ui(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def setup_ui(self):
        self.statusbar.setObjectName("statusbar")
        self.le_name.setGeometry(QtCore.QRect(100, 40, 151, 25))
        self.le_name.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.le_name.setObjectName("te_name")
        self.lb_name.setGeometry(QtCore.QRect(20, 40, 71, 25))
        self.lb_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lb_name.setObjectName("lb_name")
        self.lb_from.setGeometry(QtCore.QRect(20, 100, 71, 25))
        self.lb_from.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lb_from.setObjectName("lb_from")
        self.lb_to.setGeometry(QtCore.QRect(20, 130, 71, 25))
        self.lb_to.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lb_to.setObjectName("lb_to")
        self.le_from.setGeometry(QtCore.QRect(100, 100, 341, 25))
        self.le_from.setReadOnly(True)
        self.le_from.setObjectName("te_from")
        self.le_to.setGeometry(QtCore.QRect(100, 130, 341, 25))
        self.le_to.setReadOnly(True)
        self.le_to.setObjectName("te_to")
        self.btn_from.setGeometry(QtCore.QRect(450, 100, 30, 25))
        self.btn_from.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_from.setObjectName("btn_from")
        self.btn_to.setGeometry(QtCore.QRect(450, 130, 31, 25))
        self.btn_to.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_to.setObjectName("btn_to")
        self.lb_ext.setGeometry(QtCore.QRect(20, 70, 71, 25))
        self.lb_ext.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lb_ext.setObjectName("lb_ext")
        self.cb_item.setGeometry(QtCore.QRect(100, 71, 100, 24))
        self.cb_item.setObjectName("cb_item")
        self.btn_item_cancel.setGeometry(QtCore.QRect(265, 180, 100, 31))
        self.btn_item_cancel.setAutoDefault(False)
        self.btn_item_cancel.setObjectName("btn_item_cancel")
        self.btn_item_ok.setGeometry(QtCore.QRect(380, 180, 100, 31))
        self.btn_item_ok.setDefault(True)
        self.btn_item_ok.setObjectName("btn_item_ok")
        self.lb_cgp.setGeometry(QtCore.QRect(210, 73, 200, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.lb_cgp.setFont(font)
        self.lb_cgp.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lb_cgp.setAutoFillBackground(False)
        self.lb_cgp.setStyleSheet("color:rgb(46, 133, 209)")
        self.lb_cgp.setObjectName("lb_cgp")

    def retranslate_ui(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Dialog", "Item"))
        self.le_name.setPlaceholderText(_translate("Dialog", "Pick a name.."))
        self.lb_name.setText(_translate("Dialog", "Item Name"))
        self.lb_from.setText(_translate("Dialog", "From"))
        self.lb_to.setText(_translate("Dialog", "To"))
        self.le_from.setPlaceholderText(_translate("Dialog", "Choose a path.."))
        self.le_to.setPlaceholderText(_translate("Dialog", "Choose a path.."))
        self.btn_from.setText(_translate("Dialog", "..."))
        self.btn_to.setText(_translate("Dialog", "..."))
        self.lb_ext.setText(_translate("Dialog", "Extension"))
        self.btn_item_cancel.setText(_translate("Dialog", "Cancel"))
        self.btn_item_ok.setText(_translate("Dialog", "Ok"))
        self.lb_cgp.setText(_translate("Dialog", "Manage Group Extension"))

    def ok_item_dialog(self, dialog):
        name = ''.join(filter(str.isalnum, self.le_name.text()))
        if (name in self.items.keys()) and (self.edit is False):
            self.le_name.setStyleSheet('border: 2px solid red;')
            return
        if not name:
            self.le_name.setStyleSheet('border: 2px solid red;')
            return
        else:
            self.le_name.setStyleSheet('')

        ext = ''.join(filter(str.isalnum, self.cb_item.currentText()))
        if not ext:
            self.cb_item.setStyleSheet('border: 2px solid red;')
            return
        else:
            self.cb_item.setStyleSheet('')

        from_dir = self.le_from.text().strip()
        if not from_dir:
            self.le_from.setStyleSheet('border: 2px solid red;')
            return
        else:
            self.le_from.setStyleSheet('')

        to_dir = self.le_to.text().strip()
        if not to_dir:
            self.le_to.setStyleSheet('border: 2px solid red;')
            return
        else:
            self.le_to.setStyleSheet('')

        self.items[name] = {
                'From': self.le_from.text(),
                'To': self.le_to.text(),
                'Extension': ext
            }
        self.write_item_db()
        self.clear_elemnts()
        if self.edit:
            self.edit = False
            self.le_name.setReadOnly(False)
        dialog.close()

    def cancel(self):
        self.le_name.setStyleSheet('')
        self.cb_item.setStyleSheet('')
        self.le_from.setStyleSheet('')
        self.le_to.setStyleSheet('')

    def brows_from(self):
        self.le_from.setText(
            self.dialog_browser.getExistingDirectory(directory=os.path.join(os.environ['USERPROFILE'], 'Desktop'),
                                                     caption='Select messy directory')
        )

    def brows_to(self):
        self.le_to.setText(
            self.dialog_browser.getExistingDirectory(directory=os.path.join(os.environ['USERPROFILE'], 'Desktop'),
                                                     caption='Select an awesome directory')
        )

    def open_gp_ext(self, event):
        self.ext_ui.clear_style()
        self.ext_ui.clear_item()
        self.ext_ui.read_ext_db()
        self.ext_dialog.show()

    def read_ext_db(self):
        self.cb_item.clear()
        self.cb_item.addItem('')
        try:
            if os.path.isfile('database/Extension.json'):
                with open('database/Extension.json') as db:
                    self.extension = json.load(db)
                    for i in self.extension:
                        self.cb_item.addItem(i)
                    return self.extension
            else:
                self.log.write_to_log('Extension database not found.')
        except:
            self.log.write_to_log(
                "May your 'Tezlabss.json' file damaged or corrupted.. Fix it if you know JSON, or delete PLZ :("
            )

    def write_item_db(self):
        with open('database/Items.json', 'w') as outfile:
            json.dump(self.items, outfile, sort_keys=True, indent=4)

    def read_item_db(self):
        try:
            if os.path.isfile('database/Items.json'):
                with open('database/Items.json') as db:
                    self.items = json.load(db)
                    return self.items
            else:
                self.log.write_to_log("Not found database file")
        except:
            self.log.write_to_log(
                "May your 'Tezlabss.json' file damaged or corrupted.. Fix it if you know JSON, or delete PLZ :(")

    def clear_elemnts(self):
        self.le_name.clear()
        self.le_from.clear()
        self.le_to.clear()

    def load_item(self, item_name):
        self.edit = True
        self.le_name.setReadOnly(True)
        self.le_name.setText(item_name)
        self.le_from.setText(self.items[item_name]['From'])
        self.le_to.setText(self.items[item_name]['To'])
        cb_index = self.cb_item.findText(self.items[item_name]['Extension'])
        self.cb_item.setCurrentIndex(cb_index)
