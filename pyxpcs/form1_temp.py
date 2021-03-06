# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form1_temp.ui'
#
# Created: Thu Nov 12 15:45:33 2009
#      by: The PyQt User Interface Compiler (pyuic) 3.17.6
#
# WARNING! All changes made in this file will be lost!


from PyQt4 import Qt
from mplwidget import *
from numpy import *
from read_input import get_input
from commands import getoutput
#from qt import QFileDialog    
from makemask import make_mask
from get_edf import file_name 
from some_modules_new import sum_data, auto_mask, do_average, loadedf, saveedf, headeredf, headersedf
import os, ytrc, EdfFile, os.path, threading, thread 
from q_pattern import qpattern
import pylab as p
from time import sleep
from chi4_chiara import chi4
from numpy.ma import masked_array
from matplotlib.nxutils import points_inside_poly


class Form1(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Form1")

        self.setEnabled(1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding,20,20,self.sizePolicy().hasHeightForWidth()))
        self.setBackgroundOrigin(QDialog.WidgetOrigin)
        self.setAcceptDrops(1)
        self.setSizeGripEnabled(1)
        self.setModal(1)

        Form1Layout = QGridLayout(self,1,1,11,21,"Form1Layout")

        self.tabWidget1 = QTabWidget(self,"tabWidget1")
        self.tabWidget1.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,254,254,self.tabWidget1.sizePolicy().hasHeightForWidth()))
        self.tabWidget1.setMaximumSize(QSize(32767,32767))

        self.tab = QWidget(self.tabWidget1,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,21,"tabLayout")

        layout62 = QVBoxLayout(None,0,21,"layout62")

        layout61 = QVBoxLayout(None,0,21,"layout61")

        self.frame9 = QFrame(self.tab,"frame9")
        self.frame9.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.frame9.sizePolicy().hasHeightForWidth()))
        self.frame9.setMaximumSize(QSize(32767,60))
        self.frame9.setFrameShape(QFrame.Box)
        self.frame9.setFrameShadow(QFrame.Raised)
        frame9Layout = QHBoxLayout(self.frame9,11,21,"frame9Layout")

        self.splitter2 = QSplitter(self.frame9,"splitter2")
        self.splitter2.setOrientation(QSplitter.Horizontal)

        self.textLabel1 = QLabel(self.splitter2,"textLabel1")
        self.textLabel1.setPaletteForegroundColor(QColor(255,0,0))
        textLabel1_font = QFont(self.textLabel1.font())
        textLabel1_font.setPointSize(12)
        textLabel1_font.setBold(1)
        self.textLabel1.setFont(textLabel1_font)
        self.textLabel1.setAcceptDrops(1)
        self.textLabel1.setFrameShape(QLabel.NoFrame)
        self.textLabel1.setTextFormat(QLabel.PlainText)
        self.textLabel1.setScaledContents(1)
        self.textLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        self.lineEdit_input = QLineEdit(self.splitter2,"lineEdit_input")
        self.lineEdit_input.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit_input.sizePolicy().hasHeightForWidth()))
        self.lineEdit_input.setMinimumSize(QSize(500,0))
        self.lineEdit_input.setMaximumSize(QSize(32767,23))
        frame9Layout.addWidget(self.splitter2)

        self.pushButton1 = QPushButton(self.frame9,"pushButton1")
        self.pushButton1.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Expanding,0,0,self.pushButton1.sizePolicy().hasHeightForWidth()))
        self.pushButton1.setMinimumSize(QSize(50,30))
        pushButton1_font = QFont(self.pushButton1.font())
        pushButton1_font.setPointSize(11)
        self.pushButton1.setFont(pushButton1_font)
        frame9Layout.addWidget(self.pushButton1)

        self.pushButton2 = QPushButton(self.frame9,"pushButton2")
        self.pushButton2.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.pushButton2.sizePolicy().hasHeightForWidth()))
        self.pushButton2.setMinimumSize(QSize(50,0))
        pushButton2_font = QFont(self.pushButton2.font())
        pushButton2_font.setPointSize(11)
        self.pushButton2.setFont(pushButton2_font)
        self.pushButton2.setAutoDefault(0)
        frame9Layout.addWidget(self.pushButton2)

        self.pushButton10 = QPushButton(self.frame9,"pushButton10")
        self.pushButton10.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding,0,0,self.pushButton10.sizePolicy().hasHeightForWidth()))
        self.pushButton10.setMinimumSize(QSize(80,40))
        self.pushButton10.setPaletteBackgroundColor(QColor(107,214,0))
        frame9Layout.addWidget(self.pushButton10)

        self.checkBox_plot = QCheckBox(self.frame9,"checkBox_plot")
        self.checkBox_plot.setAutoRepeat(0)
        self.checkBox_plot.setChecked(1)
        frame9Layout.addWidget(self.checkBox_plot)

        self.checkBox_multiproc = QCheckBox(self.frame9,"checkBox_multiproc")
        frame9Layout.addWidget(self.checkBox_multiproc)
        layout61.addWidget(self.frame9)

        self.frame8 = QFrame(self.tab,"frame8")
        self.frame8.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.frame8.sizePolicy().hasHeightForWidth()))
        self.frame8.setMaximumSize(QSize(32767,120))
        self.frame8.setFrameShape(QFrame.Box)
        self.frame8.setFrameShadow(QFrame.Raised)
        frame8Layout = QGridLayout(self.frame8,1,1,11,21,"frame8Layout")

        layout110 = QHBoxLayout(None,0,21,"layout110")

        layout19 = QHBoxLayout(None,0,21,"layout19")

        self.textLabel4 = QLabel(self.frame8,"textLabel4")
        self.textLabel4.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.textLabel4.sizePolicy().hasHeightForWidth()))
        self.textLabel4.setPaletteForegroundColor(QColor(0,0,185))
        textLabel4_font = QFont(self.textLabel4.font())
        textLabel4_font.setPointSize(11)
        textLabel4_font.setBold(1)
        self.textLabel4.setFont(textLabel4_font)
        self.textLabel4.setFrameShadow(QLabel.Plain)
        self.textLabel4.setTextFormat(QLabel.AutoText)
        self.textLabel4.setScaledContents(1)
        self.textLabel4.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout19.addWidget(self.textLabel4)

        self.lineEditDataPrefix = QLineEdit(self.frame8,"lineEditDataPrefix")
        self.lineEditDataPrefix.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEditDataPrefix.sizePolicy().hasHeightForWidth()))
        self.lineEditDataPrefix.setMinimumSize(QSize(200,0))
        self.lineEditDataPrefix.setMaximumSize(QSize(32767,23))
        layout19.addWidget(self.lineEditDataPrefix)
        layout110.addLayout(layout19)

        layout44 = QHBoxLayout(None,0,21,"layout44")

        self.textLabel5 = QLabel(self.frame8,"textLabel5")
        self.textLabel5.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.textLabel5.sizePolicy().hasHeightForWidth()))
        self.textLabel5.setPaletteForegroundColor(QColor(0,0,185))
        textLabel5_font = QFont(self.textLabel5.font())
        textLabel5_font.setPointSize(11)
        textLabel5_font.setBold(1)
        self.textLabel5.setFont(textLabel5_font)
        self.textLabel5.setFrameShadow(QLabel.Plain)
        self.textLabel5.setTextFormat(QLabel.AutoText)
        self.textLabel5.setScaledContents(1)
        self.textLabel5.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout44.addWidget(self.textLabel5)

        self.lineEditDataSuff = QLineEdit(self.frame8,"lineEditDataSuff")
        self.lineEditDataSuff.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEditDataSuff.sizePolicy().hasHeightForWidth()))
        self.lineEditDataSuff.setMaximumSize(QSize(40,23))
        layout44.addWidget(self.lineEditDataSuff)
        layout110.addLayout(layout44)

        layout45 = QHBoxLayout(None,0,21,"layout45")

        self.textLabel6 = QLabel(self.frame8,"textLabel6")
        self.textLabel6.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.textLabel6.sizePolicy().hasHeightForWidth()))
        self.textLabel6.setPaletteForegroundColor(QColor(0,0,185))
        textLabel6_font = QFont(self.textLabel6.font())
        textLabel6_font.setPointSize(11)
        textLabel6_font.setBold(1)
        self.textLabel6.setFont(textLabel6_font)
        self.textLabel6.setFrameShadow(QLabel.Plain)
        self.textLabel6.setTextFormat(QLabel.AutoText)
        self.textLabel6.setScaledContents(1)
        self.textLabel6.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout45.addWidget(self.textLabel6)

        self.lineEditDataStart = QLineEdit(self.frame8,"lineEditDataStart")
        self.lineEditDataStart.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEditDataStart.sizePolicy().hasHeightForWidth()))
        self.lineEditDataStart.setMaximumSize(QSize(50,23))
        layout45.addWidget(self.lineEditDataStart)
        layout110.addLayout(layout45)

        layout46 = QHBoxLayout(None,0,21,"layout46")

        self.textLabel7 = QLabel(self.frame8,"textLabel7")
        self.textLabel7.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.textLabel7.sizePolicy().hasHeightForWidth()))
        self.textLabel7.setPaletteForegroundColor(QColor(0,0,185))
        textLabel7_font = QFont(self.textLabel7.font())
        textLabel7_font.setPointSize(11)
        textLabel7_font.setBold(1)
        self.textLabel7.setFont(textLabel7_font)
        self.textLabel7.setFrameShadow(QLabel.Plain)
        self.textLabel7.setTextFormat(QLabel.AutoText)
        self.textLabel7.setScaledContents(1)
        self.textLabel7.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout46.addWidget(self.textLabel7)

        self.lineEditDataEnd = QLineEdit(self.frame8,"lineEditDataEnd")
        self.lineEditDataEnd.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEditDataEnd.sizePolicy().hasHeightForWidth()))
        self.lineEditDataEnd.setMinimumSize(QSize(40,0))
        self.lineEditDataEnd.setMaximumSize(QSize(50,23))
        layout46.addWidget(self.lineEditDataEnd)
        layout110.addLayout(layout46)

        frame8Layout.addLayout(layout110,1,0)

        layout50 = QHBoxLayout(None,0,0,"layout50")

        self.textLabel3 = QLabel(self.frame8,"textLabel3")
        self.textLabel3.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.textLabel3.sizePolicy().hasHeightForWidth()))
        self.textLabel3.setPaletteForegroundColor(QColor(0,0,185))
        textLabel3_font = QFont(self.textLabel3.font())
        textLabel3_font.setPointSize(11)
        textLabel3_font.setBold(1)
        self.textLabel3.setFont(textLabel3_font)
        self.textLabel3.setFrameShadow(QLabel.Plain)
        self.textLabel3.setTextFormat(QLabel.AutoText)
        self.textLabel3.setScaledContents(1)
        self.textLabel3.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout50.addWidget(self.textLabel3)

        self.lineEditDataDir = QLineEdit(self.frame8,"lineEditDataDir")
        self.lineEditDataDir.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEditDataDir.sizePolicy().hasHeightForWidth()))
        self.lineEditDataDir.setMinimumSize(QSize(600,0))
        self.lineEditDataDir.setMaximumSize(QSize(32767,23))
        layout50.addWidget(self.lineEditDataDir)

        self.toolButton_DataDir = QToolButton(self.frame8,"toolButton_DataDir")
        layout50.addWidget(self.toolButton_DataDir)

        frame8Layout.addLayout(layout50,0,0)
        layout61.addWidget(self.frame8)

        self.frame1 = QFrame(self.tab,"frame1")
        self.frame1.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Fixed,0,0,self.frame1.sizePolicy().hasHeightForWidth()))
        self.frame1.setFrameShape(QFrame.Box)
        self.frame1.setFrameShadow(QFrame.Raised)
        frame1Layout = QGridLayout(self.frame1,1,1,11,21,"frame1Layout")

        self.checkBox_darks = QCheckBox(self.frame1,"checkBox_darks")
        self.checkBox_darks.setEnabled(1)
        self.checkBox_darks.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding,0,0,self.checkBox_darks.sizePolicy().hasHeightForWidth()))
        self.checkBox_darks.setMaximumSize(QSize(32767,30))
        self.checkBox_darks.setChecked(0)

        frame1Layout.addWidget(self.checkBox_darks,0,0)

        self.frame2 = QFrame(self.frame1,"frame2")
        self.frame2.setEnabled(0)
        self.frame2.setFrameShape(QFrame.StyledPanel)
        self.frame2.setFrameShadow(QFrame.Raised)
        frame2Layout = QGridLayout(self.frame2,1,1,11,21,"frame2Layout")

        layout48 = QHBoxLayout(None,0,21,"layout48")

        self.textLabel8 = QLabel(self.frame2,"textLabel8")
        self.textLabel8.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.textLabel8.sizePolicy().hasHeightForWidth()))
        self.textLabel8.setPaletteForegroundColor(QColor(0,0,185))
        textLabel8_font = QFont(self.textLabel8.font())
        textLabel8_font.setPointSize(11)
        textLabel8_font.setBold(1)
        self.textLabel8.setFont(textLabel8_font)
        self.textLabel8.setFrameShadow(QLabel.Plain)
        self.textLabel8.setTextFormat(QLabel.AutoText)
        self.textLabel8.setScaledContents(1)
        self.textLabel8.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout48.addWidget(self.textLabel8)

        self.lineEditDarkDir = QLineEdit(self.frame2,"lineEditDarkDir")
        self.lineEditDarkDir.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEditDarkDir.sizePolicy().hasHeightForWidth()))
        self.lineEditDarkDir.setMinimumSize(QSize(600,0))
        self.lineEditDarkDir.setMaximumSize(QSize(32767,23))
        layout48.addWidget(self.lineEditDarkDir)

        self.toolButton_DarkDir = QToolButton(self.frame2,"toolButton_DarkDir")
        layout48.addWidget(self.toolButton_DarkDir)

        frame2Layout.addMultiCellLayout(layout48,0,0,0,2)

        layout43 = QHBoxLayout(None,0,21,"layout43")

        self.textLabel10 = QLabel(self.frame2,"textLabel10")
        self.textLabel10.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.textLabel10.sizePolicy().hasHeightForWidth()))
        self.textLabel10.setPaletteForegroundColor(QColor(0,0,185))
        textLabel10_font = QFont(self.textLabel10.font())
        textLabel10_font.setPointSize(11)
        textLabel10_font.setBold(1)
        self.textLabel10.setFont(textLabel10_font)
        self.textLabel10.setFrameShadow(QLabel.Plain)
        self.textLabel10.setTextFormat(QLabel.AutoText)
        self.textLabel10.setScaledContents(1)
        self.textLabel10.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout43.addWidget(self.textLabel10)

        self.lineEditDarkStart = QLineEdit(self.frame2,"lineEditDarkStart")
        self.lineEditDarkStart.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEditDarkStart.sizePolicy().hasHeightForWidth()))
        self.lineEditDarkStart.setMinimumSize(QSize(50,0))
        self.lineEditDarkStart.setMaximumSize(QSize(40,23))
        layout43.addWidget(self.lineEditDarkStart)

        frame2Layout.addLayout(layout43,1,1)

        layout22 = QHBoxLayout(None,0,21,"layout22")

        self.textLabel11 = QLabel(self.frame2,"textLabel11")
        self.textLabel11.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.textLabel11.sizePolicy().hasHeightForWidth()))
        self.textLabel11.setPaletteForegroundColor(QColor(0,0,185))
        textLabel11_font = QFont(self.textLabel11.font())
        textLabel11_font.setPointSize(11)
        textLabel11_font.setBold(1)
        self.textLabel11.setFont(textLabel11_font)
        self.textLabel11.setFrameShadow(QLabel.Plain)
        self.textLabel11.setTextFormat(QLabel.AutoText)
        self.textLabel11.setScaledContents(1)
        self.textLabel11.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout22.addWidget(self.textLabel11)

        self.lineEditDarkEnd = QLineEdit(self.frame2,"lineEditDarkEnd")
        self.lineEditDarkEnd.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEditDarkEnd.sizePolicy().hasHeightForWidth()))
        self.lineEditDarkEnd.setMinimumSize(QSize(50,0))
        self.lineEditDarkEnd.setMaximumSize(QSize(50,23))
        layout22.addWidget(self.lineEditDarkEnd)

        frame2Layout.addLayout(layout22,1,2)

        layout42 = QHBoxLayout(None,0,21,"layout42")

        self.textLabel9 = QLabel(self.frame2,"textLabel9")
        self.textLabel9.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.textLabel9.sizePolicy().hasHeightForWidth()))
        self.textLabel9.setPaletteForegroundColor(QColor(0,0,185))
        textLabel9_font = QFont(self.textLabel9.font())
        textLabel9_font.setPointSize(11)
        textLabel9_font.setBold(1)
        self.textLabel9.setFont(textLabel9_font)
        self.textLabel9.setFrameShadow(QLabel.Plain)
        self.textLabel9.setTextFormat(QLabel.AutoText)
        self.textLabel9.setScaledContents(1)
        self.textLabel9.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout42.addWidget(self.textLabel9)

        self.lineEditDarkPrefix = QLineEdit(self.frame2,"lineEditDarkPrefix")
        self.lineEditDarkPrefix.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEditDarkPrefix.sizePolicy().hasHeightForWidth()))
        self.lineEditDarkPrefix.setMinimumSize(QSize(200,0))
        self.lineEditDarkPrefix.setMaximumSize(QSize(32767,23))
        layout42.addWidget(self.lineEditDarkPrefix)

        frame2Layout.addLayout(layout42,1,0)

        frame1Layout.addWidget(self.frame2,0,1)
        layout61.addWidget(self.frame1)
        layout62.addLayout(layout61)

        layout60 = QHBoxLayout(None,0,21,"layout60")

        self.frame14 = QFrame(self.tab,"frame14")
        self.frame14.setFrameShape(QFrame.StyledPanel)
        self.frame14.setFrameShadow(QFrame.Raised)
        self.frame14.setMargin(0)
        frame14Layout = QGridLayout(self.frame14,1,1,11,21,"frame14Layout")

        layout69 = QVBoxLayout(None,0,0,"layout69")

        layout60_2 = QHBoxLayout(None,0,21,"layout60_2")

        self.buttonGroup1 = QButtonGroup(self.frame14,"buttonGroup1")
        self.buttonGroup1.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.buttonGroup1.sizePolicy().hasHeightForWidth()))
        self.buttonGroup1.setPaletteForegroundColor(QColor(0,115,0))
        self.buttonGroup1.setAlignment(QButtonGroup.AlignTop | QButtonGroup.AlignHCenter)
        self.buttonGroup1.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup1.layout().setSpacing(21)
        self.buttonGroup1.layout().setMargin(11)
        buttonGroup1Layout = QGridLayout(self.buttonGroup1.layout())
        buttonGroup1Layout.setAlignment(Qt.AlignTop)

        layout51 = QVBoxLayout(None,0,21,"layout51")

        self.comboBox_detector = QComboBox(0,self.buttonGroup1,"comboBox_detector")
        layout51.addWidget(self.comboBox_detector)

        layout49 = QHBoxLayout(None,0,0,"layout49")

        self.checkBox_flatfield = QCheckBox(self.buttonGroup1,"checkBox_flatfield")
        self.checkBox_flatfield.setEnabled(1)
        self.checkBox_flatfield.setMaximumSize(QSize(67,32767))
        self.checkBox_flatfield.setPaletteForegroundColor(QColor(0,0,0))
        self.checkBox_flatfield.setChecked(0)
        layout49.addWidget(self.checkBox_flatfield)

        self.comboBox_flatfield = QComboBox(0,self.buttonGroup1,"comboBox_flatfield")
        self.comboBox_flatfield.setEnabled(0)
        self.comboBox_flatfield.setSizeLimit(10)
        layout49.addWidget(self.comboBox_flatfield)
        layout51.addLayout(layout49)

        layout48_2 = QHBoxLayout(None,0,0,"layout48_2")

        self.lineEdit_other = QLineEdit(self.buttonGroup1,"lineEdit_other")
        layout48_2.addWidget(self.lineEdit_other)
        layout51.addLayout(layout48_2)

        buttonGroup1Layout.addLayout(layout51,0,0)
        layout60_2.addWidget(self.buttonGroup1)

        self.buttonGroup2 = QButtonGroup(self.frame14,"buttonGroup2")
        self.buttonGroup2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.buttonGroup2.sizePolicy().hasHeightForWidth()))
        self.buttonGroup2.setPaletteForegroundColor(QColor(0,115,0))
        self.buttonGroup2.setAlignment(QButtonGroup.AlignTop | QButtonGroup.AlignHCenter)
        self.buttonGroup2.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup2.layout().setSpacing(21)
        self.buttonGroup2.layout().setMargin(11)
        buttonGroup2Layout = QGridLayout(self.buttonGroup2.layout())
        buttonGroup2Layout.setAlignment(Qt.AlignTop)

        layout4 = QVBoxLayout(None,0,21,"layout4")

        self.radioButton3 = QRadioButton(self.buttonGroup2,"radioButton3")
        self.radioButton3.setChecked(1)
        layout4.addWidget(self.radioButton3)

        self.radioButton4 = QRadioButton(self.buttonGroup2,"radioButton4")
        self.radioButton4.setChecked(0)
        layout4.addWidget(self.radioButton4)

        self.radioButton5 = QRadioButton(self.buttonGroup2,"radioButton5")
        layout4.addWidget(self.radioButton5)

        buttonGroup2Layout.addLayout(layout4,0,0)
        layout60_2.addWidget(self.buttonGroup2)
        layout69.addLayout(layout60_2)

        self.groupBox4 = QGroupBox(self.frame14,"groupBox4")
        self.groupBox4.setFrameShape(QGroupBox.NoFrame)
        self.groupBox4.setAlignment(QGroupBox.AlignCenter)
        self.groupBox4.setColumnLayout(0,Qt.Vertical)
        self.groupBox4.layout().setSpacing(21)
        self.groupBox4.layout().setMargin(11)
        groupBox4Layout = QGridLayout(self.groupBox4.layout())
        groupBox4Layout.setAlignment(Qt.AlignTop)

        layout63 = QHBoxLayout(None,0,21,"layout63")

        self.checkBox_droplet = QCheckBox(self.groupBox4,"checkBox_droplet")
        self.checkBox_droplet.setEnabled(0)
        layout63.addWidget(self.checkBox_droplet)

        self.groupBox3 = QGroupBox(self.groupBox4,"groupBox3")
        self.groupBox3.setEnabled(0)
        self.groupBox3.setFrameShape(QGroupBox.NoFrame)
        self.groupBox3.setAlignment(QGroupBox.AlignCenter)
        self.groupBox3.setColumnLayout(0,Qt.Vertical)
        self.groupBox3.layout().setSpacing(21)
        self.groupBox3.layout().setMargin(11)
        groupBox3Layout = QGridLayout(self.groupBox3.layout())
        groupBox3Layout.setAlignment(Qt.AlignTop)

        layout59 = QVBoxLayout(None,0,0,"layout59")

        layout55_2 = QHBoxLayout(None,0,0,"layout55_2")

        self.textLabel_photonadu_2 = QLabel(self.groupBox3,"textLabel_photonadu_2")
        self.textLabel_photonadu_2.setMaximumSize(QSize(100,32767))
        layout55_2.addWidget(self.textLabel_photonadu_2)

        self.lineEdit_0PhotADU = QLineEdit(self.groupBox3,"lineEdit_0PhotADU")
        layout55_2.addWidget(self.lineEdit_0PhotADU)

        self.textLabel_sigmaphoton_2 = QLabel(self.groupBox3,"textLabel_sigmaphoton_2")
        self.textLabel_sigmaphoton_2.setMaximumSize(QSize(30,32767))
        layout55_2.addWidget(self.textLabel_sigmaphoton_2)

        self.lineEdit_0PhotSigma = QLineEdit(self.groupBox3,"lineEdit_0PhotSigma")
        layout55_2.addWidget(self.lineEdit_0PhotSigma)
        layout59.addLayout(layout55_2)

        layout55 = QHBoxLayout(None,0,0,"layout55")

        self.textLabel_photonadu = QLabel(self.groupBox3,"textLabel_photonadu")
        self.textLabel_photonadu.setMaximumSize(QSize(100,32767))
        layout55.addWidget(self.textLabel_photonadu)

        self.lineEdit_1PhotADU = QLineEdit(self.groupBox3,"lineEdit_1PhotADU")
        layout55.addWidget(self.lineEdit_1PhotADU)

        self.textLabel_sigmaphoton = QLabel(self.groupBox3,"textLabel_sigmaphoton")
        self.textLabel_sigmaphoton.setMaximumSize(QSize(30,32767))
        layout55.addWidget(self.textLabel_sigmaphoton)

        self.lineEdit_1PhotSigma = QLineEdit(self.groupBox3,"lineEdit_1PhotSigma")
        layout55.addWidget(self.lineEdit_1PhotSigma)
        layout59.addLayout(layout55)

        groupBox3Layout.addLayout(layout59,0,0)
        layout63.addWidget(self.groupBox3)

        groupBox4Layout.addLayout(layout63,0,0)
        layout69.addWidget(self.groupBox4)

        frame14Layout.addLayout(layout69,0,0)
        layout60.addWidget(self.frame14)

        layout59_2 = QVBoxLayout(None,0,21,"layout59_2")

        self.frame10 = QFrame(self.tab,"frame10")
        self.frame10.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.frame10.sizePolicy().hasHeightForWidth()))
        self.frame10.setMaximumSize(QSize(32767,32767))
        self.frame10.setFrameShape(QFrame.Box)
        self.frame10.setFrameShadow(QFrame.Raised)
        frame10Layout = QGridLayout(self.frame10,1,1,11,21,"frame10Layout")

        layout66 = QVBoxLayout(None,0,21,"layout66")

        self.splitter12 = QSplitter(self.frame10,"splitter12")
        self.splitter12.setOrientation(QSplitter.Horizontal)

        self.textLabel12 = QLabel(self.splitter12,"textLabel12")
        self.textLabel12.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.textLabel12.sizePolicy().hasHeightForWidth()))
        self.textLabel12.setMaximumSize(QSize(170,32767))
        self.textLabel12.setPaletteForegroundColor(QColor(255,85,0))
        textLabel12_font = QFont(self.textLabel12.font())
        textLabel12_font.setPointSize(11)
        textLabel12_font.setBold(1)
        self.textLabel12.setFont(textLabel12_font)
        self.textLabel12.setFrameShadow(QLabel.Plain)
        self.textLabel12.setTextFormat(QLabel.AutoText)
        self.textLabel12.setScaledContents(1)
        self.textLabel12.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        self.lineEdit12 = QLineEdit(self.splitter12,"lineEdit12")
        self.lineEdit12.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit12.sizePolicy().hasHeightForWidth()))
        self.lineEdit12.setMinimumSize(QSize(300,20))
        self.lineEdit12.setMaximumSize(QSize(32767,23))

        self.toolButton_outdir = QToolButton(self.splitter12,"toolButton_outdir")
        layout66.addWidget(self.splitter12)

        self.splitter13 = QSplitter(self.frame10,"splitter13")
        self.splitter13.setOrientation(QSplitter.Horizontal)

        self.textLabel13 = QLabel(self.splitter13,"textLabel13")
        self.textLabel13.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.textLabel13.sizePolicy().hasHeightForWidth()))
        self.textLabel13.setMaximumSize(QSize(170,32767))
        self.textLabel13.setPaletteForegroundColor(QColor(255,85,0))
        textLabel13_font = QFont(self.textLabel13.font())
        textLabel13_font.setPointSize(11)
        textLabel13_font.setBold(1)
        self.textLabel13.setFont(textLabel13_font)
        self.textLabel13.setFrameShadow(QLabel.Plain)
        self.textLabel13.setTextFormat(QLabel.AutoText)
        self.textLabel13.setScaledContents(1)
        self.textLabel13.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        self.lineEdit13 = QLineEdit(self.splitter13,"lineEdit13")
        self.lineEdit13.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit13.sizePolicy().hasHeightForWidth()))
        self.lineEdit13.setMinimumSize(QSize(200,20))
        self.lineEdit13.setMaximumSize(QSize(32767,23))
        layout66.addWidget(self.splitter13)

        frame10Layout.addLayout(layout66,0,0)
        layout59_2.addWidget(self.frame10)

        self.frame11 = QFrame(self.tab,"frame11")
        self.frame11.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.frame11.sizePolicy().hasHeightForWidth()))
        self.frame11.setMaximumSize(QSize(32767,150))
        self.frame11.setFrameShape(QFrame.Box)
        self.frame11.setFrameShadow(QFrame.Raised)
        frame11Layout = QGridLayout(self.frame11,1,1,11,21,"frame11Layout")
        spacer3 = QSpacerItem(21,46,QSizePolicy.Minimum,QSizePolicy.Expanding)
        frame11Layout.addItem(spacer3,1,2)

        layout49_2 = QVBoxLayout(None,0,21,"layout49_2")

        layout30 = QHBoxLayout(None,0,21,"layout30")

        self.textLabel15 = QLabel(self.frame11,"textLabel15")
        self.textLabel15.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.textLabel15.sizePolicy().hasHeightForWidth()))
        self.textLabel15.setPaletteForegroundColor(QColor(0,115,0))
        textLabel15_font = QFont(self.textLabel15.font())
        textLabel15_font.setPointSize(11)
        textLabel15_font.setBold(1)
        self.textLabel15.setFont(textLabel15_font)
        self.textLabel15.setFrameShadow(QLabel.Plain)
        self.textLabel15.setTextFormat(QLabel.AutoText)
        self.textLabel15.setScaledContents(1)
        self.textLabel15.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout30.addWidget(self.textLabel15)

        self.lineEdit_dsd = QLineEdit(self.frame11,"lineEdit_dsd")
        self.lineEdit_dsd.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit_dsd.sizePolicy().hasHeightForWidth()))
        self.lineEdit_dsd.setMinimumSize(QSize(35,23))
        self.lineEdit_dsd.setMaximumSize(QSize(50,23))
        layout30.addWidget(self.lineEdit_dsd)
        layout49_2.addLayout(layout30)

        layout31 = QHBoxLayout(None,0,21,"layout31")

        self.textLabel16 = QLabel(self.frame11,"textLabel16")
        self.textLabel16.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.textLabel16.sizePolicy().hasHeightForWidth()))
        self.textLabel16.setPaletteForegroundColor(QColor(0,115,0))
        textLabel16_font = QFont(self.textLabel16.font())
        textLabel16_font.setPointSize(11)
        textLabel16_font.setBold(1)
        self.textLabel16.setFont(textLabel16_font)
        self.textLabel16.setFrameShadow(QLabel.Plain)
        self.textLabel16.setTextFormat(QLabel.LogText)
        self.textLabel16.setScaledContents(1)
        self.textLabel16.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout31.addWidget(self.textLabel16)

        self.lineEdit_lambda = QLineEdit(self.frame11,"lineEdit_lambda")
        self.lineEdit_lambda.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit_lambda.sizePolicy().hasHeightForWidth()))
        self.lineEdit_lambda.setMaximumSize(QSize(50,23))
        layout31.addWidget(self.lineEdit_lambda)
        layout49_2.addLayout(layout31)

        layout32 = QHBoxLayout(None,0,21,"layout32")

        self.textLabel17 = QLabel(self.frame11,"textLabel17")
        self.textLabel17.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.textLabel17.sizePolicy().hasHeightForWidth()))
        self.textLabel17.setPaletteForegroundColor(QColor(0,115,0))
        textLabel17_font = QFont(self.textLabel17.font())
        textLabel17_font.setPointSize(11)
        textLabel17_font.setBold(1)
        self.textLabel17.setFont(textLabel17_font)
        self.textLabel17.setFrameShadow(QLabel.Plain)
        self.textLabel17.setTextFormat(QLabel.AutoText)
        self.textLabel17.setScaledContents(1)
        self.textLabel17.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout32.addWidget(self.textLabel17)

        self.lineEdit17 = QLineEdit(self.frame11,"lineEdit17")
        self.lineEdit17.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit17.sizePolicy().hasHeightForWidth()))
        self.lineEdit17.setMaximumSize(QSize(50,23))
        layout32.addWidget(self.lineEdit17)
        layout49_2.addLayout(layout32)

        frame11Layout.addMultiCellLayout(layout49_2,0,1,0,0)

        layout50_2 = QVBoxLayout(None,0,21,"layout50_2")

        layout56 = QHBoxLayout(None,0,21,"layout56")

        self.textLabel19 = QLabel(self.frame11,"textLabel19")
        self.textLabel19.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.textLabel19.sizePolicy().hasHeightForWidth()))
        self.textLabel19.setMaximumSize(QSize(200,32767))
        self.textLabel19.setPaletteForegroundColor(QColor(0,115,0))
        textLabel19_font = QFont(self.textLabel19.font())
        textLabel19_font.setPointSize(11)
        textLabel19_font.setBold(1)
        self.textLabel19.setFont(textLabel19_font)
        self.textLabel19.setFrameShadow(QLabel.Plain)
        self.textLabel19.setTextFormat(QLabel.AutoText)
        self.textLabel19.setScaledContents(1)
        self.textLabel19.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout56.addWidget(self.textLabel19)

        self.lineEdit18 = QLineEdit(self.frame11,"lineEdit18")
        self.lineEdit18.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit18.sizePolicy().hasHeightForWidth()))
        self.lineEdit18.setMaximumSize(QSize(50,23))
        layout56.addWidget(self.lineEdit18)
        layout50_2.addLayout(layout56)

        layout55_3 = QHBoxLayout(None,0,21,"layout55_3")

        self.textLabel20 = QLabel(self.frame11,"textLabel20")
        self.textLabel20.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.textLabel20.sizePolicy().hasHeightForWidth()))
        self.textLabel20.setMaximumSize(QSize(200,32767))
        self.textLabel20.setPaletteForegroundColor(QColor(0,115,0))
        textLabel20_font = QFont(self.textLabel20.font())
        textLabel20_font.setPointSize(11)
        textLabel20_font.setBold(1)
        self.textLabel20.setFont(textLabel20_font)
        self.textLabel20.setFrameShadow(QLabel.Plain)
        self.textLabel20.setTextFormat(QLabel.AutoText)
        self.textLabel20.setScaledContents(1)
        self.textLabel20.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout55_3.addWidget(self.textLabel20)

        self.lineEdit19 = QLineEdit(self.frame11,"lineEdit19")
        self.lineEdit19.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit19.sizePolicy().hasHeightForWidth()))
        self.lineEdit19.setMaximumSize(QSize(50,23))
        layout55_3.addWidget(self.lineEdit19)
        layout50_2.addLayout(layout55_3)

        layout54 = QHBoxLayout(None,0,21,"layout54")

        self.textLabel22 = QLabel(self.frame11,"textLabel22")
        self.textLabel22.setEnabled(0)
        self.textLabel22.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.textLabel22.sizePolicy().hasHeightForWidth()))
        self.textLabel22.setMaximumSize(QSize(200,32767))
        self.textLabel22.setPaletteForegroundColor(QColor(0,115,0))
        textLabel22_font = QFont(self.textLabel22.font())
        textLabel22_font.setPointSize(11)
        textLabel22_font.setBold(1)
        self.textLabel22.setFont(textLabel22_font)
        self.textLabel22.setFrameShadow(QLabel.Plain)
        self.textLabel22.setTextFormat(QLabel.AutoText)
        self.textLabel22.setScaledContents(1)
        self.textLabel22.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout54.addWidget(self.textLabel22)

        self.lineEdit20 = QLineEdit(self.frame11,"lineEdit20")
        self.lineEdit20.setEnabled(0)
        self.lineEdit20.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit20.sizePolicy().hasHeightForWidth()))
        self.lineEdit20.setMaximumSize(QSize(50,23))
        layout54.addWidget(self.lineEdit20)
        layout50_2.addLayout(layout54)

        frame11Layout.addMultiCellLayout(layout50_2,0,1,1,1)

        self.groupBox2 = QGroupBox(self.frame11,"groupBox2")
        self.groupBox2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.groupBox2.sizePolicy().hasHeightForWidth()))
        self.groupBox2.setPaletteForegroundColor(QColor(0,115,0))
        groupBox2_font = QFont(self.groupBox2.font())
        groupBox2_font.setPointSize(11)
        groupBox2_font.setBold(1)
        self.groupBox2.setFont(groupBox2_font)
        self.groupBox2.setAlignment(QGroupBox.AlignHCenter)
        self.groupBox2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2.layout().setSpacing(21)
        self.groupBox2.layout().setMargin(11)
        groupBox2Layout = QGridLayout(self.groupBox2.layout())
        groupBox2Layout.setAlignment(Qt.AlignTop)

        self.comboBox_normalize = QComboBox(0,self.groupBox2,"comboBox_normalize")
        self.comboBox_normalize.setEnabled(1)
        comboBox_normalize_font = QFont(self.comboBox_normalize.font())
        comboBox_normalize_font.setBold(0)
        self.comboBox_normalize.setFont(comboBox_normalize_font)

        groupBox2Layout.addWidget(self.comboBox_normalize,0,0)

        frame11Layout.addWidget(self.groupBox2,0,2)
        layout59_2.addWidget(self.frame11)
        layout60.addLayout(layout59_2)
        layout62.addLayout(layout60)

        self.frame12 = QFrame(self.tab,"frame12")
        self.frame12.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.frame12.sizePolicy().hasHeightForWidth()))
        self.frame12.setMaximumSize(QSize(32767,32767))
        self.frame12.setFrameShape(QFrame.Box)
        self.frame12.setFrameShadow(QFrame.Raised)
        frame12Layout = QGridLayout(self.frame12,1,1,11,21,"frame12Layout")

        layout100 = QHBoxLayout(None,0,21,"layout100")

        self.textLabel_qTRC = QLabel(self.frame12,"textLabel_qTRC")
        self.textLabel_qTRC.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.textLabel_qTRC.sizePolicy().hasHeightForWidth()))
        self.textLabel_qTRC.setPaletteForegroundColor(QColor(240,22,25))
        textLabel_qTRC_font = QFont(self.textLabel_qTRC.font())
        textLabel_qTRC_font.setPointSize(11)
        textLabel_qTRC_font.setBold(1)
        self.textLabel_qTRC.setFont(textLabel_qTRC_font)
        self.textLabel_qTRC.setFrameShadow(QLabel.Plain)
        self.textLabel_qTRC.setTextFormat(QLabel.AutoText)
        self.textLabel_qTRC.setScaledContents(1)
        self.textLabel_qTRC.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout100.addWidget(self.textLabel_qTRC)

        self.lineEdit_qTRC = QLineEdit(self.frame12,"lineEdit_qTRC")
        self.lineEdit_qTRC.setMaximumSize(QSize(40,23))
        layout100.addWidget(self.lineEdit_qTRC)

        frame12Layout.addLayout(layout100,1,0)

        layout101 = QHBoxLayout(None,0,21,"layout101")

        self.textLabel28 = QLabel(self.frame12,"textLabel28")
        self.textLabel28.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.textLabel28.sizePolicy().hasHeightForWidth()))
        self.textLabel28.setPaletteForegroundColor(QColor(240,22,25))
        textLabel28_font = QFont(self.textLabel28.font())
        textLabel28_font.setPointSize(11)
        textLabel28_font.setBold(1)
        self.textLabel28.setFont(textLabel28_font)
        self.textLabel28.setFrameShadow(QLabel.Plain)
        self.textLabel28.setTextFormat(QLabel.AutoText)
        self.textLabel28.setScaledContents(1)
        self.textLabel28.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout101.addWidget(self.textLabel28)

        self.lineEdit_tolerance = QLineEdit(self.frame12,"lineEdit_tolerance")
        self.lineEdit_tolerance.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit_tolerance.sizePolicy().hasHeightForWidth()))
        self.lineEdit_tolerance.setMaximumSize(QSize(40,23))
        self.lineEdit_tolerance.setAlignment(QLineEdit.AlignAuto)
        layout101.addWidget(self.lineEdit_tolerance)

        frame12Layout.addLayout(layout101,0,0)

        layout103 = QHBoxLayout(None,0,21,"layout103")

        self.textLabel29 = QLabel(self.frame12,"textLabel29")
        self.textLabel29.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.textLabel29.sizePolicy().hasHeightForWidth()))
        self.textLabel29.setPaletteForegroundColor(QColor(240,22,25))
        textLabel29_font = QFont(self.textLabel29.font())
        textLabel29_font.setPointSize(11)
        textLabel29_font.setBold(1)
        self.textLabel29.setFont(textLabel29_font)
        self.textLabel29.setFrameShadow(QLabel.Plain)
        self.textLabel29.setTextFormat(QLabel.AutoText)
        self.textLabel29.setScaledContents(1)
        self.textLabel29.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout103.addWidget(self.textLabel29)

        self.lineEdit_firstq = QLineEdit(self.frame12,"lineEdit_firstq")
        self.lineEdit_firstq.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit_firstq.sizePolicy().hasHeightForWidth()))
        self.lineEdit_firstq.setMaximumSize(QSize(70,23))
        layout103.addWidget(self.lineEdit_firstq)

        frame12Layout.addLayout(layout103,0,1)

        layout104 = QHBoxLayout(None,0,21,"layout104")

        self.textLabel31 = QLabel(self.frame12,"textLabel31")
        self.textLabel31.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.textLabel31.sizePolicy().hasHeightForWidth()))
        self.textLabel31.setPaletteForegroundColor(QColor(240,22,25))
        textLabel31_font = QFont(self.textLabel31.font())
        textLabel31_font.setPointSize(11)
        textLabel31_font.setBold(1)
        self.textLabel31.setFont(textLabel31_font)
        self.textLabel31.setFrameShadow(QLabel.Plain)
        self.textLabel31.setTextFormat(QLabel.AutoText)
        self.textLabel31.setScaledContents(1)
        self.textLabel31.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout104.addWidget(self.textLabel31)

        self.lineEdit28 = QLineEdit(self.frame12,"lineEdit28")
        self.lineEdit28.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit28.sizePolicy().hasHeightForWidth()))
        self.lineEdit28.setMaximumSize(QSize(70,23))
        layout104.addWidget(self.lineEdit28)

        frame12Layout.addLayout(layout104,0,2)

        layout105 = QHBoxLayout(None,0,21,"layout105")

        self.textLabel32 = QLabel(self.frame12,"textLabel32")
        self.textLabel32.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.textLabel32.sizePolicy().hasHeightForWidth()))
        self.textLabel32.setPaletteForegroundColor(QColor(240,22,25))
        textLabel32_font = QFont(self.textLabel32.font())
        textLabel32_font.setPointSize(11)
        textLabel32_font.setBold(1)
        self.textLabel32.setFont(textLabel32_font)
        self.textLabel32.setFrameShadow(QLabel.Plain)
        self.textLabel32.setTextFormat(QLabel.AutoText)
        self.textLabel32.setScaledContents(1)
        self.textLabel32.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout105.addWidget(self.textLabel32)

        self.lineEdit_nq = QLineEdit(self.frame12,"lineEdit_nq")
        self.lineEdit_nq.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit_nq.sizePolicy().hasHeightForWidth()))
        self.lineEdit_nq.setMaximumSize(QSize(70,23))
        layout105.addWidget(self.lineEdit_nq)

        frame12Layout.addLayout(layout105,1,2)

        layout102 = QHBoxLayout(None,0,21,"layout102")

        self.textLabel30 = QLabel(self.frame12,"textLabel30")
        self.textLabel30.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.textLabel30.sizePolicy().hasHeightForWidth()))
        self.textLabel30.setPaletteForegroundColor(QColor(240,22,25))
        textLabel30_font = QFont(self.textLabel30.font())
        textLabel30_font.setPointSize(11)
        textLabel30_font.setBold(1)
        self.textLabel30.setFont(textLabel30_font)
        self.textLabel30.setFrameShadow(QLabel.Plain)
        self.textLabel30.setTextFormat(QLabel.AutoText)
        self.textLabel30.setScaledContents(1)
        self.textLabel30.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout102.addWidget(self.textLabel30)

        self.lineEdit27 = QLineEdit(self.frame12,"lineEdit27")
        self.lineEdit27.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.lineEdit27.sizePolicy().hasHeightForWidth()))
        self.lineEdit27.setMaximumSize(QSize(70,23))
        layout102.addWidget(self.lineEdit27)

        frame12Layout.addLayout(layout102,1,1)
        layout62.addWidget(self.frame12)

        tabLayout.addLayout(layout62,0,0)
        self.tabWidget1.insertTab(self.tab,QString.fromLatin1(""))

        self.TabPage = QWidget(self.tabWidget1,"TabPage")
        TabPageLayout = QGridLayout(self.TabPage,1,1,11,21,"TabPageLayout")

        layout61_2 = QVBoxLayout(None,0,0,"layout61_2")

        layout60_3 = QHBoxLayout(None,0,21,"layout60_3")

        self.frame11_2 = QFrame(self.TabPage,"frame11_2")
        self.frame11_2.setFrameShape(QFrame.StyledPanel)
        self.frame11_2.setFrameShadow(QFrame.Raised)
        self.frame11_2.setMargin(0)
        frame11_2Layout = QVBoxLayout(self.frame11_2,11,3,"frame11_2Layout")

        self.splitter11 = QSplitter(self.frame11_2,"splitter11")
        self.splitter11.setOrientation(QSplitter.Horizontal)

        self.Staticdata_label = QLabel(self.splitter11,"Staticdata_label")
        self.Staticdata_label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.Staticdata_label.sizePolicy().hasHeightForWidth()))
        self.Staticdata_label.setMaximumSize(QSize(120,32767))
        self.Staticdata_label.setPaletteForegroundColor(QColor(0,0,255))
        Staticdata_label_font = QFont(self.Staticdata_label.font())
        Staticdata_label_font.setBold(1)
        self.Staticdata_label.setFont(Staticdata_label_font)

        self.lineEdit_data = QLineEdit(self.splitter11,"lineEdit_data")
        self.lineEdit_data.setEnabled(0)
        self.lineEdit_data.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.lineEdit_data.sizePolicy().hasHeightForWidth()))
        self.lineEdit_data.setMinimumSize(QSize(600,0))
        self.lineEdit_data.setMaximumSize(QSize(860,23))
        self.lineEdit_data.setPaletteForegroundColor(QColor(116,114,116))
        frame11_2Layout.addWidget(self.splitter11)

        self.splitter16 = QSplitter(self.frame11_2,"splitter16")
        self.splitter16.setOrientation(QSplitter.Horizontal)

        self.mask_label = QLabel(self.splitter16,"mask_label")
        self.mask_label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.mask_label.sizePolicy().hasHeightForWidth()))
        self.mask_label.setMaximumSize(QSize(120,32767))
        self.mask_label.setPaletteForegroundColor(QColor(0,0,255))
        mask_label_font = QFont(self.mask_label.font())
        mask_label_font.setBold(1)
        self.mask_label.setFont(mask_label_font)

        self.lineEdit_mask = QLineEdit(self.splitter16,"lineEdit_mask")
        self.lineEdit_mask.setEnabled(1)
        self.lineEdit_mask.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.lineEdit_mask.sizePolicy().hasHeightForWidth()))
        self.lineEdit_mask.setMinimumSize(QSize(600,0))
        self.lineEdit_mask.setMaximumSize(QSize(860,23))
        self.lineEdit_mask.setPaletteForegroundColor(QColor(0,0,0))

        self.toolButtonMaskFile = QToolButton(self.splitter16,"toolButtonMaskFile")
        self.toolButtonMaskFile.setMaximumSize(QSize(40,32767))
        frame11_2Layout.addWidget(self.splitter16)

        self.splitter15 = QSplitter(self.frame11_2,"splitter15")
        self.splitter15.setOrientation(QSplitter.Horizontal)

        self.dark_label = QLabel(self.splitter15,"dark_label")
        self.dark_label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.dark_label.sizePolicy().hasHeightForWidth()))
        self.dark_label.setMaximumSize(QSize(120,32767))
        self.dark_label.setPaletteForegroundColor(QColor(0,0,255))
        dark_label_font = QFont(self.dark_label.font())
        dark_label_font.setBold(1)
        self.dark_label.setFont(dark_label_font)

        self.lineEdit_dark = QLineEdit(self.splitter15,"lineEdit_dark")
        self.lineEdit_dark.setEnabled(1)
        self.lineEdit_dark.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.lineEdit_dark.sizePolicy().hasHeightForWidth()))
        self.lineEdit_dark.setMinimumSize(QSize(600,0))
        self.lineEdit_dark.setMaximumSize(QSize(860,23))
        self.lineEdit_dark.setPaletteForegroundColor(QColor(0,0,0))

        self.toolButtonDarkFile = QToolButton(self.splitter15,"toolButtonDarkFile")
        self.toolButtonDarkFile.setMaximumSize(QSize(40,32767))
        frame11_2Layout.addWidget(self.splitter15)

        self.splitter14 = QSplitter(self.frame11_2,"splitter14")
        self.splitter14.setOrientation(QSplitter.Horizontal)

        self.qmask_label = QLabel(self.splitter14,"qmask_label")
        self.qmask_label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.qmask_label.sizePolicy().hasHeightForWidth()))
        self.qmask_label.setMaximumSize(QSize(120,32767))
        self.qmask_label.setPaletteForegroundColor(QColor(0,0,255))
        qmask_label_font = QFont(self.qmask_label.font())
        qmask_label_font.setBold(1)
        self.qmask_label.setFont(qmask_label_font)

        self.lineEdit_qmask = QLineEdit(self.splitter14,"lineEdit_qmask")
        self.lineEdit_qmask.setEnabled(0)
        self.lineEdit_qmask.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.lineEdit_qmask.sizePolicy().hasHeightForWidth()))
        self.lineEdit_qmask.setMinimumSize(QSize(600,0))
        self.lineEdit_qmask.setMaximumSize(QSize(860,23))
        self.lineEdit_qmask.setPaletteForegroundColor(QColor(116,114,116))
        frame11_2Layout.addWidget(self.splitter14)
        layout60_3.addWidget(self.frame11_2)

        self.frame10_2 = QFrame(self.TabPage,"frame10_2")
        self.frame10_2.setMaximumSize(QSize(250,32767))
        self.frame10_2.setFrameShape(QFrame.StyledPanel)
        self.frame10_2.setFrameShadow(QFrame.Raised)
        self.frame10_2.setLineWidth(1)
        frame10_2Layout = QVBoxLayout(self.frame10_2,11,0,"frame10_2Layout")

        self.splitter15_2 = QSplitter(self.frame10_2,"splitter15_2")
        self.splitter15_2.setOrientation(QSplitter.Horizontal)

        self.textLabel29_2 = QLabel(self.splitter15_2,"textLabel29_2")
        self.textLabel29_2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.textLabel29_2.sizePolicy().hasHeightForWidth()))
        self.textLabel29_2.setMaximumSize(QSize(140,32767))
        self.textLabel29_2.setPaletteForegroundColor(QColor(240,22,25))
        textLabel29_2_font = QFont(self.textLabel29_2.font())
        textLabel29_2_font.setPointSize(11)
        textLabel29_2_font.setBold(1)
        self.textLabel29_2.setFont(textLabel29_2_font)
        self.textLabel29_2.setFrameShadow(QLabel.Plain)
        self.textLabel29_2.setTextFormat(QLabel.AutoText)
        self.textLabel29_2.setScaledContents(1)
        self.textLabel29_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        self.lineEdit_firstq_2 = QLineEdit(self.splitter15_2,"lineEdit_firstq_2")
        self.lineEdit_firstq_2.setMaximumSize(QSize(80,23))
        frame10_2Layout.addWidget(self.splitter15_2)

        self.splitter9 = QSplitter(self.frame10_2,"splitter9")
        self.splitter9.setOrientation(QSplitter.Horizontal)

        self.textLabel30_2 = QLabel(self.splitter9,"textLabel30_2")
        self.textLabel30_2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.textLabel30_2.sizePolicy().hasHeightForWidth()))
        self.textLabel30_2.setMaximumSize(QSize(140,32767))
        self.textLabel30_2.setPaletteForegroundColor(QColor(240,22,25))
        textLabel30_2_font = QFont(self.textLabel30_2.font())
        textLabel30_2_font.setPointSize(11)
        textLabel30_2_font.setBold(1)
        self.textLabel30_2.setFont(textLabel30_2_font)
        self.textLabel30_2.setFrameShadow(QLabel.Plain)
        self.textLabel30_2.setTextFormat(QLabel.AutoText)
        self.textLabel30_2.setScaledContents(1)
        self.textLabel30_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        self.lineEdit_deltaq_2 = QLineEdit(self.splitter9,"lineEdit_deltaq_2")
        self.lineEdit_deltaq_2.setMaximumSize(QSize(80,23))
        frame10_2Layout.addWidget(self.splitter9)

        self.splitter8 = QSplitter(self.frame10_2,"splitter8")
        self.splitter8.setOrientation(QSplitter.Horizontal)

        self.textLabel31_2 = QLabel(self.splitter8,"textLabel31_2")
        self.textLabel31_2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.textLabel31_2.sizePolicy().hasHeightForWidth()))
        self.textLabel31_2.setMaximumSize(QSize(140,32767))
        self.textLabel31_2.setPaletteForegroundColor(QColor(240,22,25))
        textLabel31_2_font = QFont(self.textLabel31_2.font())
        textLabel31_2_font.setPointSize(11)
        textLabel31_2_font.setBold(1)
        self.textLabel31_2.setFont(textLabel31_2_font)
        self.textLabel31_2.setFrameShadow(QLabel.Plain)
        self.textLabel31_2.setTextFormat(QLabel.AutoText)
        self.textLabel31_2.setScaledContents(1)
        self.textLabel31_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        self.lineEdit_stepq_2 = QLineEdit(self.splitter8,"lineEdit_stepq_2")
        self.lineEdit_stepq_2.setMaximumSize(QSize(80,23))
        frame10_2Layout.addWidget(self.splitter8)

        self.splitter6 = QSplitter(self.frame10_2,"splitter6")
        self.splitter6.setOrientation(QSplitter.Horizontal)

        self.textLabel32_2 = QLabel(self.splitter6,"textLabel32_2")
        self.textLabel32_2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.textLabel32_2.sizePolicy().hasHeightForWidth()))
        self.textLabel32_2.setMaximumSize(QSize(140,32767))
        self.textLabel32_2.setPaletteForegroundColor(QColor(240,22,25))
        textLabel32_2_font = QFont(self.textLabel32_2.font())
        textLabel32_2_font.setPointSize(11)
        textLabel32_2_font.setBold(1)
        self.textLabel32_2.setFont(textLabel32_2_font)
        self.textLabel32_2.setFrameShadow(QLabel.Plain)
        self.textLabel32_2.setTextFormat(QLabel.AutoText)
        self.textLabel32_2.setScaledContents(1)
        self.textLabel32_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        self.lineEdit_nq_2 = QLineEdit(self.splitter6,"lineEdit_nq_2")
        self.lineEdit_nq_2.setMaximumSize(QSize(80,23))
        frame10_2Layout.addWidget(self.splitter6)

        self.splitter16_2 = QSplitter(self.frame10_2,"splitter16_2")
        self.splitter16_2.setOrientation(QSplitter.Horizontal)

        self.textLabel_tolerance_2 = QLabel(self.splitter16_2,"textLabel_tolerance_2")
        self.textLabel_tolerance_2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum,0,0,self.textLabel_tolerance_2.sizePolicy().hasHeightForWidth()))
        self.textLabel_tolerance_2.setMaximumSize(QSize(140,32767))
        self.textLabel_tolerance_2.setPaletteForegroundColor(QColor(240,22,25))
        textLabel_tolerance_2_font = QFont(self.textLabel_tolerance_2.font())
        textLabel_tolerance_2_font.setPointSize(11)
        textLabel_tolerance_2_font.setBold(1)
        self.textLabel_tolerance_2.setFont(textLabel_tolerance_2_font)
        self.textLabel_tolerance_2.setFrameShadow(QLabel.Plain)
        self.textLabel_tolerance_2.setTextFormat(QLabel.AutoText)
        self.textLabel_tolerance_2.setScaledContents(1)
        self.textLabel_tolerance_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        self.lineEdit_tolerance_2 = QLineEdit(self.splitter16_2,"lineEdit_tolerance_2")
        self.lineEdit_tolerance_2.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.lineEdit_tolerance_2.sizePolicy().hasHeightForWidth()))
        self.lineEdit_tolerance_2.setMaximumSize(QSize(80,23))
        frame10_2Layout.addWidget(self.splitter16_2)
        layout60_3.addWidget(self.frame10_2)
        layout61_2.addLayout(layout60_3)

        layout59_3 = QGridLayout(None,1,1,0,0,"layout59_3")

        layout44_2 = QGridLayout(None,1,1,0,0,"layout44_2")

        self.matplotlibWidget1 = MatplotlibWidget(self.TabPage,"matplotlibWidget1")
        self.matplotlibWidget1.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,254,0,self.matplotlibWidget1.sizePolicy().hasHeightForWidth()))

        layout44_2.addWidget(self.matplotlibWidget1,0,1)

        self.buttonGroup3 = QButtonGroup(self.TabPage,"buttonGroup3")
        self.buttonGroup3.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.buttonGroup3.sizePolicy().hasHeightForWidth()))
        self.buttonGroup3.setFrameShape(QButtonGroup.NoFrame)
        self.buttonGroup3.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup3.layout().setSpacing(3)
        self.buttonGroup3.layout().setMargin(11)
        buttonGroup3Layout = QVBoxLayout(self.buttonGroup3.layout())
        buttonGroup3Layout.setAlignment(Qt.AlignTop)

        self.pushButtonMakeDark = QPushButton(self.buttonGroup3,"pushButtonMakeDark")
        self.pushButtonMakeDark.setEnabled(0)
        buttonGroup3Layout.addWidget(self.pushButtonMakeDark)

        self.pushButtonDoStaticFast = QPushButton(self.buttonGroup3,"pushButtonDoStaticFast")
        buttonGroup3Layout.addWidget(self.pushButtonDoStaticFast)

        self.pushButtonDoStaticAll = QPushButton(self.buttonGroup3,"pushButtonDoStaticAll")
        buttonGroup3Layout.addWidget(self.pushButtonDoStaticAll)

        self.pushButtonMakeMask = QPushButton(self.buttonGroup3,"pushButtonMakeMask")
        buttonGroup3Layout.addWidget(self.pushButtonMakeMask)

        self.pushButton_makeQs = QPushButton(self.buttonGroup3,"pushButton_makeQs")
        buttonGroup3Layout.addWidget(self.pushButton_makeQs)

        self.pushButton10_2 = QPushButton(self.buttonGroup3,"pushButton10_2")
        self.pushButton10_2.setPaletteBackgroundColor(QColor(107,214,0))
        buttonGroup3Layout.addWidget(self.pushButton10_2)

        self.pushButton16 = QPushButton(self.buttonGroup3,"pushButton16")
        self.pushButton16.setEnabled(1)
        self.pushButton16.setPaletteBackgroundColor(QColor(255,0,0))
        buttonGroup3Layout.addWidget(self.pushButton16)

        layout44_2.addWidget(self.buttonGroup3,0,0)

        layout59_3.addLayout(layout44_2,1,0)

        layout58 = QHBoxLayout(None,0,21,"layout58")

        self.buttonGroup4 = QButtonGroup(self.TabPage,"buttonGroup4")
        self.buttonGroup4.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.buttonGroup4.sizePolicy().hasHeightForWidth()))

        self.pushButtonDark = QPushButton(self.buttonGroup4,"pushButtonDark")
        self.pushButtonDark.setEnabled(0)
        self.pushButtonDark.setGeometry(QRect(11,11,82,42))

        self.pushButtonRaw = QPushButton(self.buttonGroup4,"pushButtonRaw")
        self.pushButtonRaw.setEnabled(0)
        self.pushButtonRaw.setGeometry(QRect(96,11,82,42))

        self.pushButtonUnmasked = QPushButton(self.buttonGroup4,"pushButtonUnmasked")
        self.pushButtonUnmasked.setGeometry(QRect(181,11,104,42))

        self.pushButtonMasked = QPushButton(self.buttonGroup4,"pushButtonMasked")
        self.pushButtonMasked.setGeometry(QRect(288,11,91,42))

        self.pushButton_showQs = QPushButton(self.buttonGroup4,"pushButton_showQs")
        self.pushButton_showQs.setGeometry(QRect(382,11,82,42))

        self.pushButton_ShowIq = QPushButton(self.buttonGroup4,"pushButton_ShowIq")
        self.pushButton_ShowIq.setGeometry(QRect(467,11,82,42))
        layout58.addWidget(self.buttonGroup4)

        self.checkBox_zoom = QCheckBox(self.TabPage,"checkBox_zoom")
        self.checkBox_zoom.setMaximumSize(QSize(80,32767))
        layout58.addWidget(self.checkBox_zoom)

        layout59_3.addLayout(layout58,0,0)
        layout61_2.addLayout(layout59_3)

        TabPageLayout.addLayout(layout61_2,0,0)
        self.tabWidget1.insertTab(self.TabPage,QString.fromLatin1(""))

        self.TabPage_2 = QWidget(self.tabWidget1,"TabPage_2")
        TabPageLayout_2 = QGridLayout(self.TabPage_2,1,1,11,21,"TabPageLayout_2")

        layout64 = QVBoxLayout(None,0,0,"layout64")

        layout43_2 = QHBoxLayout(None,0,21,"layout43_2")

        layout11 = QHBoxLayout(None,0,21,"layout11")

        self.cf_label = QLabel(self.TabPage_2,"cf_label")
        self.cf_label.setPaletteForegroundColor(QColor(0,0,255))
        cf_label_font = QFont(self.cf_label.font())
        cf_label_font.setBold(1)
        self.cf_label.setFont(cf_label_font)
        layout11.addWidget(self.cf_label)

        self.lineEdit_cf = QLineEdit(self.TabPage_2,"lineEdit_cf")
        self.lineEdit_cf.setEnabled(1)
        self.lineEdit_cf.setMinimumSize(QSize(400,0))
        layout11.addWidget(self.lineEdit_cf)
        layout43_2.addLayout(layout11)

        self.splitter5 = QSplitter(self.TabPage_2,"splitter5")
        self.splitter5.setOrientation(QSplitter.Horizontal)

        self.Staticdata_label_2 = QLabel(self.splitter5,"Staticdata_label_2")
        self.Staticdata_label_2.setMaximumSize(QSize(80,32767))
        self.Staticdata_label_2.setPaletteForegroundColor(QColor(0,0,255))
        Staticdata_label_2_font = QFont(self.Staticdata_label_2.font())
        Staticdata_label_2_font.setBold(1)
        self.Staticdata_label_2.setFont(Staticdata_label_2_font)
        self.Staticdata_label_2.setIndent(-1)

        self.lineEdit_plotq = QLineEdit(self.splitter5,"lineEdit_plotq")
        self.lineEdit_plotq.setMinimumSize(QSize(20,0))
        self.lineEdit_plotq.setMaximumSize(QSize(35,32767))
        layout43_2.addWidget(self.splitter5)

        self.pushButton_cf_del = QPushButton(self.TabPage_2,"pushButton_cf_del")
        layout43_2.addWidget(self.pushButton_cf_del)

        self.pushButton_del_cf = QPushButton(self.TabPage_2,"pushButton_del_cf")
        layout43_2.addWidget(self.pushButton_del_cf)
        layout64.addLayout(layout43_2)

        layout63_2 = QHBoxLayout(None,0,0,"layout63_2")

        self.matplotlibWidget_cf = MatplotlibWidget(self.TabPage_2,"matplotlibWidget_cf")
        self.matplotlibWidget_cf.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,254,0,self.matplotlibWidget_cf.sizePolicy().hasHeightForWidth()))
        layout63_2.addWidget(self.matplotlibWidget_cf)

        layout62_2 = QVBoxLayout(None,0,21,"layout62_2")
        spacer3_2 = QSpacerItem(20,221,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout62_2.addItem(spacer3_2)

        self.pushButton23 = QPushButton(self.TabPage_2,"pushButton23")
        layout62_2.addWidget(self.pushButton23)

        self.checkBox_hold = QCheckBox(self.TabPage_2,"checkBox_hold")
        self.checkBox_hold.setMaximumSize(QSize(50,32767))
        self.checkBox_hold.setChecked(1)
        layout62_2.addWidget(self.checkBox_hold)
        spacer3_2_2 = QSpacerItem(20,221,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout62_2.addItem(spacer3_2_2)
        layout63_2.addLayout(layout62_2)
        layout64.addLayout(layout63_2)

        TabPageLayout_2.addLayout(layout64,0,0)
        self.tabWidget1.insertTab(self.TabPage_2,QString.fromLatin1(""))

        self.TabPage_3 = QWidget(self.tabWidget1,"TabPage_3")
        TabPageLayout_3 = QGridLayout(self.TabPage_3,1,1,11,21,"TabPageLayout_3")

        layout67 = QVBoxLayout(None,0,0,"layout67")

        layout66_2 = QHBoxLayout(None,0,21,"layout66_2")

        self.splitter17 = QSplitter(self.TabPage_3,"splitter17")
        self.splitter17.setOrientation(QSplitter.Horizontal)

        self.cf_label_TRcf = QLabel(self.splitter17,"cf_label_TRcf")
        self.cf_label_TRcf.setMaximumSize(QSize(200,32767))
        self.cf_label_TRcf.setPaletteForegroundColor(QColor(0,0,255))
        cf_label_TRcf_font = QFont(self.cf_label_TRcf.font())
        cf_label_TRcf_font.setBold(1)
        self.cf_label_TRcf.setFont(cf_label_TRcf_font)

        self.lineEdit_TRcf = QLineEdit(self.splitter17,"lineEdit_TRcf")
        self.lineEdit_TRcf.setEnabled(1)
        self.lineEdit_TRcf.setMinimumSize(QSize(400,0))
        layout66_2.addWidget(self.splitter17)

        self.splitter16_3 = QSplitter(self.TabPage_3,"splitter16_3")
        self.splitter16_3.setOrientation(QSplitter.Horizontal)

        self.q_label = QLabel(self.splitter16_3,"q_label")
        self.q_label.setMaximumSize(QSize(80,32767))
        self.q_label.setPaletteForegroundColor(QColor(0,0,255))
        q_label_font = QFont(self.q_label.font())
        q_label_font.setBold(1)
        self.q_label.setFont(q_label_font)

        self.lineEdit_plotq_TRcf = QLineEdit(self.splitter16_3,"lineEdit_plotq_TRcf")
        self.lineEdit_plotq_TRcf.setMaximumSize(QSize(35,3267))
        layout66_2.addWidget(self.splitter16_3)

        self.pushButton_TRcf_plot = QPushButton(self.TabPage_3,"pushButton_TRcf_plot")
        layout66_2.addWidget(self.pushButton_TRcf_plot)

        self.pushButton_TRcf_calc = QPushButton(self.TabPage_3,"pushButton_TRcf_calc")
        self.pushButton_TRcf_calc.setEnabled(0)
        layout66_2.addWidget(self.pushButton_TRcf_calc)
        layout67.addLayout(layout66_2)

        layout42_2 = QHBoxLayout(None,0,0,"layout42_2")

        self.matplotlibWidget_TRC = MatplotlibWidget(self.TabPage_3,"matplotlibWidget_TRC")
        self.matplotlibWidget_TRC.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,254,0,self.matplotlibWidget_TRC.sizePolicy().hasHeightForWidth()))
        layout42_2.addWidget(self.matplotlibWidget_TRC)

        layout41 = QVBoxLayout(None,0,21,"layout41")

        self.groupBox1 = QGroupBox(self.TabPage_3,"groupBox1")
        self.groupBox1.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed,0,0,self.groupBox1.sizePolicy().hasHeightForWidth()))
        self.groupBox1.setFrameShadow(QGroupBox.Raised)
        self.groupBox1.setAlignment(QGroupBox.AlignCenter)
        self.groupBox1.setColumnLayout(0,Qt.Vertical)
        self.groupBox1.layout().setSpacing(21)
        self.groupBox1.layout().setMargin(11)
        groupBox1Layout = QGridLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(Qt.AlignTop)

        layout40 = QGridLayout(None,1,1,0,21,"layout40")

        layout38 = QHBoxLayout(None,0,21,"layout38")

        self.textLabel2 = QLabel(self.groupBox1,"textLabel2")
        layout38.addWidget(self.textLabel2)

        self.lineEdit_zmin = QLineEdit(self.groupBox1,"lineEdit_zmin")
        layout38.addWidget(self.lineEdit_zmin)

        layout40.addLayout(layout38,0,0)

        layout39 = QHBoxLayout(None,0,21,"layout39")

        self.textLabel3_2 = QLabel(self.groupBox1,"textLabel3_2")
        layout39.addWidget(self.textLabel3_2)

        self.lineEdit_zmax = QLineEdit(self.groupBox1,"lineEdit_zmax")
        layout39.addWidget(self.lineEdit_zmax)

        layout40.addLayout(layout39,1,0)

        groupBox1Layout.addLayout(layout40,0,0)
        layout41.addWidget(self.groupBox1)
        spacer2 = QSpacerItem(20,330,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout41.addItem(spacer2)
        layout42_2.addLayout(layout41)
        layout67.addLayout(layout42_2)

        TabPageLayout_3.addLayout(layout67,0,0)
        self.tabWidget1.insertTab(self.TabPage_3,QString.fromLatin1(""))

        self.TabPage_4 = QWidget(self.tabWidget1,"TabPage_4")
        TabPageLayout_4 = QGridLayout(self.TabPage_4,1,1,11,21,"TabPageLayout_4")

        layout70 = QVBoxLayout(None,0,0,"layout70")

        self.splitter20 = QSplitter(self.TabPage_4,"splitter20")
        self.splitter20.setMinimumSize(QSize(763,29))
        self.splitter20.setMaximumSize(QSize(32767,29))
        self.splitter20.setOrientation(QSplitter.Horizontal)

        self.splitter19 = QSplitter(self.splitter20,"splitter19")
        self.splitter19.setOrientation(QSplitter.Horizontal)

        self.cf_label_TRcf_2 = QLabel(self.splitter19,"cf_label_TRcf_2")
        self.cf_label_TRcf_2.setEnabled(1)
        self.cf_label_TRcf_2.setMaximumSize(QSize(100,23))
        self.cf_label_TRcf_2.setPaletteForegroundColor(QColor(0,0,255))
        cf_label_TRcf_2_font = QFont(self.cf_label_TRcf_2.font())
        cf_label_TRcf_2_font.setBold(1)
        self.cf_label_TRcf_2.setFont(cf_label_TRcf_2_font)

        self.lineEdit_chi4_file = QLineEdit(self.splitter19,"lineEdit_chi4_file")
        self.lineEdit_chi4_file.setEnabled(1)
        self.lineEdit_chi4_file.setMinimumSize(QSize(400,0))
        self.lineEdit_chi4_file.setMaximumSize(QSize(32767,23))

        self.splitter18 = QSplitter(self.splitter20,"splitter18")
        self.splitter18.setOrientation(QSplitter.Horizontal)

        self.q_label_chi4 = QLabel(self.splitter18,"q_label_chi4")
        self.q_label_chi4.setEnabled(1)
        self.q_label_chi4.setMaximumSize(QSize(80,23))
        self.q_label_chi4.setPaletteForegroundColor(QColor(0,0,255))
        q_label_chi4_font = QFont(self.q_label_chi4.font())
        q_label_chi4_font.setBold(1)
        self.q_label_chi4.setFont(q_label_chi4_font)

        self.q_lineEdit_chi4 = QLineEdit(self.splitter18,"q_lineEdit_chi4")
        self.q_lineEdit_chi4.setEnabled(1)
        self.q_lineEdit_chi4.setMaximumSize(QSize(3267,23))

        LayoutWidget = QWidget(self.splitter20,"layout41")
        layout41_2 = QHBoxLayout(LayoutWidget,11,0,"layout41_2")

        self.pushButton_plot_chi4 = QPushButton(LayoutWidget,"pushButton_plot_chi4")
        self.pushButton_plot_chi4.setEnabled(1)
        self.pushButton_plot_chi4.setMaximumSize(QSize(100,32767))
        layout41_2.addWidget(self.pushButton_plot_chi4)

        self.pushButton_chi4 = QPushButton(LayoutWidget,"pushButton_chi4")
        self.pushButton_chi4.setEnabled(1)
        self.pushButton_chi4.setMaximumSize(QSize(100,32767))
        layout41_2.addWidget(self.pushButton_chi4)
        layout70.addWidget(self.splitter20)

        layout68 = QHBoxLayout(None,0,0,"layout68")

        self.matplotlibWidget_chi4 = MatplotlibWidget(self.TabPage_4,"matplotlibWidget_chi4")
        self.matplotlibWidget_chi4.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,254,0,self.matplotlibWidget_chi4.sizePolicy().hasHeightForWidth()))
        layout68.addWidget(self.matplotlibWidget_chi4)

        self.checkBox_hold_chi4 = QCheckBox(self.TabPage_4,"checkBox_hold_chi4")
        self.checkBox_hold_chi4.setMaximumSize(QSize(50,32767))
        self.checkBox_hold_chi4.setChecked(1)
        layout68.addWidget(self.checkBox_hold_chi4)
        layout70.addLayout(layout68)

        TabPageLayout_4.addLayout(layout70,0,0)
        self.tabWidget1.insertTab(self.TabPage_4,QString.fromLatin1(""))

        Form1Layout.addWidget(self.tabWidget1,0,0)

        self.languageChange()

        self.resize(QSize(1372,683).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.checkBox_darks,SIGNAL("toggled(bool)"),self.pushButtonMakeDark.setEnabled)
        self.connect(self.checkBox_darks,SIGNAL("toggled(bool)"),self.pushButtonRaw.setEnabled)
        self.connect(self.checkBox_darks,SIGNAL("toggled(bool)"),self.pushButtonDark.setEnabled)
        self.connect(self.checkBox_darks,SIGNAL("toggled(bool)"),self.frame2.setEnabled)
        self.connect(self.checkBox_droplet,SIGNAL("toggled(bool)"),self.groupBox3.setEnabled)
        self.connect(self.checkBox_flatfield,SIGNAL("toggled(bool)"),self.comboBox_flatfield.setEnabled)
        self.connect(self.comboBox_detector,SIGNAL("activated(int)"),self.activate_flatfield)
        self.connect(self.comboBox_detector,SIGNAL("activated(int)"),self.SetNormalizeList)
        self.connect(self.comboBox_flatfield,SIGNAL("activated(int)"),self.activateLoad)
        self.connect(self.lineEdit27,SIGNAL("textChanged(const QString&)"),self.lineEdit_deltaq_2.setText)
        self.connect(self.lineEdit28,SIGNAL("textChanged(const QString&)"),self.lineEdit_stepq_2.setText)
        self.connect(self.lineEdit_deltaq_2,SIGNAL("textChanged(const QString&)"),self.lineEdit27.setText)
        self.connect(self.lineEdit_firstq,SIGNAL("textChanged(const QString&)"),self.lineEdit_firstq_2.setText)
        self.connect(self.lineEdit_firstq_2,SIGNAL("textChanged(const QString&)"),self.lineEdit_firstq.setText)
        self.connect(self.lineEdit_nq,SIGNAL("textChanged(const QString&)"),self.lineEdit_nq_2.setText)
        self.connect(self.lineEdit_nq_2,SIGNAL("textChanged(const QString&)"),self.lineEdit_nq.setText)
        self.connect(self.lineEdit_stepq_2,SIGNAL("textChanged(const QString&)"),self.lineEdit28.setText)
        self.connect(self.lineEdit_tolerance,SIGNAL("textChanged(const QString&)"),self.lineEdit_tolerance_2.setText)
        self.connect(self.lineEdit_tolerance_2,SIGNAL("returnPressed()"),self.pushButtonMasked.animateClick)
        self.connect(self.lineEdit_tolerance_2,SIGNAL("textChanged(const QString&)"),self.lineEdit_tolerance.setText)
        self.connect(self.pushButton1,SIGNAL("clicked()"),self.loadinput)
        self.connect(self.pushButton10,SIGNAL("pressed()"),self.correlator)
        self.connect(self.pushButton10_2,SIGNAL("pressed()"),self.correlator)
        self.connect(self.pushButton16,SIGNAL("pressed()"),self.stop_correlator)
        self.connect(self.pushButton2,SIGNAL("pressed()"),self.makeinput)
        self.connect(self.pushButton23,SIGNAL("pressed()"),self.fit)
        self.connect(self.pushButton_cf_del,SIGNAL("pressed()"),self.plot_cf)
        self.connect(self.pushButton_chi4,SIGNAL("pressed()"),self.chi4)
        self.connect(self.pushButtonDark,SIGNAL("pressed()"),self.plot_dark)
        self.connect(self.pushButton_del_cf,SIGNAL("pressed()"),self.del_cf)
        self.connect(self.pushButtonDoStaticAll,SIGNAL("pressed()"),self.dostatic_all)
        self.connect(self.pushButtonDoStaticFast,SIGNAL("pressed()"),self.dostatic_quick)
        self.connect(self.pushButtonMakeDark,SIGNAL("pressed()"),self.dodarks)
        self.connect(self.pushButtonMakeMask,SIGNAL("pressed()"),self.user_mask)
        self.connect(self.pushButton_makeQs,SIGNAL("pressed()"),self.Qs)
        self.connect(self.pushButtonMasked,SIGNAL("pressed()"),self.plot_masked)
        self.connect(self.pushButton_plot_chi4,SIGNAL("pressed()"),self.plot_chi4)
        self.connect(self.pushButtonRaw,SIGNAL("pressed()"),self.plot_raw)
        self.connect(self.pushButton_ShowIq,SIGNAL("pressed()"),self.Iq)
        self.connect(self.pushButton_showQs,SIGNAL("pressed()"),self.plotQmask)
        self.connect(self.pushButton_TRcf_calc,SIGNAL("pressed()"),self.calc_TRCF)
        self.connect(self.pushButton_TRcf_plot,SIGNAL("pressed()"),self.plot_TRcf)
        self.connect(self.pushButtonUnmasked,SIGNAL("pressed()"),self.plot_unmasked)
        self.connect(self.radioButton3,SIGNAL("toggled(bool)"),self.lineEdit20.setDisabled)
        self.connect(self.radioButton3,SIGNAL("toggled(bool)"),self.textLabel22.setDisabled)
        self.connect(self.radioButton3,SIGNAL("toggled(bool)"),self.groupBox3.setDisabled)
        self.connect(self.radioButton3,SIGNAL("toggled(bool)"),self.change_labelsback)
        self.connect(self.radioButton3,SIGNAL("toggled(bool)"),self.change_labelsbeamback)
        self.connect(self.radioButton4,SIGNAL("toggled(bool)"),self.groupBox3.setDisabled)
        self.connect(self.radioButton4,SIGNAL("toggled(bool)"),self.change_labelsback)
        self.connect(self.radioButton4,SIGNAL("toggled(bool)"),self.change_labelsbeam)
        self.connect(self.radioButton5,SIGNAL("toggled(bool)"),self.lineEdit20.setDisabled)
        self.connect(self.radioButton5,SIGNAL("toggled(bool)"),self.textLabel22.setDisabled)
        self.connect(self.radioButton5,SIGNAL("toggled(bool)"),self.checkBox_droplet.setEnabled)
        self.connect(self.radioButton5,SIGNAL("toggled(bool)"),self.change_labelsbeamback)
        self.connect(self.tabWidget1,SIGNAL("currentChanged(QWidget*)"),self.update_text)
        self.connect(self.tabWidget1,SIGNAL("currentChanged(QWidget*)"),self.update_text)
        self.connect(self.toolButton_DarkDir,SIGNAL("clicked()"),self.LoadDarkDir)
        self.connect(self.toolButtonDarkFile,SIGNAL("clicked()"),self.LoadDarkFile)
        self.connect(self.toolButton_DataDir,SIGNAL("clicked()"),self.LoadDataDir)
        self.connect(self.toolButtonMaskFile,SIGNAL("clicked()"),self.LoadMaskFile)
        self.connect(self.toolButton_outdir,SIGNAL("clicked()"),self.LoadOutDir)
