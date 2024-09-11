
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

from systems import (
    create_guides
)

from systems.utils import (
    connect_modules, 
    utils
)

# Reload Modules
importlib.reload(create_guides)
importlib.reload(connect_modules)
importlib.reload(utils)

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
        self.update_dropdown() # add available modules to the ddbox on ui
        self.module_created = 0
        self.created_guides = []
        self.systems_to_be_made = {}

        #self.ui.hand_module_btn.clicked.connect(self.temp_hand_func)
        # Tab 1 - RIG
        # if biped_finger is the chosen then enable the finger number ddbox
        self.ui.finger_number_ddbox.setDisabled(True)
        self.ui.finger_lbl.setDisabled(True)
        self.ui.base_skeleton_box.setDisabled(True)

        # Access the blueprints_toolbtn
        parent_widget = self.ui.findChild(QtWidgets.QWidget, "tab_rig")
        if parent_widget:
            print("found parent widget")
            self.blueprints_toolbtn = parent_widget.findChild(QtWidgets.QToolButton, 
                                                              "blueprints_menu_toolbtn")
        else:
            print("couldn't find parent widget")
        # set the popup mode for blueprints_toolbtn which is to addd whole 
        # character presets. 
        if self.blueprints_toolbtn:
            print(f"Found blueprints_menu_toolbtn in the ui")
            self.blueprints_toolbtn.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
            self.create_popup_menu()
        else:
            print(f"could not find blueprints_menu_toolbtn in the ui")
        
        self.ui.blueprints_menu_toolbtn.clicked.connect(self.blueprints_menu_func)
        self.ui.image_lbl.setPixmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                                 "interface","logo_cog.jpeg"))
        
        self.ui.add_mdl_btn.clicked.connect(self.add_module)
        
        # Tab 2 - SKINNING

        # Tab 3 - CURVE HELPER

        # Tab 4 - OUTPUT OPTIONS(export)

    # functions, connected to above commands   
    def initUI(self):
        loader = QUiLoader()
        UI_VERSION = "002"
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

    # For the seperate modules i would like to have the option for them to spawn 
    # somewhere in space with a locator that loads in from selecting checkbox on my ui

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

    def update_dropdown(self):
        #  function updates the dropdown box named "module_picker_ddbox" in the user interface.
        # get the module path: the list comprehension splits each filename at the dots, 
        # removes the extension(last part after the dot) and rejoins the remaining parts.
        # Generating a list of module names without their extensions. 
        files = [".".join(f.split(".")[:-1]) for f in os.listdir(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "systems", "modules"))]
        try: 
            files.remove("")
        except ValueError: 
            pass
        print(f"Update dropdown files: '{files}'")
        files.remove("__init__")
        # Adds the list of modules names to the dopdown menu 
        self.ui.module_picker_ddbox.addItems(files)
        #try: files.remove("")
        #except ValueError: pass
        
        # set default selected item in the dropdown. 
        index = files.index("root_basic")
        self.ui.module_picker_ddbox.setCurrentIndex(index)
        
    def add_module(self):
        # function imports the selected module dynamically during runtim!
        module = self.ui.module_picker_ddbox.currentText()
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                     "systems", "modules"))
        module_path = importlib.import_module(module) # you are calling the import_module function from the importlib module
        importlib.reload(module_path)
        
        print("module_path: ", module_path, "print from ui in add_module()" )
        
        offset = [self.ui.offset_Xaxes_spinbx.value(), 
                  self.ui.offset_Yaxes_spinbx.value(), 
                  self.ui.offset_Zaxes_spinbx.value()
                  ]
    
        # create_guides.py is needed! > in the systems folder!
        guides = create_guides.Guides_class(module, offset, module_path.side, to_connect_to=[], use_existing_attr=[], orientation=[])
        guide = guides.collect_guides()
        print(guide)
        # If guides are succesfully created, this extracts important elements like these:
        if guide:
            master_guide = guide["master_guide"]
            guide_connector_list = guide["guide_connector_list"]
            systems_to_connect = guide["systems_to_connect"]
            guide_list = guide["ui_guide_list"]
            
            # you would have if statement if rev_locators in guide  make a vairable for it, otherwise rev_locators = [] 
            
            # Append the 'master_guide' to a list of created guides 
            self.created_guides.append(master_guide)
            # Enable the skeleton creation box
            self.ui.base_skeleton_box.setDisabled(False)
            
            # create a temp dict to store details abt the module and its guides... 
            temp_dictionary = {
                "module": module, 
                "master_guide": master_guide, 
                "guide_list": guide_connector_list, 
                "scale": module_path.guide_scale, 
                "joints": [], 
                "side": module_path.side, 
                "guide_connectors": guide_connector_list, 
                "systems_to_connect": systems_to_connect, 
                
            } # When it comes to joint creation I need to add ik/fk ctrl & 
            # joint list as well as rev_lovcators
            
            # add the temp dict to systems to be made, to manage all systems that eed to be constructed. 
            self.systems_to_be_made[master_guide] = temp_dictionary

            # if statement id add_hand.isChecked() on the ui later on. 
        
        # Reset the offset spin boxes to 0 to prepare for the necxt module adition
        self.ui.offset_Xaxes_spinbx.setValue(0)
        self.ui.offset_Yaxes_spinbx.setValue(0)
        self.ui.offset_Zaxes_spinbx.setValue(0)
        
        # clear the selection
        cmds.select(cl=1)
    
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

