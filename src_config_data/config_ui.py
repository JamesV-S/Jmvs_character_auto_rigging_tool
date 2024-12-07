
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
from functools import partial # if you want to include args with UI method calls                   

import os.path
import importlib
import sys
import configparser

from src_config_systems import (
    fk_sys,
    ik_sys,
    jnts,
    config_cr_blueprints,
    squash_stretch    
)

from config_utils import (
    ikfk_switch,
    mdl_foll_connection,
    utils,
    mirror_guides_jnts,
    space_swap,
    OPM,
    neck_twistBend_sys
)

importlib.reload(config_cr_blueprints)
importlib.reload(jnts)
importlib.reload(utils)
importlib.reload(mirror_guides_jnts)
importlib.reload(fk_sys)
importlib.reload(ik_sys)
importlib.reload(ikfk_switch)
importlib.reload(squash_stretch)
importlib.reload(space_swap)
importlib.reload(OPM)
importlib.reload(mdl_foll_connection)
importlib.reload(neck_twistBend_sys)


def delete_existing_ui(ui_name):
    if cmds.window(ui_name, exists=True):
        cmds.deleteUI(ui_name, window=True)

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)

def delete_existing_ui(ui_name):
    # Delete existing UI if it exists
    if cmds.window(ui_name, exists=True):
        cmds.deleteUI(ui_name, window=True)

class QtSampler(QWidget):
    def __init__(self, *args, **kwargs):
        super(QtSampler,self).__init__(*args, **kwargs)
        # Ensure any existing UI is removed
        delete_existing_ui("JmvsCharAutoRiggerUI")
        # Set a unique object name
        self.setObjectName("JmvsCharAutoRiggerUI")
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Jmvs Char Auto Rigger")
        self.initUI()

        if self.blueprints_toolbtn:
            print(f"Found blueprints_menu_toolbtn in the ui")
            self.blueprints_toolbtn.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
            self.create_popup_menu()
        else:
            print(f"could not find blueprints_menu_toolbtn in the ui")

    # functions, connected to above commands   
    def initUI(self):
        loader = QUiLoader()
        UI_VERSION = "003"
        # Constructing the UI File Path
        UI_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               "config_parent_interface", f"Jmvs_character_auto_rigger_{UI_VERSION}.ui")
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

    # For the seperate modules i would like to have the option for them to spawn 
    # somewhere in space with a locator that loads in from selecting checkbox on my ui

    def create_popup_menu(self):
        # Create a QMenu
        menu = QMenu(self)
        # cr actions for the buttons
        biped_action = QAction("Biped - Basic", self)
        quad_action = QAction("Quad - Basic", self)

        # connect the actions to their respective fucntions.
        biped_action.triggered.connect(self.load_biped_basic_blueprint)
        quad_action.triggered.connect(self.load_quad_basic_blueprint)

        # ad actions to the menu
        menu.addAction(biped_action)
        menu.addAction(quad_action)

        # set the menu to the blueprints_toolbtn
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