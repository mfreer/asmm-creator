'''
Created on Mar 6, 2012

@author: freer
'''

from PyQt4 import QtCore, QtGui
from ui.mainwindow import MainWindow

def launch_asmm_creator():
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    launch_asmm_creator()
