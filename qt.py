import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.Qt import *
from PySide6.QtCore import Qt
from excel_process import excel_process, type_previw
from threading import Timer

class Custom_QGroupBox(QtWidgets.QGroupBox):
    checkAllIfAny = True
    
    def __init__(self, *args, **kwargs):
        super(Custom_QGroupBox, self).__init__(*args, **kwargs)
        self.setCheckable(True)
        self.checkBoxes = []
        self.choiceBoxes = []
        self.clicked_order = []
        self.toggled.connect(self.toggleCheckBoxes)

    def addCheckBox(self, cb):
        self.checkBoxes.append(cb)
        cb.toggled.connect(self.update)
        cb.stateChanged.connect(self.on_checkbox_change)
        cb.destroyed.connect(lambda: self.removeCheckBox(cb))

    def addChoiceBox(self, chib):
        self.choiceBoxes.append(chib)

    def removeCheckBox(self, cb):
        try:
            self.checkBoxes.remove(cb)
            cb.toggled.disconnect(self.update)
        except:
            pass

    def allStates(self):
        return [cb.isChecked() for cb in self.checkBoxes]

    def on_checkbox_change(self, state):
        if state == 2:  # Qt.Checked
            self.clicked_order.append(self.checkBoxes.index(self.sender()))
            print(self.clicked_order)
        else:
            self.clicked_order.remove(self.checkBoxes.index(self.sender()))
            print(self.clicked_order)

    def toggleCheckBoxes(self):
        if self.checkAllIfAny:
            state = not all(self.allStates())
        else:
            state = not any(self.allStates())

        for widget in self.children():
            if not widget.isWidgetType():
                continue
            if not widget.testAttribute(QtCore.Qt.WA_ForceDisabled):
                # восстановить включенное состояние, чтобы переопределить 
                # поведение setChecked(False) по умолчанию; 
                # предыдущие явные вызовы setEnabled(False) для целевого виджета 
                # будут игнорироваться
                widget.setEnabled(True)
                if widget in self.checkBoxes:
                    widget.setChecked(state)

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOptionGroupBox()
        self.initStyleOption(opt)
        states = self.allStates()
        if all(states):
            # force the "checked" state
            opt.state |= QtWidgets.QStyle.State_On
            opt.state &= ~QtWidgets.QStyle.State_Off
        else:
            # force the "not checked" state
            opt.state &= ~QtWidgets.QStyle.State_On
            if any(states):
                # force the "not unchecked" state and set the tristate mode
                opt.state &= ~QtWidgets.QStyle.State_Off
                opt.state |= QtWidgets.QStyle.State_NoChange
            else:
                # force the "unchecked" state
                opt.state |= QtWidgets.QStyle.State_Off
        painter = QtWidgets.QStylePainter(self)
        painter.drawComplexControl(QtWidgets.QStyle.CC_GroupBox, opt)


class MainWindow(QtWidgets.QWidget):
    def __init__(self, file_name):
        super().__init__()
        
        self.clear_file_name = str(file_name.split('.')[0])
        value = type_previw(self.clear_file_name, False)[0]
        self.groupBox = Custom_QGroupBox('Все категории')
        layout = QtWidgets.QGridLayout(self.groupBox)
        num = 0
        for c in range(1):
            for r in range(len(value)):
                num += 1
                cb = QtWidgets.QCheckBox(f' {value[r]}.')
                self.groupBox.addCheckBox(cb)
                layout.addWidget(cb, r, c)
                chib = QtWidgets.QComboBox()
                chib.addItems(["Стока", "Столбец"])
                self.groupBox.addChoiceBox(chib)
                layout.addWidget(chib, r, c+1)

        self.toolButton = QtWidgets.QToolButton()
        self.toolButton.setIcon(QtGui.QIcon('head3.png'))
        self.toolButton.setAutoRaise(True)
        self.toolButton.setIconSize(QtCore.QSize(70, 70))
        self.toolButton.setStyleSheet(
            'background-color: green; border-radius: 35px;')
            
        self.label_1 = QtWidgets.QLabel("Выберите используемые данные")
        self.label_1.setWordWrap(True)
        label_2 = QtWidgets.QLabel('Найденные категории:')
        
        self.buttonConfirm = QtWidgets.QPushButton('Создать')
        self.buttonConfirm.clicked.connect(self.confirm)
        self.buttonCancel = QtWidgets.QPushButton('Закрыть')
        self.buttonCancel.clicked.connect(self.cancel)

        layoutH = QtWidgets.QHBoxLayout()
        layoutH.addStretch(1)
        layoutH.addWidget(self.buttonConfirm)
        layoutH.addWidget(self.buttonCancel)

        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addWidget(self.toolButton, 1, 1)
        main_layout.addWidget(self.label_1, 1, 2)
        main_layout.addWidget(label_2, 2, 1, 1, 2)
        main_layout.addWidget(self.groupBox, 3, 1, 1, 2)
        main_layout.addLayout(layoutH, 4, 1, 1, 2)
        
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(5, 1)
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(3, 1)
    
    def confirm(self):
        self.buttonConfirm.setEnabled(False)
        self.label_1.setText("Выполняется процесс, ожидайте ...")
                                   
        QtCore.QCoreApplication.processEvents()

        checked = []
        for i in self.groupBox.clicked_order:
            checked.append([
                i,
                self.groupBox.choiceBoxes[i].currentIndex()
            ])
        print(checked)

        result = excel_process(self.clear_file_name, checked)
        
        self.buttonConfirm.setEnabled(True) 
        if (result):
            self.label_1.setText("Успешно!")
            self.toolButton.setStyleSheet(
                'background-color: green; border-radius: 35px;')
        else:
            self.label_1.setText("Выберите хотя бы одну пару имя - значение")
            self.toolButton.setStyleSheet(
                'background-color: red; border-radius: 35px;')
    
    @QtCore.Slot()
    def cancel(self):
        sys.exit()

if __name__ == "__main__":


    # command = './mdb-export-all.sh ' + sys.argv[1]
    # os.system(command)
    
    app = QtWidgets.QApplication([])
    
    widget = MainWindow("DKR")