#        self.connect(self.pushButton_TRcf_calc,SIGNAL("stateChanged(int)"),self.dostatic)


    def languageChange(self):
        self.setCaption(self.__tr("XPCS GUI version 1.1.2"))
        self.textLabel1.setText(self.__tr("Input file:"))
        self.lineEdit_input.setText(self.__tr("./input.txt"))
        self.pushButton1.setText(self.__tr("&LOAD"))
        self.pushButton1.setAccel(QKeySequence(self.__tr("Alt+L")))
        self.pushButton2.setText(self.__tr("&SAVE"))
        self.pushButton2.setAccel(QKeySequence(self.__tr("Alt+S")))
        self.pushButton10.setText(self.__tr("START\n"
"Correlator"))
        self.pushButton10.setAccel(QKeySequence(QString.null))
        self.checkBox_plot.setText(self.__tr("plot online"))
        self.checkBox_multiproc.setText(self.__tr("multiprocessor"))
        self.textLabel4.setText(self.__tr("data prefix:"))
        self.lineEditDataPrefix.setText(self.__tr("example_0001_"))
        self.textLabel5.setText(self.__tr("data suffix:"))
        self.lineEditDataSuff.setText(self.__tr(".edf"))
        self.textLabel6.setText(self.__tr("n first image:"))
        self.lineEditDataStart.setText(self.__tr("1"))
        self.textLabel7.setText(self.__tr("n last image:"))
        self.lineEditDataEnd.setText(self.__tr("1000"))
        self.textLabel3.setText(self.__tr("data directory:"))
        self.lineEditDataDir.setText(self.__tr("/data/opid10/external/your_dir.../"))
        self.toolButton_DataDir.setText(self.__tr("..."))
        self.checkBox_darks.setText(self.__tr("use darks"))
        self.textLabel8.setText(self.__tr("darks directory:"))
        self.lineEditDarkDir.setText(self.__tr("/data/opid10/external/your_dir.../"))
        self.toolButton_DarkDir.setText(self.__tr("..."))
        self.textLabel10.setText(self.__tr("n first dark:"))
        self.lineEditDarkStart.setText(self.__tr("1"))
        self.textLabel11.setText(self.__tr("n last dark:"))
        self.lineEditDarkEnd.setText(self.__tr("100"))
        self.textLabel9.setText(self.__tr("darks prefix:"))
        self.lineEditDarkPrefix.setText(self.__tr("example_0002_"))
        self.buttonGroup1.setTitle(self.__tr("Detector"))
        self.comboBox_detector.clear()
        self.comboBox_detector.insertItem(self.__tr("Medipix"))
        self.comboBox_detector.insertItem(self.__tr("Princeton"))
        self.comboBox_detector.insertItem(self.__tr("Andor 22.5micron"))
        self.comboBox_detector.insertItem(self.__tr("Andor 13micron"))
        self.comboBox_detector.setCurrentItem(0)
        self.checkBox_flatfield.setText(self.__tr("flatfield"))
        QToolTip.add(self.checkBox_flatfield,self.__tr("only used for  medipix"))
        self.comboBox_flatfield.clear()
        self.comboBox_flatfield.insertItem(self.__tr("8keV"))
        self.comboBox_flatfield.insertItem(self.__tr("8keV before april 2009"))
        self.comboBox_flatfield.insertItem(self.__tr("10keV"))
        self.comboBox_flatfield.insertItem(self.__tr("other"))
        self.buttonGroup2.setTitle(self.__tr("Scattering geometry"))
        self.radioButton3.setText(self.__tr("&SAXS"))
        self.radioButton3.setAccel(QKeySequence(self.__tr("Alt+S")))
        self.radioButton4.setText(self.__tr("&GISAXS"))
        self.radioButton4.setAccel(QKeySequence(self.__tr("Alt+G")))
        self.radioButton5.setText(self.__tr("WAXS"))
        self.radioButton5.setAccel(QKeySequence(QString.null))
        self.groupBox4.setTitle(QString.null)
        self.checkBox_droplet.setText(self.__tr("dropletize"))
        self.groupBox3.setTitle(QString.null)
        self.textLabel_photonadu_2.setText(self.__tr("0 photon adu:"))
        self.lineEdit_0PhotADU.setText(self.__tr("0"))
        self.textLabel_sigmaphoton_2.setText(self.__tr("+/-"))
        self.lineEdit_0PhotSigma.setText(self.__tr("200"))
        self.textLabel_photonadu.setText(self.__tr("1photon ADU:"))
        self.lineEdit_1PhotADU.setText(self.__tr("1930"))
        self.textLabel_sigmaphoton.setText(self.__tr("+/-"))
        self.lineEdit_1PhotSigma.setText(self.__tr("100"))
        self.textLabel12.setText(self.__tr("output directory:"))
        self.lineEdit12.setText(self.__tr("/data/opid10/external/your_dir.../analysis../"))
        self.toolButton_outdir.setText(self.__tr("..."))
        self.textLabel13.setText(self.__tr("output files prefix:"))
        self.lineEdit13.setText(self.__tr("sample1_"))
        self.textLabel15.setText(self.__tr("detecor-sample distance (mm):"))
        self.lineEdit_dsd.setText(self.__tr("2100"))
        self.textLabel16.setText(self.__tr("wavelength (1/Ang):"))
        self.lineEdit_lambda.setText(self.__tr("1.55"))
        self.textLabel17.setText(self.__tr("time between images (sec):"))
        self.lineEdit17.setText(self.__tr("auto"))
        self.textLabel19.setText(self.__tr("X direct beam:"))
        self.lineEdit18.setText(self.__tr("1"))
        self.textLabel20.setText(self.__tr("Y direct beam:"))
        self.lineEdit19.setText(self.__tr("30"))
        self.textLabel22.setText(self.__tr("incidence angle (deg):"))
        self.lineEdit20.setText(self.__tr("0.1"))
        self.groupBox2.setTitle(self.__tr("Normalization"))
        self.comboBox_normalize.clear()
        self.comboBox_normalize.insertItem(self.__tr("None"))
        self.comboBox_normalize.insertItem(self.__tr("Average in CCD"))
        self.textLabel_qTRC.setText(self.__tr("q for TRC (no.):"))
        self.lineEdit_qTRC.setText(self.__tr("2"))
        self.textLabel28.setText(self.__tr("tolerance:"))
        self.lineEdit_tolerance.setText(self.__tr("0"))
        QToolTip.add(self.lineEdit_tolerance,self.__tr("This defines a treshold: from princeton detector, all pixels with less than this value will be set to zero. For medipix, all pixels of the dark with more than this value will be masked. Put 0 if you don't want auto mask"))
        QWhatsThis.add(self.lineEdit_tolerance,self.__tr("This defines a treshold: from princeton detector, all pixels with less than this value will be set to zero. For medipix, all pixels of the dark with more than this value will be masked. Put 0 if you don't want auto mask"))
        self.textLabel29.setText(self.__tr("first q (1/Ang):"))
        self.lineEdit_firstq.setText(self.__tr("0"))
        self.textLabel31.setText(self.__tr("step q (1/Ang):"))
        self.lineEdit28.setText(self.__tr("2e-4"))
        self.textLabel32.setText(self.__tr("no. of q:"))
        self.lineEdit_nq.setText(self.__tr("50"))
        self.textLabel30.setText(self.__tr("delta q (1/Ang):"))
        self.lineEdit27.setText(self.__tr("2e-4"))
        self.tabWidget1.changeTab(self.tab,self.__tr("Edit Input"))
        self.Staticdata_label.setText(self.__tr("static data file:"))
        QWhatsThis.add(self.lineEdit_data,self.__tr("If this file exist, it will be loaded, otherwise when you create the mask, it will be saved with this name. (it is the output directory+the output_file_prefix+ '_mask.edf' as given in the Edit Input tab"))
        self.mask_label.setText(self.__tr("mask file:"))
        self.lineEdit_mask.setText(self.__tr("default"))
        QWhatsThis.add(self.lineEdit_mask,self.__tr("If this file exist, it will be loaded, otherwise when you create the mask, it will be saved with this name. (it is the output directory+the output_file_prefix+ '_mask.edf' as given in the Edit Input tab"))
        self.toolButtonMaskFile.setText(self.__tr("..."))
        self.dark_label.setText(self.__tr("dark file:"))
        self.lineEdit_dark.setText(self.__tr("default"))
        QWhatsThis.add(self.lineEdit_dark,self.__tr("If this file exist, it will be loaded, otherwise when you create the mask, it will be saved with this name. (it is the output directory+the output_file_prefix+ '_mask.edf' as given in the Edit Input tab"))
        self.toolButtonDarkFile.setText(self.__tr("..."))
        self.qmask_label.setText(self.__tr("qmask file:"))
        QWhatsThis.add(self.lineEdit_qmask,self.__tr("If this file exist, it will be loaded, otherwise when you create the mask, it will be saved with this name. (it is the output directory+the output_file_prefix+ '_mask.edf' as given in the Edit Input tab"))
        self.textLabel29_2.setText(self.__tr("first q (1/Ang):"))
        self.lineEdit_firstq_2.setText(self.__tr("0"))
        self.textLabel30_2.setText(self.__tr("delta q (1/Ang):"))
        self.lineEdit_deltaq_2.setText(self.__tr("2e-4"))
        self.textLabel31_2.setText(self.__tr("step q (1/Ang):"))
        self.lineEdit_stepq_2.setText(self.__tr("2e-4"))
        self.textLabel32_2.setText(self.__tr("no. of q:"))
        self.lineEdit_nq_2.setText(self.__tr("50"))
        self.textLabel_tolerance_2.setText(self.__tr("tolerance:"))
        self.lineEdit_tolerance_2.setText(self.__tr("0"))
        QToolTip.add(self.lineEdit_tolerance_2,self.__tr("This defines a treshold: from princeton detector, all pixels with less than this value will be set to zero. For medipix, all pixels of the dark with more than this value will be masked. Put 0 if you don't want auto mask"))
        QWhatsThis.add(self.lineEdit_tolerance_2,self.__tr("This defines a treshold: from princeton detector, all pixels with less than this value will be set to zero. For medipix, all pixels of the dark with more than this value will be masked. Put 0 if you don't want auto mask"))
        self.buttonGroup3.setTitle(QString.null)
        self.pushButtonMakeDark.setText(self.__tr("Make Dark"))
        self.pushButtonDoStaticFast.setText(self.__tr("Make Quick\n"
"Static"))
        QToolTip.add(self.pushButtonDoStaticFast,self.__tr("Average first 20 images"))
        self.pushButtonDoStaticAll.setText(self.__tr("Make All\n"
"Static"))
        QToolTip.add(self.pushButtonDoStaticAll,self.__tr("average all images"))
        self.pushButtonMakeMask.setText(self.__tr("Make Mask"))
        self.pushButton_makeQs.setText(self.__tr("Make \n"
"Qs"))
        self.pushButton10_2.setText(self.__tr("Start \n"
"Correlator"))
        self.pushButton10_2.setAccel(QKeySequence(QString.null))
        self.pushButton16.setText(self.__tr("Stop \n"
"Correlator"))
        self.buttonGroup4.setTitle(QString.null)
        self.pushButtonDark.setText(self.__tr("Show \n"
"Dark"))
        self.pushButtonRaw.setText(self.__tr("Show \n"
"raw data"))
        self.pushButtonUnmasked.setText(self.__tr("Show Unmasked\n"
"Data"))
        self.pushButtonMasked.setText(self.__tr("Show Masked\n"
"Data"))
        self.pushButton_showQs.setText(self.__tr("Show \n"
"Qs"))
        self.pushButton_ShowIq.setText(self.__tr("Show\n"
"I(q)"))
        self.checkBox_zoom.setText(self.__tr("fix zoom"))
        self.tabWidget1.changeTab(self.TabPage,self.__tr("Correlator"))
        self.cf_label.setText(self.__tr("correlation functions file:"))
        QWhatsThis.add(self.lineEdit_cf,self.__tr("If this file exist, it will be loaded, otherwise when you create the mask, it will be saved with this name. (it is the output directory+the output_file_prefix+ '_mask.edf' as given in the Edit Input tab"))
        self.Staticdata_label_2.setText(self.__tr("q number:"))
        self.lineEdit_plotq.setText(self.__tr("all"))
        self.pushButton_cf_del.setText(self.__tr("PLOT"))
        self.pushButton_del_cf.setText(self.__tr("REMOVE"))
        self.pushButton23.setText(self.__tr("Start\n"
"Fitting"))
        self.checkBox_hold.setText(self.__tr("Hold"))
        self.tabWidget1.changeTab(self.TabPage_2,self.__tr("Correlation Functions"))
        self.cf_label_TRcf.setText(self.__tr("TR correlation functions file:"))
        QWhatsThis.add(self.lineEdit_TRcf,self.__tr("If this file exist, it will be loaded, otherwise when you create the mask, it will be saved with this name. (it is the output directory+the output_file_prefix+ '_mask.edf' as given in the Edit Input tab"))
        self.q_label.setText(self.__tr("q number:"))
        self.lineEdit_plotq_TRcf.setText(self.__tr("2"))
        self.pushButton_TRcf_plot.setText(self.__tr("PLOT"))
        self.pushButton_TRcf_calc.setText(self.__tr("CALCULATE"))
        self.groupBox1.setTitle(self.__tr("Z SCALE"))
        self.textLabel2.setText(self.__tr("Z min:"))
        self.lineEdit_zmin.setText(self.__tr("auto"))
        self.textLabel3_2.setText(self.__tr("Z max:"))
        self.lineEdit_zmax.setText(self.__tr("auto"))
        self.tabWidget1.changeTab(self.TabPage_3,self.__tr("Time Resolved CF"))
        self.cf_label_TRcf_2.setText(self.__tr("Chi 4 file:"))
        QWhatsThis.add(self.lineEdit_chi4_file,self.__tr("If this file exist, it will be loaded, otherwise when you create the mask, it will be saved with this name. (it is the output directory+the output_file_prefix+ '_mask.edf' as given in the Edit Input tab"))
        self.q_label_chi4.setText(self.__tr("q number:"))
        self.q_lineEdit_chi4.setText(self.__tr("2"))
        self.pushButton_plot_chi4.setText(self.__tr("PLOT"))
        self.pushButton_chi4.setText(self.__tr("CALCULATE"))
        self.checkBox_hold_chi4.setText(self.__tr("Hold"))
        self.tabWidget1.changeTab(self.TabPage_4,self.__tr("Chi_4 analysis"))


    def loadinput(self,window=1):
           if window == 1:
              PathLineEdit=self.lineEdit_input.text().ascii()
              filename = QFileDialog.getOpenFileName(PathLineEdit,('*.txt'))
              if filename:
                 self.lineEdit_input.setText(filename)
              else: 
                 filename=self.lineEdit_input.text().ascii()
           else:
              filename=self.lineEdit_input.text().ascii()
           input_info=get_input(filename)
           self.lineEditDataDir.setText(input_info['dir'])
           self.lineEditDataPrefix.setText(input_info['file_prefix'])
           self.lineEditDataSuff.setText(input_info['file_suffix'])
           self.lineEditDataStart.setText(input_info['n_first_image'])
           self.lineEditDataEnd.setText(input_info['n_last_image'])
           if input_info['n_first_dark'].lower()=='none':
              self.checkBox_darks.setChecked(0)
           else:
              self.checkBox_darks.setChecked(1)
              self.lineEditDarkDir.setText(input_info['dark dir'])
              self.lineEditDarkPrefix.setText(input_info['dark_prefix'])
              self.lineEditDarkStart.setText(input_info['n_first_dark'])
              self.lineEditDarkEnd.setText(input_info['n_last_dark'])
           self.lineEdit12.setText(input_info['output directory'])
           self.lineEdit13.setText(input_info['output filename prefix'])
           if input_info['detector'].lower()=='medipix':
              self.comboBox_detector.setCurrentItem(0)
              self.checkBox_flatfield.setEnabled(1)
              try:
                 flat_file=input_info['flatfield file'].lower()
                 if flat_file == 'none' :
                    self.checkBox_flatfield.setChecked(0)
                    self.comboBox_flatfield.setEnabled(0)
                 else:
                    self.checkBox_flatfield.setChecked(1)
                    self.comboBox_flatfield.setEnabled(1) 
                    if flat_file == '8kev' :
                      self.comboBox_flatfield.setCurrentItem(0)
                    elif flat_file == '8kev before april 2009' :
                      self.comboBox_flatfield.setCurrentItem(1)
                    elif flat_file == '10kev' :
                      self.comboBox_flatfield.setCurrentItem(2)
                    else:
                      self.comboBox_flatfield.setCurrentItem(3)
                      self.lineEdit_other.setText(input_info['flatfield file'])
              except:
                    self.checkBox_flatfield.setChecked(1)
                    self.comboBox_flatfield.setCurrentItem(1)
           else:
              self.checkBox_flatfield.setChecked(0)
              self.checkBox_flatfield.setEnabled(0)
              self.comboBox_flatfield.setEnabled(0)
           if input_info['detector'].lower()=='princeton':
              self.comboBox_detector.setCurrentItem(1)
           if input_info['detector'].lower()=='andor 22.5micron':
              self.comboBox_detector.setCurrentItem(2)
           if input_info['detector'].lower()== 'andor 13micron': 
              self.comboBox_detector.setCurrentItem(3)
           if input_info['detector'].lower()=='andor': #andor alone is for old input files
              self.comboBox_detector.setCurrentItem(3)
           self.SetNormalizeList()
           self.lineEdit_dsd.setText(input_info['detector sample distance'])
           self.lineEdit_lambda.setText(input_info['wavelength'])
           self.lineEdit17.setText(input_info['lag time'])
           if input_info['geometry']=='saxs':
              self.radioButton3.setChecked(1)
              self.lineEdit18.setText(input_info['x direct beam'])
              self.lineEdit19.setText(input_info['y direct beam'])
           if input_info['geometry']=='gisaxs':
              self.radioButton4.setChecked(1)
              self.lineEdit18.setText(input_info['x reflected beam'])
              self.lineEdit19.setText(input_info['y reflected beam'])
              self.lineEdit20.setText(input_info['incidence angle'])
           if input_info['geometry']=='waxs':
              self.radioButton5.setChecked(1)
              self.lineEdit18.setText(input_info['x direct beam'])
              self.lineEdit19.setText(input_info['y direct beam'])
              self.checkBox_droplet.setEnabled(1)
              try:
                if input_info['dropletize'].lower()=='yes':
                  self.checkBox_droplet.setChecked(1)
                  self.lineEdit_0PhotADU.setText(input_info['0 Photon ADU'])
                  self.lineEdit_0PhotSigma.setText(input_info['0 Photon Sigma'])
                  self.lineEdit_1PhotADU.setText(input_info['1 Photon ADU'])
                  self.lineEdit_1PhotSigma.setText(input_info['1 Photon Sigma'])
                else:
                  self.checkBox_droplet.setChecked(0)
              except:
                self.checkBox_droplet.setChecked(0)
           self.lineEdit_firstq.setText(input_info['first q'])
           self.lineEdit27.setText(input_info['delta q'])
           self.lineEdit28.setText(input_info['step q'])
           self.lineEdit_nq.setText(input_info['number of q'])
           self.lineEdit_qTRC.setText(input_info['q for TRC'])
           self.lineEdit_plotq_TRcf.setText(input_info['q for TRC'])
           self.q_lineEdit_chi4.setText(input_info['q for TRC'])
           self.lineEdit_tolerance.setText(input_info['tolerance'])
           self.lineEdit_tolerance_2.setText(input_info['tolerance'])
           try:
              self.lineEdit_mask.setText(input_info['mask file'])
              self.lineEdit_dark.setText(input_info['dark file'])
           except:
              self.lineEdit_mask.setText(self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'mask.edf')
              self.lineEdit_dark.setText(self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'dark.edf')
           try:
              normalize=input_info['normalize'].lower()
              if normalize== 'none':
                 self.comboBox_normalize.setCurrentItem(0)  
              if normalize== 'average in ccd':
                 self.comboBox_normalize.setCurrentItem(1)
              if normalize== 'monitor':
                 self.comboBox_normalize.setCurrentItem(2)
           except:
              self.comboBox_normalize.setCurrentItem(0)  
           self.update_text()
           outdir=input_info['output directory']
           print outdir
           if os.path.exists(outdir) is False:
              com='mkdir '+outdir
              print getoutput(com)
              if os.path.exists(outdir) is False:
                 print 'cannot create output directory, please check if there is some error'
              else:
                 print 'created output directory:', outdir
        

    def makeinput(self):  
           filename=self.lineEdit_input.text().ascii()
           self.lineEdit_input.setText(os.path.realpath(filename))
           try:
              f=open(filename,'w')
           except:
              print "wrong directory for the file: ",filename
              return
           dir=os.path.realpath(self.lineEditDataDir.text().ascii())
           if dir[-1]!='/':
              dir=dir+'/'
           f.write('dir = '+ dir+'\n')
           f_prefix=self.lineEditDataPrefix.text().ascii()
           f.write('file_prefix = '+ f_prefix+'\n')
           f_suffix=self.lineEditDataSuff.text().ascii()
           f.write('file_suffix = '+ f_suffix+'\n')
           n_image=self.lineEditDataStart.text().ascii()
           f.write('n_first_image = '+ n_image+'\n')
           n_image=self.lineEditDataEnd.text().ascii()
           f.write('n_last_image = '+ n_image+'\n')
           if self.checkBox_darks.isChecked():
              dark_dir=self.lineEditDarkDir.text().ascii()
              if dark_dir=='':
                 dark_dir=dir
              dark_dir=os.path.realpath(dark_dir)
              if dark_dir[-1]!='/':
                 dark_dir=dark_dir+'/'
              f.write('dark dir = ' +dark_dir +'\n')
              dark_prefix=self.lineEditDarkPrefix.text().ascii()
              f.write('dark_prefix = '+ dark_prefix +'\n')
              dark1=self.lineEditDarkStart.text().ascii()
              f.write('n_first_dark = '+ dark1 + '\n')
              dark2=self.lineEditDarkEnd.text().ascii()
              f.write('n_last_dark = ' + dark2 + '\n')
           else:
              f.write('dark dir = none \n')
              f.write('dark_prefix = none \n')
              f.write('n_first_dark = none \n')
              f.write('n_last_dark = none \n')
           
           outdir=self.lineEdit12.text().ascii()
           if (outdir=='' or outdir=='none'):
              outdir='./'
           else:
              if outdir[-1]!='/':
                 outdir=outdir+'/'
           if os.path.exists(outdir) is False:
              com='mkdir '+outdir
              print getoutput(com)
              if os.path.exists(outdir) is False:
                 print 'cannot create output directory, please check if there is some error'
              else:
                 print 'created output directory:', outdir
                 outdir=os.path.realpath(outdir)
           f.write('output directory = '+ outdir + '\n')
           outprefix=self.lineEdit13.text().ascii()
           f.write('output filename prefix = '+ outprefix + '\n')
           mask_file=self.lineEdit_mask.text().ascii()
           if mask_file=='default':
              mask_file=outdir+outprefix+'mask.edf'
           if mask_file=='':
              mask_file=outdir+outprefix+'mask.edf'  
           self.lineEdit_mask.setText(mask_file)
           f.write('mask file = '+ mask_file + '\n')
           dark_file=self.lineEdit_dark.text().ascii()
           if dark_file=='default':
              dark_file=outdir+outprefix+'dark.edf'
           if dark_file=='':
              dark_file=outdir+outprefix+'dark.edf'
           self.lineEdit_dark.setText(dark_file)
           f.write('dark file = '+ dark_file + '\n')
           detector=self.comboBox_detector.currentText().ascii().lower()
           f.write('detector = ' +detector+ '\n')
           if self.checkBox_flatfield.isChecked():
              flatfield_file=self.comboBox_flatfield.currentText().ascii()
              if flatfield_file=='other':
                 flatfield_file=self.lineEdit_other.text().ascii()
           else:
              flatfield_file='none'
           f.write('flatfield file = '+flatfield_file+'\n')
           dsd=self.lineEdit_dsd.text().ascii()
           f.write('detector sample distance = '+dsd+'\n')
           lam=self.lineEdit_lambda.text().ascii()
           f.write('wavelength = '+lam+'\n')
           dt=self.lineEdit17.text().ascii()
           if dt=='':
              dt='auto'
           f.write('lag time = '+dt+'\n')
           if self.radioButton3.isChecked():
              f.write('geometry = saxs \n')
              xbeam=self.lineEdit18.text().ascii()
              ybeam=self.lineEdit19.text().ascii()
              f.write('x direct beam = ' +xbeam+'\n')
              f.write('y direct beam = ' +ybeam+'\n')
           if self.radioButton4.isChecked():
              f.write('geometry = gisaxs \n')
              xbeam=self.lineEdit18.text().ascii()
              ybeam=self.lineEdit19.text().ascii()
              f.write('x reflected beam = '+ xbeam+'\n')
              f.write('y reflected beam = ' + ybeam+'\n')
              angle=self.lineEdit20.text().ascii()
              f.write('incidence angle = '+ angle+'\n')
           if self.radioButton5.isChecked():
              f.write('geometry = waxs \n')
              xbeam=self.lineEdit18.text().ascii()
              ybeam=self.lineEdit19.text().ascii()
           if self.checkBox_droplet.isChecked():
              f.write('dropletize = yes \n')
              ZerophotADU=self.lineEdit_0PhotADU.text().ascii()
              ZerophotSigma=self.lineEdit_0PhotSigma.text().ascii()
              OnephotADU=self.lineEdit_1PhotADU.text().ascii()
              OnephotSigma=self.lineEdit_1PhotSigma.text().ascii()
           else:
              f.write('dropletize = no \n')
              ZerophotADU='none'
              ZerophotSigma='none'
              OnephotADU='none'
              OnephotSigma='none'
           f.write('0 Photon ADU = ' +ZerophotADU+'\n')
           f.write('0 Photon Sigma = ' +ZerophotSigma+'\n')
           f.write('1 Photon ADU = ' +OnephotADU+'\n')
           f.write('1 Photon Sigma = ' +OnephotSigma+'\n')
           f.write('x direct beam = ' +xbeam+'\n')
           f.write('y direct beam = ' +ybeam+'\n')
           normalize=self.comboBox_normalize.currentText().ascii().lower()
           f.write('normalize = ' +normalize+'\n')
           darkstatus=self.checkBox_darks.isChecked()
           tol=float(self.lineEdit_tolerance.text().ascii())
           if (detector=='medipix')&(darkstatus is False)&(tol>0):
             self.lineEdit_tolerance.setText('0')
             self.lineEdit_tolerance_2.setText('0')
           tol=self.lineEdit_tolerance.text().ascii()
           f.write('tolerance = '+ tol+'\n')
           q1=self.lineEdit_firstq.text().ascii()
           f.write('first q = '+ q1+'\n')
           dq=self.lineEdit27.text().ascii()
           f.write('delta q = '+ dq+'\n')
           sq=self.lineEdit28.text().ascii()
           f.write('step q = '+ sq+'\n')
           nq=self.lineEdit_nq.text().ascii()
           f.write('number of q = '+ nq+'\n')
           nq_TRC=self.lineEdit_qTRC.text().ascii()
           f.write('q for TRC = '+ nq_TRC+'\n')
           f.close()
           print 'new input file created:', filename
        
        
        
        

    def change_labelsq(self):
           self.textLabel29.setText('first angle (in degrees)')
           self.textLabel30.setText('delta angle (in degrees)')
           self.textLabel31.setText('step angle (in degrees)')
           self.textLabel32.setText('no. of angle')
           self.textLabel29_2.setText('first angle (in degrees)')
           self.textLabel30_2.setText('delta angle (in degrees)')
           self.textLabel31_2.setText('step angle (in degrees)')
        

    def change_labelsback(self):
           Inv_Ang=u"(\u00C5\u207B\u00B9):"
           Ang=u"(\u00C5):"
           self.textLabel16.setText('waverlength '+ Ang)
           self.textLabel29.setText('first q '+ Inv_Ang)
           self.textLabel30.setText('delta q '+Inv_Ang)
           self.textLabel31.setText('step q ' + Inv_Ang)
           self.textLabel32.setText('no. of q')
           self.textLabel29_2.setText('first q '+ Inv_Ang)
           self.textLabel30_2.setText('delta q '+Inv_Ang)
           self.textLabel31_2.setText('step q ' + Inv_Ang)
        

    def user_mask(self):
          self.makeinput()
          mask_file=self.lineEdit_mask.text().ascii()
          data_file=self.lineEdit_data.text().ascii()
          if os.path.exists(data_file) is False:
             print 'static data ', data_file, "doesn't exist: using first image"
             dir=self.lineEditDataDir.text().ascii()
             prefix=self.lineEditDataPrefix.text().ascii()
             suffix=self.lineEditDataSuff.text().ascii()
             no=self.lineEditDataStart.text().ascii()
             data_file=dir+file_name(prefix,suffix,no)
          if os.path.exists(mask_file) is False:
             self.automask()
          else:
             make_mask(data_file,mask_file)
          print 'done'
          self.plot_masked()
        
        

    def plot_masked(self):
          self.makeinput()
          data_file=self.lineEdit_data.text().ascii()
          if os.path.exists(data_file) is False:
             self.dostatic_quick()
          data=loadedf(data_file)
          mask_file=self.lineEdit_mask.text().ascii()
          print mask_file
          self.automask()
          mymask=loadedf(mask_file,0)+loadedf(mask_file,1)
          print 'plotted masked data'
          if self.checkBox_zoom.isChecked():
             self.matplotlibWidget1.update_figure(0,data+1,data_file,mymask,Zoom='fixed')
          else:
             self.matplotlibWidget1.update_figure(0,data+1,data_file,mymask)
        

    def plot_unmasked(self):
          self.makeinput()
          data_file=self.lineEdit_data.text().ascii()
          if os.path.exists(data_file) is True:
             data=loadedf(data_file)
             if self.checkBox_zoom.isChecked():
                self.matplotlibWidget1.update_figure(1,data+1,data_file,Zoom='fixed')
             else:
                self.matplotlibWidget1.update_figure(1,data+1,data_file)
        

    def update_text(self):
          data_file=self.lineEdit12.text().ascii()+self.lineEdit13.text().ascii()+'static.edf'
          qmask_file=self.lineEdit12.text().ascii()+self.lineEdit13.text().ascii()+'qmask.edf'
          cf_file=self.lineEdit12.text().ascii()+self.lineEdit13.text().ascii()+'cf.dat'
          nq=self.lineEdit_plotq_TRcf.text().ascii()
          TRcf_file=self.lineEdit12.text().ascii()+self.lineEdit13.text().ascii()+'2times_q_'+nq+'.edf'
          nq_chi4=self.q_lineEdit_chi4.text().ascii()
          chi4_file=self.lineEdit12.text().ascii()+self.lineEdit13.text().ascii()+'fitchi4_q_'+nq_chi4+'.dat'
          self.lineEdit_data.setText(data_file)
          self.lineEdit_qmask.setText(qmask_file)
          self.lineEdit_cf.setText(cf_file)
          self.lineEdit_TRcf.setText(TRcf_file)
          self.lineEdit_chi4_file.setText(chi4_file)
         
        
        

    def dodarks(self): 
             self.makeinput()
             print 'calculating dark...'
             dir=self.lineEditDarkDir.text().ascii()
             prefix=self.lineEditDarkPrefix.text().ascii()
             prefix=dir+prefix
             suffix=self.lineEditDataSuff.text().ascii()
             nstart=int(self.lineEditDarkStart.text().ascii())
             nend=int(self.lineEditDarkEnd.text().ascii())
             files=[]
             for i in range(nstart,nend):
                dark_file=file_name(prefix,suffix,i)
                files.append(dark_file)
             if os.path.exists(dir) is False:
                print "dark directory doesn't exist, please check it!!!!"
             elif os.path.exists(files[0]) is False:
                print "dark prefix or numbers wrong, please check it!!!!"
             else:
                detector=self.comboBox_detector.currentText().ascii().lower()
                flatfield_file=self.comboBox_flatfield.currentText().ascii()
                if flatfield_file== 'other':
                   flatfield_file=self.lineEdit_other.text().ascii()
                while os.path.exists(files[-1]) is False:
                   print 'waiting for dark ', files[-1]
                dark=sum_data(files,detector,flatfield_file)
                dark_file=self.lineEdit_dark.text().ascii()
                print dark_file
                saveedf(dark_file,dark)
                if self.checkBox_zoom.isChecked():
                   self.matplotlibWidget1.update_figure(1,dark,dark_file,logscale='nolog',Zoom='fixed')
                else:
                   self.matplotlibWidget1.update_figure(1,dark,dark_file,logscale='nolog')
                print '...done'
                 

    def dostatic_quick(self):
             print 'calculating quick static...'
             self.dostatic('quick')
        

    def dostatic_all(self):
             print 'calculating accurate static...'
             self.dostatic('all')
        

    def dostatic(self,mode):
     self.makeinput()
     inputfile=self.lineEdit_input.text().ascii()
     if mode=='quick':
        data=do_average(inputfile,nstart='first',nend='nstart+20')
     if mode=='all':
        data=do_average(inputfile,nstart='first',nend='last')
     data_file=self.lineEdit12.text().ascii()+self.lineEdit13.text().ascii()+'rawstatic.edf'
     saveedf(data_file,data)
     if self.checkBox_darks.isChecked():
        dark_file=self.lineEdit_dark.text().ascii()
        if os.path.exists(dark_file) is False:
          self.dodarks()
        dark=loadedf(dark_file)
     else:
        dark=0*data
     data_file=self.lineEdit_data.text().ascii()
     info=get_input(inputfile)
     detector=info['detector']
     if detector!= 'medipix':
        data-=dark
     data[data<=0]=0
     saveedf(data_file,data)
     if self.checkBox_zoom.isChecked():
        self.matplotlibWidget1.update_figure(1,(data+1),data_file,Zoom='fixed')
     else:
        self.matplotlibWidget1.update_figure(1,(data+1),data_file)
     print '...done'

    def plot_dark(self):
          self.makeinput()
          dark_file=self.lineEdit_dark.text().ascii()
          if os.path.exists(dark_file) is False:
            self.dodarks()
          dark=loadedf(dark_file)
          if self.checkBox_zoom.isChecked():
             self.matplotlibWidget1.update_figure(1,dark,dark_file,logscale='nolog',Zoom='fixed')
          else:
             self.matplotlibWidget1.update_figure(1,dark,dark_file,logscale='nolog')
        

    def correlator(self):
        self.makeinput()
        self.loadinput(0)
        inputfile=self.lineEdit_input.text().ascii()
        staticfile=self.lineEdit_data.text().ascii()
        maskfile=self.lineEdit_mask.text().ascii()
        darkfile=self.lineEdit_dark.text().ascii()
        qmaskfile=self.lineEdit_qmask.text().ascii()
        if self.checkBox_darks.isChecked():
           if os.path.exists(darkfile) is False:
              self.dodarks()
              self.dostatic_quick()
        if os.path.exists(staticfile) is False:
           self.dostatic_quick()
        static=loadedf(staticfile)
        if os.path.exists(maskfile) is False:
           print 'making mask'
           self.automask() #the user_mask is directly called in automask as there is no mask file yet
        mask=loadedf(maskfile)
        if shape(mask)!=shape(static):
           print 'mask and static data have different size.... please make a mask!'
           self.user_mask()
        if os.path.exists(qmaskfile) is False:
           print 'making q mask'
           self.Qs()
        qmask=loadedf(qmaskfile)
        nq=int(self.lineEdit_nq.text().ascii())
        if int(qmask.max()/2)!= nq:
           print 'updating qmask...'
           self.Qs()
           print '...done'
        if shape(qmask)!=shape(static):
           print 'q mask and static data have different size.... calculating q mask!'
           self.Qs()
        if self.checkBox_plot.isChecked():
           arg=inputfile,darkfile,maskfile
        else:
           arg=inputfile,darkfile,maskfile,'no'
        self.Iq()
        if self.checkBox_multiproc.isChecked():
           from correlator_online_new_mp import correlator_online_mp
           tmain=threading.Thread(target=correlator_online_mp,args=(arg))
        else:
           from correlator_online_new import correlator_online
           tmain=threading.Thread(target=correlator_online,args=(arg))
        tmain.start()
        

    def stop_correlator(self):
          print 'ciao'
          os.spawnlp(os.P_WAIT, 'stop')
        
        

    def change_labelsbeam(self):
           self.textLabel19.setText('X reflected beam:')
           self.textLabel20.setText('Y reflected beam:')
           self.textLabel22.setEnabled(1)
           self.lineEdit20.setEnabled(1)
        

    def change_labelsbeamback(self):
           self.textLabel19.setText('X direct beam:')
           self.textLabel20.setText('Y direct beam:')
        

    def plot_raw(self):
          self.makeinput()
          raw_file=self.lineEdit12.text().ascii()+self.lineEdit13.text().ascii()+'rawstatic.edf'
          if os.path.exists(raw_file) is False:
             self.dostatic_quick()
          data=loadedf(raw_file)
          if self.checkBox_zoom.isChecked():
             self.matplotlibWidget1.update_figure(1,data+1,raw_file,Zoom='fixed')
          else:
             self.matplotlibWidget1.update_figure(1,data+1,raw_file)
        

    def plot_cf(self):
          filename=self.lineEdit_cf.text().ascii()
          if os.path.isfile(filename):
            f=open(filename,'r')
            title= f.readline()
            qlist=title.split(': ')[-1]
            qs=qlist.split(' ')
            f.close()
            hold=False
            nq=self.lineEdit_plotq.text().ascii()
            if nq.lower()=='all':
               firstq=int(1)
               lastq=len(qs)+1
            elif nq.find(':')!=-1:
               limits=nq.split(':')
               firstq=int(limits[0])
               lastq=int(limits[1])+1
            else:
               firstq=int(nq)
               lastq=int(nq)+1
            if self.checkBox_hold.isChecked():
               hold=True
            cfdata=loadtxt(filename)
            markers=self.matplotlibWidget_cf.update_plot(cfdata,hold,firstq,lastq,qs,filename,"G(t)") 
          else:
            print "file ",filename," does not exist!"
        
        

    def del_cf(self):
          file=self.lineEdit_cf.text().ascii()
          nq=self.lineEdit_plotq.text().ascii()
          if nq.lower()=='all':
              self.matplotlibWidget_cf.cla() 
          else:
            if nq.find(':')!=-1:
              limits=nq.split(':')
              firstq=int(limits[0])
              lastq=int(limits[1])+1
            else:
              firstq=int(nq)
              lastq=int(nq)+1
            del_data=loadtxt(file) 
            self.matplotlibWidget_cf.remove_plot(del_data[:,firstq:lastq]) 
        

    def plot_TRcf(self):
          self.update_text()
          file=self.lineEdit_TRcf.text().ascii()
          if os.path.exists(file) is False:
             print 'file ', file, "doesn't exist"
          else:
            zmin=self.lineEdit_zmin.text().ascii()
            zmax=self.lineEdit_zmax.text().ascii()
            data=ytrc.read(file)
            datadim=shape(data)[0]#sqrt(size(data))
            while datadim>4000:
               newdim=int(datadim/2)
               data=ytrc.rebin(data,(newdim,newdim))
               datadim=shape(data)[0]#sqrt(size(data))
            if zmin!='auto':
               zmin=float(zmin)
            else:
               self.lineEdit_zmin.setText(str(0))
            if zmax!='auto':
               zmax=float(zmax)
            else:
               self.lineEdit_zmax.setText(str(mean(diag(data,k=5))-1))
            self.matplotlibWidget_TRC.update_figure(1,data,file,zmax=zmax,zmin=zmin)
        

    def calc_TRCF(self):
          print "this doesnot work"
          #self.update_text()
          #outfile=self.lineEdit_TRcf.text().ascii()
          #nq=int(lineEdit_plotq_TRcf.text().ascii())
          #thread.start_new_thread(TRCF(nq,outfile))
        

    def Qs(self):
           self.makeinput()
           input_file=self.lineEdit_input.text().ascii()
           input_info=get_input(input_file)
           qtot=qpattern(input_info)           
           geometry=input_info['geometry']
           if geometry == 'gisaxs':
              qtot=qtot[1]
           firstq=float(input_info['first q'])
           deltaq=float(input_info['delta q'])
           stepq=float(input_info['step q'])
           nq=int(input_info['number of q'])
           lastq=firstq+nq*(stepq+deltaq)
           qvalues=arange(firstq,lastq,stepq+deltaq)
           if len(qvalues)>nq:
             qvalues.resize((nq,))
           qaxis_list=[]
           I=[]
           static_file=self.lineEdit_data.text().ascii()
           if os.path.exists(static_file) is False:
              self.dostatic_quick()
           static_data=loadedf(static_file)
           mask_file=self.lineEdit_mask.text().ascii()
           if os.path.exists(mask_file) is False:
              self.user_mask()
           if EdfFile.EdfFile(mask_file).GetNumImages()!=2:
              self.automask()
           totmask=loadedf(mask_file,0)+loadedf(mask_file,1)
           fileq=self.lineEdit_qmask.text().ascii()
           qvalue=firstq
           firsttime=0
           qsave=0*static_data
           n=0
           for el,q in enumerate(qvalues):
              ind=where((qtot>=q)&(qtot<=q+deltaq)&(totmask==0))
              npixel=len(ind[0])
              #This is to reject q-rings that have no pixels (e.g. behind the beamstop or outside the ccd range, it permits to put in the input firstq=0 and an arbitrary high number of qs)
              if npixel!=0:
                 n+=2
                 if firsttime==0:
                    firstq=q
                    self.lineEdit_firstq.setText(str(firstq))
                 qsave[ind]=n
                 firsttime=1
                 qval=q+deltaq/2
                 qaxis_list.append(qval)
                 I.append(p.average(static_data[ind]))
           saveedf(fileq,qsave)
           outfile=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'1Dstatic.dat'
           f=open(outfile,'w')
           f.write('#q (1/Ang) I(q) (a.u.) \n')
           qaxis=array(qaxis_list)
           I_q=array(I)
           tosave=transpose(array([qaxis,I_q]))
           savetxt(f,tosave)
           f.close()
           nq=len(qaxis_list)
           self.lineEdit_nq.setText(str(nq))
           qsave[qsave==0]=1
           qsave[qsave>=2]=0
           if self.checkBox_zoom.isChecked():
              self.matplotlibWidget1.update_figure(0,static_data+1,fileq,qsave+totmask,Zoom='fixed')
           else:
              self.matplotlibWidget1.update_figure(0,static_data+1,fileq,qsave+totmask)
           self.makeinput()
        

    def plotQmask(self): 
           static_file=self.lineEdit_data.text().ascii()
           if os.path.exists(static_file) is False:
              self.dostatic_quick()
           static_data=loadedf(static_file)
           mask_file=self.lineEdit_mask.text().ascii()
           if os.path.exists(mask_file) is False:
              self.user_mask()
           if EdfFile.EdfFile(mask_file).GetNumImages()!=2:
              self.automask()
           totmask=loadedf(mask_file,0)+loadedf(mask_file,1)
           fileq=self.lineEdit_qmask.text().ascii()
           if os.path.exists(fileq) is False:
              self.Qs()
           q=loadedf(fileq)
           q[q==0]=1
           q[q>=2]=0
           if self.checkBox_zoom.isChecked():
              self.matplotlibWidget1.update_figure(0,static_data+1,fileq,q+totmask,Zoom='fixed')
           else:
              self.matplotlibWidget1.update_figure(0,static_data+1,fileq,q+totmask,)
        

    def Iq(self):
           self.makeinput()
           input_file=self.lineEdit_input.text().ascii()
           input_info=get_input(input_file)
           qtot=qpattern(input_info)
           geometry=input_info['geometry']
           if geometry == 'gisaxs':
              qtot=qtot[1]
           wavelength=float(self.lineEdit_lambda.text().ascii())
           distance=float(self.lineEdit_dsd.text().ascii())
           detector=self.comboBox_detector.currentText().ascii().lower()
           if detector == 'princeton' or detector == 'andor 22.5micron':
              pix_size=0.0225      
           if detector == 'medipix':
              pix_size=0.055      
           if detector == 'andor 13micron' or detector == 'andor':
              pix_size=0.013      
           deltaq=4*pi/wavelength*sin(arctan(2*pix_size/distance)/2)
           static_file=self.lineEdit_data.text().ascii()
           if os.path.exists(static_file) is False:
              self.dostatic_quick()
           static_data=loadedf(static_file)
           mask_file=self.lineEdit_mask.text().ascii()
           if os.path.exists(mask_file) is False:
              self.user_mask()
           if EdfFile.EdfFile(mask_file).GetNumImages()!=2:
              self.automask()
           totmask=loadedf(mask_file,0)+loadedf(mask_file,1)
           q=qtot[totmask==0]
           indq=argsort(q)
           q=q[indq]
           qr=arange(min(q),max(q)+deltaq,deltaq)
           m=static_data[totmask==0]
           m=m[indq]
           lqv=len(qr)
           ini=0
           hh,bins=histogram(q,lqv)
           radi=zeros((len(bins)-1,2))
           radi[:,0]=bins[:-1]+deltaq/2
           for i in xrange(lqv):
              radi[i,1]=mean(m[ini:ini+hh[i]])
              ini=ini+hh[i]
           outfile=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'1Dstatic_fine.dat'
           f=open(outfile,'w')
           f.write('#q (1/Ang) I(q) (a.u.) \n')      
           savetxt(f,radi)
           f.close()  
           outfile=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'1Dstatic.dat'
           if os.path.isfile(outfile): 
             iq_data=loadtxt(outfile)  
             radi=transpose(radi)
             self.matplotlibWidget1.update_plotlog(iq_data[:,0],iq_data[:,1],radi[0],radi[1])
           else:
             print "Make Qs first!"

    def automask(self):
         filename=self.lineEdit_input.text().ascii()
         self.makeinput()
         input_info=get_input(filename)
         tolerance=float(input_info['tolerance'])
         print 'tolearance = ', tolerance
         datafile=self.lineEdit_data.text().ascii()
         if os.path.exists(datafile) is False:
            self.dostatic_quick()
         data=loadedf(datafile)
         if tolerance>=0:
           detector=self.comboBox_detector.currentText().ascii().lower()
           treshold_mask=auto_mask(input_info,dark_file=self.lineEdit_dark.text().ascii())
         else:
             print 'using only user mask'
             treshold_mask=zeros(shape(data),dtype=int)
         mask_file=self.lineEdit_mask.text().ascii()
         print mask_file
         if os.path.exists(mask_file):
           usermask=loadedf(mask_file,0)
           saveedf(mask_file,usermask,0)
           saveedf(mask_file,treshold_mask,1)
         else: 
           print 'make user mask'
           usermask=0*treshold_mask
           saveedf(mask_file,usermask,0)
           saveedf(mask_file,treshold_mask,1)
           self.user_mask()

        

    def clear_cf(self):
          self.matplotlibWidget_cf.cla()
        

    def chi4(self):
          print "this does not work!" 
          #self.update_text()
          #inputfile=self.lineEdit_input.text().ascii()
          #q_chi4=int(self.q_lineEdit_chi4.text().ascii())
          #print '...calculating chi4'
          #mask_file=self.lineEdit_mask.text().ascii()
          #dark_file=self.lineEdit_dark.text().ascii()
          #arg=q_chi4,inputfile,dark_file,mask_file
          #tchi4=threading.Thread(target=chi4,args=(arg))
          #tchi4.start()
        # # tchi4.join()
          #print 'plotting'
        # # chi4(q_chi4,fileinput=inputfile,mask_file=mask_file,dark_file=dark_file)
          #self.plot_chi4()
        

    def plot_chi4(self):
          self.update_text()
          chi4_file=self.lineEdit_chi4_file.text().ascii()
          if os.path.isfile(chi4_file):
            f=open(chi4_file,'r')
            line=f.readline()
            qs=[line.split(":")[1]]*2
            chi4_data=loadtxt(chi4_file)
            hold=False 
            if self.checkBox_hold_chi4.isChecked():
              hold=True
            self.matplotlibWidget_chi4.update_plot(chi4_data,hold,1,2,qs,chi4_file,"Chi_4") 
          else:
            print 'chi4 file ', chi4_file, "doesn't exist"


    def fit(self):
          tmain=threading.Thread(target=os.spawnlp,args=(os.P_WAIT,'PYFIT'))
          tmain.start()
        
        #  os.spawnlp(os.P_WAIT, 'multifit_gui')
        

    def activate_flatfield(self):
           detector=self.comboBox_detector.currentText().ascii().lower()
           if detector!='medipix':	   
              self.checkBox_flatfield.setEnabled(0)
              self.comboBox_flatfield.setEnabled(0)
           else:
              self.checkBox_flatfield.setEnabled(1)
              self.checkBox_flatfield.setChecked(1)
              self.comboBox_flatfield.setEnabled(1)
              self.comboBox_flatfield.setCurrentItem(0)
        

    def Loadflatfield(self):
           PathLineEdit = "./"
           flatfield_file = QFileDialog.getOpenFileName(PathLineEdit,('*.edf'))
           self.lineEdit_other.setText(flatfield_file)
        
        
        

    def activateLoad(self):
           flatfield_file=self.comboBox_flatfield.currentText().ascii().lower()
           if flatfield_file=='other':
              self.Loadflatfield()
              self.lineEdit_other.setEnabled(1)
           else:
              self.lineEdit_other.clear()
              self.lineEdit_other.setEnabled(0)
        

    def LoadDataDir(self):
           PathLineEdit = "./"
           dir = QFileDialog.getExistingDirectory(PathLineEdit)
           if dir:
              self.lineEditDataDir.setText(dir)
        

    def LoadDarkDir(self):
           PathLineEdit = self.lineEditDataDir.text().ascii()
           dir = QFileDialog.getExistingDirectory(PathLineEdit)
           if dir:
              self.lineEditDarkDir.setText(dir)
        

    def LoadOutDir(self):
           PathLineEdit = "./"
           dir = QFileDialog.getExistingDirectory(PathLineEdit)
           if dir:
              self.lineEdit12.setText(dir)
        

    def LoadMaskFile(self):
           PathLineEdit = self.lineEdit_mask.text().ascii()
           filename = QFileDialog.getOpenFileName(PathLineEdit,('*.edf'))
           if filename:
              self.lineEdit_mask.setText(filename)
        

    def LoadDarkFile(self):
           PathLineEdit = self.lineEdit_dark.text().ascii()
           filename = QFileDialog.getOpenFileName(PathLineEdit,('*.edf'))
           if filename:
              self.lineEdit_dark.setText(filename)
        

    def SetNormalizeList(self):
           self.comboBox_normalize.clear()
           self.comboBox_normalize.insertItem(self.__tr("None"))
           self.comboBox_normalize.insertItem(self.__tr("Average in CCD"))
           detector=self.comboBox_detector.currentText().ascii().lower()
           if detector!='medipix':
              self.comboBox_normalize.insertItem(self.__tr("Monitor"))
        
        

    def __tr(self,s,c = None):
        return qApp.translate("Form1",s,c)
    
    def pmake_mask(self,data_file,mask_file='none'):
       global key, x, y,lc,data,im,xy,mymask,xx,yy,px,lx,lm,default_mask,maskfig
       # determine if a point is inside a given polygon or not
       # Polygon is a list of (x,y) pairs.
      
       #read input parameters
   
       header=headersedf(data_file)
       data=loadedf(data_file)
       lx,ly=p.shape(data)
       if os.path.exists(mask_file) is True:
          mymask=loadedf(mask_file,0)
          automask=loadedf(mask_file,1)
       if p.shape(mymask)!=p.shape(data):
          mymask=zeros((lx,ly))
       else:
          mymask=zeros((lx,ly))
          automask=zeros((lx,ly))

       points=[]
       for i in range(lx):
         for j in range(ly):
           points.append([i,j]) 
       key=[]
       x=0
       y=0
       xy=[]
       xx=[]
       yy=[]
  
       def on_click(event):
        global key, x, y,lc,data,im,xy,mymask,xx,yy,px,lx,lm,default_mask,maskfig
        if not event.inaxes: 
           xy=[]
           return
        x,y=int(event.xdata), int(event.ydata)
        key=event.key
        xx.append([x])
        yy.append([y])
        xy.append([y,x])
        lc.set_data(xx,yy)
        if key=='m': 
           print 'masking'
           xx[-1]=xx[0]
           yy[-1]=yy[0]
           xy[-1]=xy[0]
           ind=p.nonzero(points_inside_poly(points,xy))
           mymask=mymask.reshape(lx*ly,1)
           mymask[ind]=1
           mymask=mymask.reshape(lx,ly)
     #      mymask[default_mask==1]=1
           data=masked_array(data,mymask+automask)
           im.set_data(data)
           xx=[]
           yy=[]
           xy=[] 
           lc.set_data(xx,yy)
           lm.set_data(xx,yy)
           p.draw()
           x=0
           y=0 
        if key=='u': 
           xx[-1]=xx[0]
           yy[-1]=yy[0]
           xy[-1]=xy[0]
           ind=p.nonzero(points_inside_poly(points,xy))
           mymask=mymask.reshape(lx*ly,1)
           mymask[ind]=0
           mymask=mymask.reshape(lx,ly)
    #       mymask[default_mask==1]=1
           data=masked_array(data,mymask+automask)
           im.set_data(data)
           xx=[]
           yy=[]
           xy=[] 
           lc.set_data(xx,yy)
           lm.set_data(xx,yy)
           p.draw()
           x=0
           y=0 
        if key=='r':
          mymask=0*mymask
          mymask=mymask.reshape(lx,ly)
          data=masked_array(data,mymask+automask)
          im.set_data(data)
          xx=[]
          yy=[]
          xy=[] 
          lc.set_data(xx,yy)
          lm.set_data(xx,yy)
          p.draw()
          x=0
          y=0 
        if key=='w':
          print 'exit'
          p.close()
          saveedf(mask_file,mymask,0)
          saveedf(mask_file,automask,1)
          print 'Mask saved in file:', mask_file
          return
          #p.close()
   
       def on_move(event):
        global lm,x,y
        if not event.inaxes: return
        xm,ym=int(event.xdata), int(event.ydata)
        # update the line positions
        if x!=0: 
           lm.set_data((x,xm),(y,ym))
           p.draw()
       p.rc('image',origin = 'lower')
       p.rc('image',interpolation = 'nearest')
       p.figure()
       px=p.subplot(111)
       data=p.log(data+1)
       #p.ion()
       im=p.imshow(masked_array(data,mymask+automask))
       p.title("Select a ROI. Press m to mask or u to unmask it \n w to write mask and exit")
       lc,=px.plot((0,0),(0,0),'-+m',linewidth=1,markersize=8,markeredgewidth=1)
       lm,=px.plot((0,0),(0,0),'-+m',linewidth=1,markersize=8,markeredgewidth=1)
       px.set_xlim(0,ly)
       px.set_ylim(0,lx)
       cidb=p.connect('button_press_event',on_click)
       cidk=p.connect('key_press_event',on_click)
       cidm=p.connect('motion_notify_event',on_move)
       p.show()
       return
