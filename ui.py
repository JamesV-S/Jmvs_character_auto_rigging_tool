
import maya.cmds as cmds
from maya import OpenMayaUI as omui

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtWidgets, QtCore
from functools import partial # if you want to include args with UI method calls


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

        ''' A method to get the icon Directory!
        tool_file = __file__
        tool_file = tool_file.replace( '\\', '/')

        if '_tool.py' in tool_file:
            product = os.path.basename( tool_file ).split( '_tool.py' )[0]
        else:
            product = os.path.basename( tool_file ).split( '.py' )[0]

        product_fullName = 'UltimateAdjustableCarRig'
        tool_folder = os.path.dirname( tool_file ) + '/'
        rig_folder = tool_folder + 'rigs/'
        tool_fileName = os.path.basename( tool_file ).split( '.py' )[0]

        abrev = 'UACR'
        iconDir = tool_folder + 'icons/'
        '''
        #self.ui.hand_module_btn.clicked.connect(self.temp_hand_func)
        # Tab 1 - RIG
        
        # Access the blueprints_toolbtn
        parent_widget = self.ui.findChild(QtWidgets.QWidget, "tab_rig")
        if parent_widget:
            print("found parent widget")
            self.blueprints_toolbtn = parent_widget.findChild(QtWidgets.QToolButton, "blueprints_menu_toolbtn")
        else:
            print("couldn't find parent widget")
        # set the popup mode for blueprints_toolbtn
        if self.blueprints_toolbtn:
            print(f"Found blueprints_menu_toolbtn in the ui")
            self.blueprints_toolbtn.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
            self.create_popup_menu()
        else:
            print(f"could not find blueprints_menu_toolbtn in the ui")
        
        self.ui.blueprints_menu_toolbtn.clicked.connect(self.blueprints_menu_func)
        
        # Tab 2 - SKINNING

        # Tab 3 - CURVE HELPER

        # Tab 4 - OUTPUT OPTIONS(export)

    # functions, connected to above commands   
    def initUI(self):
        loader = QUiLoader()
        UI_VERSION = "001"
        # Constructing the UI File Path
        UI_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               "interface", f"Jmvs_character_auto_rigger_{UI_VERSION}.ui")
        print(f"UI Jmvs_Character auto rigger file path: {UI_FILE}")
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
    
    def create_popup_menu(self):
        # Create a QMenu
        menu = QMenu(self)

        # Create actions for the buttons
        biped_action = QAction("Biped - Basic", self)
        quad_action = QAction("Quad - Basic", self)

        # Connect the actions to their respective fucntions.
        biped_action.triggered.connect(self.load_biped_basic_blueprint)
        quad_action.triggered.connect(self.load_quad_basic_blueprint)

        # Add actions to the menu
        menu.addAction(biped_action)
        menu.addAction(quad_action)

        # Set the menu to the blueprints_toolbtn
        self.blueprints_toolbtn.setMenu(menu)
    
    def blueprints_menu_func(self):
        # Define the functionality for blueprints_toolbtn here
        print("blueprints menu button clicked")
    
    def load_biped_basic_blueprint(self):
        # Define the functionality for Biped basic button here 
        print("Biped basic button clicked")
    
    def load_quad_basic_blueprint(self):
        # Define the functionality for Quad basic button here
        print("Quad basic button clicked")

    def temp_hand_func(self):
        print("button hand!!!!!!!!!")
def main():
    ui = QtSampler()
    ui.show()
    return ui

'''
if __name__ == '__main__':
    main()
'''  

