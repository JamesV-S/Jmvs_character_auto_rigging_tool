
import maya.cmds as cmds
from maya import OpenMayaUI as omui

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from shiboken2 import wrapInstance

import os.path
import importlib
import sys
import subprocess
import platform


mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

class QtSampler(QWidget):
    def __init__(self, *args, **kwargs):
        super(QtSampler,self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Jmvs Char Auto Rigger")
        self.initUI()
        
        # self.update_d

        # Tab 1
        '''
        self.ui.scale_spnB.valueChanged.connect(self.scale_of_ctrl)
        self.ui.axs_ddbx.currentIndexChanged.connect(self.axs_dir_ddbox)
        self.ui.zero_out_checkBx.stateChanged.connect(self.clean_ctrls)
        self.ui.num_ctrl_line.textChanged.connect(self.num_ctrl_input)
        self.ui.new_ctrl_ddp.currentIndexChanged.connect(self.cr_nw_ctrl)
        self.ui.type_ctrl_ddbox.currentIndexChanged.connect(self.ctrl_type_func)
        self.ui.sys_type_line.textChanged.connect(self.sys_type)
        self.ui.colour_line.textChanged.connect(self.ctl_colour)
        self.ui.apply_btn.clicked.connect(self.apply_func)
        '''
        # Tab 2

        # Tab 3

    # functions, connected to above commands   
    def initUI(self):
        loader = QUiLoader()
        UI_VERSION = "001"
        # Constructing the UI File Path
        UI_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               "interface", f"Jmvs_character_auto_rigger_{UI_VERSION}.ui")
        print(f"UI Jmvs_CAR file path: {UI_FILE}")
        # Instead of writing the path manually: Gets absolute path of ui file, 
        # as os.path.join() constructs a path by combining the directory with 
        # the relative path:  ui.py directory + "interface\\Jmvs_character_auto_rigger_001.ui".

        if not os.path.exists(UI_FILE):
            cmds.error(f"ERROR: UI file path doesn't exist: {UI_FILE}")
        #`os.path.exists(UI_FILE)` checks if the UI file exists at the specified path.

        file = QFile(UI_FILE)
        if not file.open(QFile.ReadOnly):
            cmds.error(f"ERROR: UI file path doesn't open: {UI_FILE}")

        self.ui = loader.load(file, parentWidget=self)
        file.close()
    #--------------------------------------------------------------------------     
    
       
def main():
    ui = QtSampler()
    ui.show()
    return ui

'''
if __name__ == '__main__':
    main()
'''  

