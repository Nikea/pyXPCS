#!/usr/bin/env python
from PyQt4 import Qt
from form1_temp import *
import sys
import time
if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = Form1()
    f.show()
    app.setMainWidget(f)
    f.change_labelsback()
    if len(sys.argv)==2:
       input= sys.argv[1]
       if os.path.exists(input):
          f.lineEdit_input.setText(input)
          f.loadinput()
          f.plot_unmasked()
    app.exec_loop()
