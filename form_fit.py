# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form_fit.ui'
#
# Created: Wed Dec 10 17:30:02 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *


class Form1(QMainWindow):
    def __init__(self,parent = None,name = None,fl = 0):
        QMainWindow.__init__(self,parent,name,fl)
        self.statusBar()

        if not name:
            self.setName("Form1")


        self.setCentralWidget(QWidget(self,"qt_central_widget"))
        Form1Layout = QGridLayout(self.centralWidget(),1,1,11,6,"Form1Layout")

        self.splitter2 = QSplitter(self.centralWidget(),"splitter2")
        self.splitter2.setOrientation(QSplitter.Horizontal)

        self.textLabel_input = QLabel(self.splitter2,"textLabel_input")

        self.lineEdit_input = QLineEdit(self.splitter2,"lineEdit_input")
        self.lineEdit_input.setMaximumSize(QSize(32767,20))

        Form1Layout.addWidget(self.splitter2,0,0)

        self.textEdit_input = QTextEdit(self.centralWidget(),"textEdit_input")
        self.textEdit_input.setWordWrap(QTextEdit.WidgetWidth)

        Form1Layout.addMultiCellWidget(self.textEdit_input,1,1,0,1)

        self.splitter8 = QSplitter(self.centralWidget(),"splitter8")
        self.splitter8.setOrientation(QSplitter.Horizontal)

        LayoutWidget = QWidget(self.splitter8,"layout5")
        layout5 = QHBoxLayout(LayoutWidget,11,6,"layout5")

        self.splitter6 = QSplitter(LayoutWidget,"splitter6")
        self.splitter6.setOrientation(QSplitter.Horizontal)

        self.textLabel_filepars = QLabel(self.splitter6,"textLabel_filepars")
        self.textLabel_filepars.setMaximumSize(QSize(50,32767))

        self.lineEdit_filepars = QLineEdit(self.splitter6,"lineEdit_filepars")
        self.lineEdit_filepars.setEnabled(0)
        self.lineEdit_filepars.setMaximumSize(QSize(32767,20))
        self.lineEdit_filepars.setPaletteForegroundColor(QColor(240,22,25))
        layout5.addWidget(self.splitter6)

        self.splitter5 = QSplitter(LayoutWidget,"splitter5")
        self.splitter5.setOrientation(QSplitter.Horizontal)

        self.textLabel_filefit = QLabel(self.splitter5,"textLabel_filefit")
        self.textLabel_filefit.setMaximumSize(QSize(50,32767))

        self.lineEdit_filefit = QLineEdit(self.splitter5,"lineEdit_filefit")
        self.lineEdit_filefit.setEnabled(0)
        self.lineEdit_filefit.setMaximumSize(QSize(32767,20))
        layout5.addWidget(self.splitter5)

        self.pushButton_start = QPushButton(self.splitter8,"pushButton_start")
        self.pushButton_start.setMaximumSize(QSize(50,32767))
        self.pushButton_start.setPaletteBackgroundColor(QColor(110,220,0))
        pushButton_start_font = QFont(self.pushButton_start.font())
        pushButton_start_font.setPointSize(12)
        pushButton_start_font.setBold(1)
        self.pushButton_start.setFont(pushButton_start_font)
        self.pushButton_start.setFlat(0)

        Form1Layout.addMultiCellWidget(self.splitter8,4,4,0,1)

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.pushButton_load = QPushButton(self.centralWidget(),"pushButton_load")
        pushButton_load_font = QFont(self.pushButton_load.font())
        pushButton_load_font.setPointSize(12)
        pushButton_load_font.setBold(1)
        self.pushButton_load.setFont(pushButton_load_font)
        layout3.addWidget(self.pushButton_load)

        self.pushButton_save = QPushButton(self.centralWidget(),"pushButton_save")
        pushButton_save_font = QFont(self.pushButton_save.font())
        pushButton_save_font.setPointSize(12)
        pushButton_save_font.setBold(1)
        self.pushButton_save.setFont(pushButton_save_font)
        layout3.addWidget(self.pushButton_save)

        Form1Layout.addLayout(layout3,0,1)

        self.splitter9 = QSplitter(self.centralWidget(),"splitter9")
        self.splitter9.setOrientation(QSplitter.Horizontal)

        self.splitter3 = QSplitter(self.splitter9,"splitter3")
        self.splitter3.setOrientation(QSplitter.Horizontal)

        self.textLabel_col = QLabel(self.splitter3,"textLabel_col")

        self.lineEdit_col = QLineEdit(self.splitter3,"lineEdit_col")

        self.checkBox_plot = QCheckBox(self.splitter9,"checkBox_plot")
        self.checkBox_plot.setChecked(1)

        Form1Layout.addMultiCellWidget(self.splitter9,2,2,0,1)

        self.splitter10 = QSplitter(self.centralWidget(),"splitter10")
        self.splitter10.setOrientation(QSplitter.Horizontal)

        self.splitter1 = QSplitter(self.splitter10,"splitter1")
        self.splitter1.setOrientation(QSplitter.Horizontal)

        self.textLabel_outdir = QLabel(self.splitter1,"textLabel_outdir")
        self.textLabel_outdir.setMaximumSize(QSize(100,32767))

        self.lineEdit_outdir = QLineEdit(self.splitter1,"lineEdit_outdir")

        self.splitter4 = QSplitter(self.splitter10,"splitter4")
        self.splitter4.setOrientation(QSplitter.Horizontal)

        self.textLabel_outpref = QLabel(self.splitter4,"textLabel_outpref")

        self.lineEdit_outpref = QLineEdit(self.splitter4,"lineEdit_outpref")

        Form1Layout.addMultiCellWidget(self.splitter10,3,3,0,1)



        self.languageChange()

        self.resize(QSize(712,307).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton_load,SIGNAL("pressed()"),self.load_input)
        self.connect(self.pushButton_save,SIGNAL("pressed()"),self.save_input)
        self.connect(self.pushButton_start,SIGNAL("pressed()"),self.fit)


    def languageChange(self):
        self.setCaption(self.__tr("PYFIT version 1.0"))
        self.textLabel_input.setText(self.__tr("Input file:"))
        self.lineEdit_input.setText(self.__tr("input_fit.txt"))
        self.textEdit_input.setText(self.__tr("file=./InputFiles/ferrofluids/220KB-horiz_cf.dat\n"
"xcol=1\n"
"ycol=2\n"
"normcol=none\n"
"yerr=none\n"
"range=in   #(in/out/all)\n"
"T1=1e-3\n"
"T2=1e2\n"
"f(x)=p0*exp(-2*(p1*x)**p2)+c0\n"
"p2=beta, 1\n"
"p0=contrast, .08\n"
"p1=gamma, 1\n"
"c0=baseline, 1\n"
""))
        self.textLabel_filepars.setText(self.__tr("file pars:"))
        self.textLabel_filefit.setText(self.__tr("files fit:"))
        self.pushButton_start.setText(self.__tr("S&tart"))
        self.pushButton_start.setAccel(QKeySequence(self.__tr("Alt+T")))
        self.pushButton_load.setText(self.__tr("&LOAD"))
        self.pushButton_load.setAccel(QKeySequence(self.__tr("Alt+L")))
        self.pushButton_save.setText(self.__tr("&SAVE"))
        self.pushButton_save.setAccel(QKeySequence(self.__tr("Alt+S")))
        self.textLabel_col.setText(self.__tr("Last Column"))
        self.lineEdit_col.setText(self.__tr("5"))
        self.checkBox_plot.setText(self.__tr("Plot"))
        self.textLabel_outdir.setText(self.__tr("output directory:"))
        self.lineEdit_outdir.setText(self.__tr("auto"))
        self.textLabel_outpref.setText(self.__tr("output prefix:"))
        self.lineEdit_outpref.setText(self.__tr("auto"))


    def load_input(self):
        print "Form1.load_input(): Not implemented yet"

    def save_input(self):
        print "Form1.save_input(): Not implemented yet"

    def fit(self):
        print "Form1.fit(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("Form1",s,c)
