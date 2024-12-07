
import sys
import os
import configparser
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QWidget)
from shiboken6 import wrapInstance
import maya.cmds as cmds
from maya import OpenMayaUI as omui

def delete_existing_ui(ui_name):
    if cmds.window(ui_name, exists=True):
        cmds.deleteUI(ui_name, window=True)

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)

class CtrlConfigUI(QtWidgets.QWidget):
    def __init__(self, config_file, *args, **kwargs):
        super(CtrlConfigUI, self).__init__(*args, **kwargs)
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        
        self.setObjectName("CtrlConfigUI")
        delete_existing_ui(self.objectName())
        self.setParent(maya_main_window())
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Control Config UI")
        self.resize(400, 200)
    
        self.initUI()
    
    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        self.control_type_box = QtWidgets.QComboBox()
        self.control_type_box.addItems(self.config.options('ctrl_Shapes'))
        layout.addWidget(self.control_type_box)
        
        save_button = QtWidgets.QPushButton("_Save_")
        layout.addWidget(save_button)
        
        save_button.clicked.connect(self.save_changes)
    
    def save_changes(self):
        selected_control = self.control_type_box.currentText()
        ''' make this more dynamic now it works, set frst ctrl shape to selected on ui
        self.config.set('ControlShapes', 'circle', selected_control)
        '''
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        print("Config updated!")

def open_ui_on_sel(config_file):
    selected = cmds.ls(selection=True)
    if selected:
        app = QtWidgets.QApplication.instance()
        if not app: # If there is no 
            app = QtWidgets.QApplication([])# Use an empty list for maya
    
        ui = CtrlConfigUI(config_file)
        ui.show()
        app.exec()
        return ui
    
if __name__ == '__open_ui_on_sel__':
    print("RUN IF")
else:
    print("DIDN'T RUN IF")