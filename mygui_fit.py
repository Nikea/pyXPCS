#!/usr/bin/env python
from qt import *
from form_fit import *
import sys
import time

if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = Form1()
    f.show()
    f.load_input()
    app.setMainWidget(f)
    app.exec_loop()

