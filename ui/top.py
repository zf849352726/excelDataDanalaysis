# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'top.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(773, 693)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(True)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks|QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks|QtWidgets.QMainWindow.ForceTabbedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget_2 = QtWidgets.QWidget(self.tab)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.widget_2)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_5 = QtWidgets.QWidget(self.groupBox)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.SelectPathLineEdit = QtWidgets.QLineEdit(self.widget_5)
        self.SelectPathLineEdit.setAutoFillBackground(False)
        self.SelectPathLineEdit.setStyleSheet("image: url(:/images/lineEditPic.png);")
        self.SelectPathLineEdit.setText("")
        self.SelectPathLineEdit.setObjectName("SelectPathLineEdit")
        self.horizontalLayout_6.addWidget(self.SelectPathLineEdit)
        self.SelectNeedDataAnalysisDirButton = QtWidgets.QPushButton(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectNeedDataAnalysisDirButton.sizePolicy().hasHeightForWidth())
        self.SelectNeedDataAnalysisDirButton.setSizePolicy(sizePolicy)
        self.SelectNeedDataAnalysisDirButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.SelectNeedDataAnalysisDirButton.setAutoFillBackground(False)
        self.SelectNeedDataAnalysisDirButton.setStyleSheet("background-image: url(:/images/lineEditPic.png);\n"
"border: none; /* 去掉按钮边框，如果需要 */\n"
"background-repeat: no-repeat; /* 防止背景图片重复 */\n"
"background-position: center; /* 将背景图片居中 */")
        self.SelectNeedDataAnalysisDirButton.setAutoDefault(False)
        self.SelectNeedDataAnalysisDirButton.setObjectName("SelectNeedDataAnalysisDirButton")
        self.horizontalLayout_6.addWidget(self.SelectNeedDataAnalysisDirButton)
        self.fianlPushButton = QtWidgets.QPushButton(self.widget_5)
        self.fianlPushButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fianlPushButton.sizePolicy().hasHeightForWidth())
        self.fianlPushButton.setSizePolicy(sizePolicy)
        self.fianlPushButton.setObjectName("fianlPushButton")
        self.horizontalLayout_6.addWidget(self.fianlPushButton)
        self.checkBox_7 = QtWidgets.QCheckBox(self.widget_5)
        self.checkBox_7.setObjectName("checkBox_7")
        self.horizontalLayout_6.addWidget(self.checkBox_7)
        self.checkBox = QtWidgets.QCheckBox(self.widget_5)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_6.addWidget(self.checkBox)
        self.verticalLayout_2.addWidget(self.widget_5)
        self.widget_4 = QtWidgets.QWidget(self.groupBox)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.TableColName = QtWidgets.QTableView(self.widget_4)
        self.TableColName.setObjectName("TableColName")
        self.TableColName.horizontalHeader().setCascadingSectionResizes(True)
        self.TableColName.horizontalHeader().setSortIndicatorShown(True)
        self.TableColName.horizontalHeader().setStretchLastSection(True)
        self.TableColName.verticalHeader().setCascadingSectionResizes(True)
        self.TableColName.verticalHeader().setStretchLastSection(True)
        self.verticalLayout_13.addWidget(self.TableColName)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.widget_6 = QtWidgets.QWidget(self.groupBox)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ReruleLineEdit = QtWidgets.QLineEdit(self.widget_6)
        self.ReruleLineEdit.setText("")
        self.ReruleLineEdit.setObjectName("ReruleLineEdit")
        self.horizontalLayout_5.addWidget(self.ReruleLineEdit)
        self.FilterColNameLineEdit = QtWidgets.QLineEdit(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FilterColNameLineEdit.sizePolicy().hasHeightForWidth())
        self.FilterColNameLineEdit.setSizePolicy(sizePolicy)
        self.FilterColNameLineEdit.setObjectName("FilterColNameLineEdit")
        self.horizontalLayout_5.addWidget(self.FilterColNameLineEdit)
        self.SumColNameLineEdit = QtWidgets.QLineEdit(self.widget_6)
        self.SumColNameLineEdit.setObjectName("SumColNameLineEdit")
        self.horizontalLayout_5.addWidget(self.SumColNameLineEdit)
        self.HeaderSpin = QtWidgets.QSpinBox(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HeaderSpin.sizePolicy().hasHeightForWidth())
        self.HeaderSpin.setSizePolicy(sizePolicy)
        self.HeaderSpin.setObjectName("HeaderSpin")
        self.horizontalLayout_5.addWidget(self.HeaderSpin)
        self.verticalLayout_2.addWidget(self.widget_6)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.horizontalLayout.addWidget(self.widget)
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget_3)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.DataTableView = QtWidgets.QTableView(self.groupBox_2)
        self.DataTableView.setObjectName("DataTableView")
        self.DataTableView.horizontalHeader().setCascadingSectionResizes(True)
        self.DataTableView.horizontalHeader().setSortIndicatorShown(True)
        self.DataTableView.horizontalHeader().setStretchLastSection(True)
        self.DataTableView.verticalHeader().setCascadingSectionResizes(True)
        self.DataTableView.verticalHeader().setStretchLastSection(True)
        self.verticalLayout_4.addWidget(self.DataTableView)
        self.widget_7 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.SelectPathLineEdit_2 = QtWidgets.QLineEdit(self.widget_7)
        self.SelectPathLineEdit_2.setText("")
        self.SelectPathLineEdit_2.setObjectName("SelectPathLineEdit_2")
        self.horizontalLayout_7.addWidget(self.SelectPathLineEdit_2)
        self.SelectNeedDataAnalysisDirButton_2 = QtWidgets.QPushButton(self.widget_7)
        self.SelectNeedDataAnalysisDirButton_2.setObjectName("SelectNeedDataAnalysisDirButton_2")
        self.horizontalLayout_7.addWidget(self.SelectNeedDataAnalysisDirButton_2)
        self.verticalLayout_4.addWidget(self.widget_7)
        self.widget_8 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.five_measure_ledger_button = QtWidgets.QPushButton(self.widget_8)
        self.five_measure_ledger_button.setObjectName("five_measure_ledger_button")
        self.horizontalLayout_8.addWidget(self.five_measure_ledger_button)
        self.testButton = QtWidgets.QPushButton(self.widget_8)
        self.testButton.setObjectName("testButton")
        self.horizontalLayout_8.addWidget(self.testButton)
        self.dataMarkButton = QtWidgets.QPushButton(self.widget_8)
        self.dataMarkButton.setObjectName("dataMarkButton")
        self.horizontalLayout_8.addWidget(self.dataMarkButton)
        self.verticalLayout_4.addWidget(self.widget_8)
        self.verticalLayout_6.addWidget(self.groupBox_2)
        self.horizontalLayout.addWidget(self.widget_3)
        self.horizontalLayout_4.addWidget(self.widget_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_12.addWidget(self.label_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_12 = QtWidgets.QWidget(self.tab_3)
        self.widget_12.setObjectName("widget_12")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_12)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_13 = QtWidgets.QWidget(self.widget_12)
        self.widget_13.setObjectName("widget_13")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.widget_13)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.lineEdit = QtWidgets.QLineEdit(self.widget_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_10.addWidget(self.lineEdit)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_10.addWidget(self.pushButton_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.widget_13)
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_10.addWidget(self.checkBox_3)
        self.pushButton_10 = QtWidgets.QPushButton(self.widget_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_10.sizePolicy().hasHeightForWidth())
        self.pushButton_10.setSizePolicy(sizePolicy)
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout_10.addWidget(self.pushButton_10)
        self.verticalLayout_5.addWidget(self.widget_13)
        self.widget_17 = QtWidgets.QWidget(self.widget_12)
        self.widget_17.setObjectName("widget_17")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.widget_17)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget_17)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_12.addWidget(self.lineEdit_2)
        self.pushButton_6 = QtWidgets.QPushButton(self.widget_17)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_12.addWidget(self.pushButton_6)
        self.checkBox_5 = QtWidgets.QCheckBox(self.widget_17)
        self.checkBox_5.setEnabled(False)
        self.checkBox_5.setObjectName("checkBox_5")
        self.horizontalLayout_12.addWidget(self.checkBox_5)
        self.spinBox_3 = QtWidgets.QSpinBox(self.widget_17)
        self.spinBox_3.setObjectName("spinBox_3")
        self.horizontalLayout_12.addWidget(self.spinBox_3)
        self.pushButton_9 = QtWidgets.QPushButton(self.widget_17)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_12.addWidget(self.pushButton_9)
        self.verticalLayout_5.addWidget(self.widget_17)
        self.widget_20 = QtWidgets.QWidget(self.widget_12)
        self.widget_20.setObjectName("widget_20")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.widget_20)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget_20)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_15.addWidget(self.lineEdit_3)
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_20)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_15.addWidget(self.pushButton_5)
        self.checkBox_4 = QtWidgets.QCheckBox(self.widget_20)
        self.checkBox_4.setObjectName("checkBox_4")
        self.horizontalLayout_15.addWidget(self.checkBox_4)
        self.checkBox_2 = QtWidgets.QCheckBox(self.widget_20)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_15.addWidget(self.checkBox_2)
        self.pushButton_8 = QtWidgets.QPushButton(self.widget_20)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_15.addWidget(self.pushButton_8)
        self.verticalLayout_5.addWidget(self.widget_20)
        self.widget_18 = QtWidgets.QWidget(self.widget_12)
        self.widget_18.setObjectName("widget_18")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.widget_18)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.pushButton_7 = QtWidgets.QPushButton(self.widget_18)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_13.addWidget(self.pushButton_7)
        self.verticalLayout_5.addWidget(self.widget_18)
        self.widget_14 = QtWidgets.QWidget(self.widget_12)
        self.widget_14.setObjectName("widget_14")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_14)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_6 = QtWidgets.QLabel(self.widget_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_9.addWidget(self.label_6)
        self.widget_19 = QtWidgets.QWidget(self.widget_14)
        self.widget_19.setObjectName("widget_19")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.widget_19)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.verticalLayout_9.addWidget(self.widget_19)
        self.widget_11 = QtWidgets.QWidget(self.widget_14)
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_11)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.textEdit = QtWidgets.QTextEdit(self.widget_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_9.addWidget(self.textEdit)
        self.graphicsView = QtWidgets.QGraphicsView(self.widget_11)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_9.addWidget(self.graphicsView)
        self.verticalLayout_9.addWidget(self.widget_11)
        self.verticalLayout_5.addWidget(self.widget_14)
        self.verticalLayout.addWidget(self.widget_12)
        self.widget_9 = QtWidgets.QWidget(self.tab_3)
        self.widget_9.setObjectName("widget_9")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget_9)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget_9)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.verticalLayout_14.addWidget(self.label)
        self.widget_10 = QtWidgets.QWidget(self.groupBox_3)
        self.widget_10.setObjectName("widget_10")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.widget_10)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget_10)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.widget_15 = QtWidgets.QWidget(self.widget_10)
        self.widget_15.setObjectName("widget_15")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_15)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget_21 = QtWidgets.QWidget(self.widget_15)
        self.widget_21.setObjectName("widget_21")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.widget_21)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget_21)
        self.lineEdit_4.setText("")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_16.addWidget(self.lineEdit_4)
        self.pushButton_11 = QtWidgets.QPushButton(self.widget_21)
        self.pushButton_11.setObjectName("pushButton_11")
        self.horizontalLayout_16.addWidget(self.pushButton_11)
        self.verticalLayout_7.addWidget(self.widget_21)
        self.widget_22 = QtWidgets.QWidget(self.widget_15)
        self.widget_22.setObjectName("widget_22")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.widget_22)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget_22)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_17.addWidget(self.lineEdit_5)
        self.pushButton_12 = QtWidgets.QPushButton(self.widget_22)
        self.pushButton_12.setObjectName("pushButton_12")
        self.horizontalLayout_17.addWidget(self.pushButton_12)
        self.verticalLayout_7.addWidget(self.widget_22)
        self.widget_16 = QtWidgets.QWidget(self.widget_15)
        self.widget_16.setObjectName("widget_16")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.widget_16)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_5 = QtWidgets.QLabel(self.widget_16)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_11.addWidget(self.label_5)
        self.spinBox = QtWidgets.QSpinBox(self.widget_16)
        self.spinBox.setAccelerated(False)
        self.spinBox.setSingleStep(2)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_11.addWidget(self.spinBox)
        self.label_2 = QtWidgets.QLabel(self.widget_16)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_11.addWidget(self.label_2)
        self.label_7 = QtWidgets.QLabel(self.widget_16)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_11.addWidget(self.label_7)
        self.spinBox_2 = QtWidgets.QSpinBox(self.widget_16)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_11.addWidget(self.spinBox_2)
        self.label_4 = QtWidgets.QLabel(self.widget_16)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_11.addWidget(self.label_4)
        self.verticalLayout_7.addWidget(self.widget_16)
        self.widget_23 = QtWidgets.QWidget(self.widget_15)
        self.widget_23.setObjectName("widget_23")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.widget_23)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_23)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_18.addWidget(self.pushButton_3)
        self.checkBox_6 = QtWidgets.QCheckBox(self.widget_23)
        self.checkBox_6.setObjectName("checkBox_6")
        self.horizontalLayout_18.addWidget(self.checkBox_6)
        self.verticalLayout_7.addWidget(self.widget_23)
        self.horizontalLayout_2.addWidget(self.widget_15)
        self.verticalLayout_14.addWidget(self.widget_10)
        self.verticalLayout_8.addWidget(self.groupBox_3)
        self.verticalLayout.addWidget(self.widget_9)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout_11.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_2.setStyleSheet("border: none;\n"
"background: transparent;")
        self.dockWidget_2.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.dockWidgetContents_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.toolButton_2 = QtWidgets.QToolButton(self.dockWidgetContents_2)
        self.toolButton_2.setArrowType(QtCore.Qt.LeftArrow)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_3.addWidget(self.toolButton_2)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_2)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "计量计价工具箱"))
        self.SelectPathLineEdit.setPlaceholderText(_translate("MainWindow", "选择文件夹"))
        self.SelectNeedDataAnalysisDirButton.setText(_translate("MainWindow", "选择"))
        self.fianlPushButton.setText(_translate("MainWindow", "完成提交"))
        self.checkBox_7.setText(_translate("MainWindow", "需要计算式"))
        self.checkBox.setText(_translate("MainWindow", "对比表格"))
        self.ReruleLineEdit.setPlaceholderText(_translate("MainWindow", "请输入正则表达式"))
        self.FilterColNameLineEdit.setText(_translate("MainWindow", "名称 项目特征描述 计量单位"))
        self.FilterColNameLineEdit.setPlaceholderText(_translate("MainWindow", "输入列名（不同列名 以空格分割）"))
        self.SumColNameLineEdit.setText(_translate("MainWindow", "工程量"))
        self.SumColNameLineEdit.setPlaceholderText(_translate("MainWindow", "请输入求和的列名"))
        self.SelectPathLineEdit_2.setPlaceholderText(_translate("MainWindow", "导出数据的文件夹"))
        self.SelectNeedDataAnalysisDirButton_2.setText(_translate("MainWindow", "导出"))
        self.five_measure_ledger_button.setText(_translate("MainWindow", "五量台账"))
        self.testButton.setText(_translate("MainWindow", "测试一下五量"))
        self.dataMarkButton.setText(_translate("MainWindow", "数据标记"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "数据处理"))
        self.label_3.setText(_translate("MainWindow", "广联达计量GTJ2025自动化软件"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "计量软件自动化"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "输入添加/删除的步骤："))
        self.pushButton_2.setText(_translate("MainWindow", "添加步骤/任务"))
        self.checkBox_3.setText(_translate("MainWindow", "新增任务"))
        self.pushButton_10.setText(_translate("MainWindow", "清空"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "输入插入的步骤/任务："))
        self.pushButton_6.setText(_translate("MainWindow", "插入步骤"))
        self.checkBox_5.setText(_translate("MainWindow", "插入任务"))
        self.pushButton_9.setText(_translate("MainWindow", "清空"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "输入删除的步骤/任务"))
        self.pushButton_5.setText(_translate("MainWindow", "删除步骤/任务"))
        self.checkBox_4.setText(_translate("MainWindow", "删除任务"))
        self.checkBox_2.setText(_translate("MainWindow", "删除所有"))
        self.pushButton_8.setText(_translate("MainWindow", "清空"))
        self.pushButton_7.setText(_translate("MainWindow", "执行"))
        self.label_6.setText(_translate("MainWindow", "当前已有步骤："))
        self.label.setText(_translate("MainWindow", "工具箱"))
        self.pushButton.setText(_translate("MainWindow", "截图"))
        self.pushButton_4.setText(_translate("MainWindow", "excel筛选"))
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "选择插入图片文件夹"))
        self.pushButton_11.setText(_translate("MainWindow", "选择"))
        self.lineEdit_5.setPlaceholderText(_translate("MainWindow", "选择插入的word文件"))
        self.pushButton_12.setText(_translate("MainWindow", "选择"))
        self.label_5.setText(_translate("MainWindow", "宽："))
        self.label_2.setText(_translate("MainWindow", "厘米"))
        self.label_7.setText(_translate("MainWindow", "高："))
        self.label_4.setText(_translate("MainWindow", "厘米"))
        self.pushButton_3.setText(_translate("MainWindow", "word非插入改图"))
        self.checkBox_6.setText(_translate("MainWindow", "插入修改"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "计价软件自动化"))
        self.toolButton_2.setText(_translate("MainWindow", "..."))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))