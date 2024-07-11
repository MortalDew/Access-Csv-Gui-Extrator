import sys, os
from PySide6 import QtWidgets
from qt import MainWindow

def file_path_confirm(full_path):
    if (len(sys.argv) == 2):
        if (full_path.find('/') > 0):
            return os.path.splitext(os.path.basename(full_path))[0]
        else:
            return full_path
    else:
        print("Введите путь к файлу")
        sys.exit()

if __name__ == "__main__":

    file = file_path_confirm(sys.argv[1])

    # command = './mdb-export-all.sh ' + sys.argv[1]
    # os.system(command)
    
    app = QtWidgets.QApplication([])
    
    widget = MainWindow(file)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
