from PyQt6 import QtWidgets, uic
import sys
import visa
 
app = QtWidgets.QApplication([])
win = uic.loadUi("swmeas_main.ui")
 
win.show()
sys.exit(app.exec())