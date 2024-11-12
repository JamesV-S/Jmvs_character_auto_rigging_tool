
import maya.cmds as cmds
from maya import OpenMayaUI as omui

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from shiboken6 import wrapInstance
from PySide6 import QtUiTools, QtWidgets, QtCore
from functools import partial # if you want to include args with UI method calls                   


import os.path
import importlib
import sys
import subprocess
import platform

from systems import (
    create_guides,
    joints, 
    fk, 
    ik, 
    squash_stretch    
)

from systems.utils import (
    connect_modules,
    mdl_foll_connection,
    utils, 
    mirror_rig,
    guide_data,
    arrow_ctrl,
    ikfk_switch, 
    space_swap,
    OPM,
    neck_twistBend_sys
)

# Reload Modules
importlib.reload(create_guides)
importlib.reload(joints)
importlib.reload(connect_modules)
importlib.reload(utils)
importlib.reload(mirror_rig)
importlib.reload(guide_data)
importlib.reload(fk)
importlib.reload(ik)
importlib.reload(arrow_ctrl)
importlib.reload(ikfk_switch)
importlib.reload(squash_stretch)
importlib.reload(space_swap)
importlib.reload(OPM)
importlib.reload(mdl_foll_connection)
importlib.reload(neck_twistBend_sys)

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

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
        
        # self.update_d
        self.update_dropdown() # add available modules to the ddbox on ui
        self.module_created = 0
        self.created_guides = []
        self.systems_to_be_made = {}
        self.init_existing_module()

        #self.ui.hand_module_btn.clicked.connect(self.temp_hand_func)
        # Tab 1 - RIG
        # if biped_finger is the chosen then enable the finger number ddbox
        self.ui.neck_num_SpinBox.setMinimum(3)
        # self.ui.neck_num_SpinBox.setDisabled(True)
        # self.ui.neck_num_lbl.setDisabled(True)
        
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
        tab1_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "interface","logo_cog.jpeg")
        self.ui.image_lbl.setPixmap(QPixmap(tab1_image_path))

        self.ui.add_mdl_btn.clicked.connect(self.add_module)
        self.ui.remove_mdl_btn.clicked.connect(self.remove_module)
        self.ui.orientation_ddbox.currentIndexChanged.connect(self.orientation_func)
        self.ui.build_skeleton_btn.clicked.connect(self.create_joints)
        self.ui.Create_systems_btn.clicked.connect(self.create_rig)
        
        # Tab 2 - SKINNING
        tab2_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "interface","skinning_symbol.png")
        self.ui.skinning_image_lbl.setPixmap(QPixmap(tab2_image_path))
        # Tab 3 - CURVE HELPER

        # Tab 4 - OUTPUT OPTIONS(export)

    # functions, connected to above commands   
    def initUI(self):
        loader = QUiLoader()
        UI_VERSION = "003"
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


    def orientation_func(self):
        clicked_orientation = self.ui.orientation_ddbox.currentText()
        if clicked_orientation == 'xyz':
            self.orientation = "XYZ"
        elif clicked_orientation == 'yzx':
            self.orientation = "YZX"
        print("ORIENTATION CLICKED IS: ",  self.orientation)
        return self.orientation


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


    def init_existing_module(self):
        temp_dict = guide_data.init_data()
        for dict in temp_dict.values():
            master_guide = dict["master_guide"]
            self.created_guides.append(master_guide)
            print(f"guide_data, created_guides == {self.created_guides}")
            self.systems_to_be_made[master_guide] = dict
            if not dict["space_swap"] == []:
                if 'arm' in dict['module']:
                    sublist = [dict["space_swap"][0:4], dict["space_swap"][4:6], dict["space_swap"][6:8], dict["space_swap"][8:10]]
                else:
                    sublist = [dict["space_swap"][0:4], dict["space_swap"][4:6], dict["space_swap"][6:8]]
                print(f"OLD space_swap key: {dict['space_swap']}")
                dict.update({"space_swap": sublist})
                print(f"updated space_swap key: {dict['space_swap']}")


    def add_module(self):
        # Get the selected module from the UI
        module = self.ui.module_picker_ddbox.currentText()
        
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                     "systems", "modules"))
        # you are calling the import_module function from the importlib module
        module_path = importlib.import_module(module)
        importlib.reload(module_path)
        
        #----------------------------------------------------------------------
        print("existing MODULE", module," ///// ","module_path: ", module_path, "print from ui in add_module()" )
        
        # Search for existing modules of the same type in the scene

        # if module has no side : f"master_*_{module}"
        if "spine" in module:
            existing_guides = cmds.ls(f"master_*_{module}")
            #print("existing_guides without 'side': spine, tail, neck")
        else:
            existing_guides = cmds.ls(f"master_*_{module}_*")
            #print("existing_guides with 'side': arm, leg")
            
        #existing_guides = cmds.ls(f"master_*_{module}_*")
        existing_ids = []
        
        # Extract unique IDs from existing guides
        for guide in existing_guides:
            parts = guide.split('_')
            if len(parts) > 2 and parts[1].isdigit():
                existing_ids.append(int(parts[1]))
     
        # Determine the next unique ID 
        if existing_ids:
            self.unique_id_counter = max(existing_ids) + 1
        else:
            self.unique_id_counter = 0 
        
        # Number bueprint id
        self.numb_id = self.unique_id_counter
        print(f"Assigned unique ID: {self.numb_id}")
        
        self.neck_jnt_num = self.ui.neck_num_SpinBox.value()
        print(f"NECK module: {self.neck_jnt_num}")
        if 'neck' in module:
            offsetY = 10
            if self.neck_jnt_num > 3:
                
                module_path.system = [f"neck_{i}" for i in range(self.neck_jnt_num)]
                
                for i in range(3, self.neck_jnt_num):
                    last_pos = module_path.system_pos_xyz[f"neck_{i-1}"]
                    # X orientation
                    # add new postion with the offset on Y axis!. 
                    module_path.system_pos_xyz[f"neck_{i}"] = [last_pos[0], last_pos[1]+offsetY, last_pos[2]]
                    # Rotation is the same :
                    module_path.system_rot_xyz[f"neck_{i}"] = module_path.system_rot_xyz[f"neck_{i-1}"]
                    
                    # Y orientation
                    module_path.system_pos_yzx[f"neck_{i}"] = [last_pos[0], last_pos[1]+offsetY, last_pos[2]]
                    module_path.system_rot_yzx[f"neck_{i}"] = module_path.system_rot_yzx[f"neck_{i-1}"]
                    
            neck_sys_dict = {
                "nck_sys": module_path.system, 
                "nck_pos_xyz": module_path.system_pos_xyz, 
                "nck_rot_xyz": module_path.system_rot_xyz, 
                "nck_pos_yzx": module_path.system_pos_yzx, 
                "nck_rot_yzx": module_path.system_rot_yzx
                }     
            guides = create_guides.Guides_class(module, module_path.side, to_connect_to=[], 
                use_existing_attr=[], orientation=self.orientation_func(), numb_id=self.numb_id, neck_dict=neck_sys_dict)
        else:    
            guides = create_guides.Guides_class(module, module_path.side, to_connect_to=[], 
                use_existing_attr=[], orientation=self.orientation_func(), numb_id=self.numb_id)
        guide = guides.collect_guides()
        
        print(f"GUIIDE RETURNED DICT: {guide}")
        # If guides are succesfully created, this extracts important elements like these:
        if guide:
            master_guide =  guide["master_guide"] # guide["master_guide"] - f"master_{guide_number}_{module}"
            guide_connector_list = guide["guide_connector_list"]
            systems_to_connect = guide["system_to_connect"]
            guide_list = guide["ui_guide_list"]
            data_guide = guide["data_guide"]
            number_int = guide["guide_number"]
            
            # Append the 'master_guide' to a list of created guides 
            self.created_guides.append(master_guide)
            print(f"ADD_MODULE, created_guides == {self.created_guides}")
            # create a temp dict to store details abt the module and its guides... 
            
            temp_dictionary = {
                "module": module, 
                "master_guide": master_guide, 
                "guide_list": guide_list, 
                "guide_scale": module_path.guide_scale, 
                "joints": [], 
                "side": module_path.side, 
                "guide_connectors": guide_connector_list, 
                "systems_to_connect": systems_to_connect,
                "ik_ctrl_list": [],
                "fk_ctrl_list": [],
                "ik_joint_list": [],
                "fk_joint_list": [],
                "space_swap": module_path.space_swapping,
                "mdl_switch_ctrl_list": [],
                "guide_number": number_int
            }

            # add the temp dict to systems to be made, to manage all systems that eed to be constructed. 
            self.systems_to_be_made[master_guide] = temp_dictionary
            print(f"temp dict for setup: {temp_dictionary}")
            print(f">>>>>>>>>>>>>>>>>>>>>>>> self.systems_to_be_made = {self.systems_to_be_made}")
            # Add the attributes to the data locator!
            guide_data.setup(temp_dictionary, data_guide)


    def remove_module(self):
        module = cmds.ls(sl=1)
        for key in list(self.systems_to_be_made.values()):
            print(f"remove module 'key' : {key}")
            if module[0] in key['master_guide']:
                self.systems_to_be_made.pop(module[0])
                self.created_guides.remove(module[0])
                cmds.delete(module[0], key['guide_connectors'])


    def temp_hand_func(self):
        print("button hand!!!!!!!!!")
    

    def create_joints(self):
        # master_guides: ['guide_root', 'master_biped_arm_l_1']
        print(f"The systems to be made are:>> {self.systems_to_be_made}")
        
        rig_jnt_list = joints.get_joint_list(self.created_guides, system="rig")
             
        # adding the joint list to the dictionary
        num = 0
        for key in self.systems_to_be_made.values():
            key["joints"] = rig_jnt_list[num]
            num += 1
        
        mirror_module = mirror_rig.mirror_data(self.systems_to_be_made, self.orientation_func())
        self.systems_to_be_made = mirror_module.get_mirror_data()
        
        connect_modules.attach_jnts(self.systems_to_be_made, system="rig")
       
        #self.hide_guides()

    
    def create_rig(self):
        # gather master_guide, rig_type = ikfk, (don't need orientation tbh - but u never know)
        self.neck_jnt_num = self.ui.neck_num_SpinBox.value()
        print(f"NECK amount value: {self.neck_jnt_num}")
        for key in self.systems_to_be_made.values():
            pass
            master_guide = key['master_guide']
            rig_type = cmds.getAttr(f"{master_guide}.{master_guide}_rig_type", asString=1) # name of master_guide
            orientation = self.orientation_func() # Upper case: XYZ not xyz

            # Import the current module used 
            sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                        "systems", "modules"))
            # you are calling the import_module function from the importlib module
            module = importlib.import_module(key["module"])
            importlib.reload(module)

            if key["module"] == "root_basic": 
                CTRL_ROOT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "systems", 
                                        "imports","ctrl_root_import.abc")
                root_imp = cmds.file(CTRL_ROOT_FILE, i=1, namespace="imp_root", rnn=1)
                cmds.scale(1, 1, 1, root_imp)
                self.ctrl_root = cmds.rename(root_imp[0], f"ctrl_root")
                cmds.matchTransform(self.ctrl_root, key["guide_list"][1],  pos=1, rot=0, scl=0)
                utils.colour_root_control(self.ctrl_root)

                # If root module, create cog_ctrl. TO be used in ikfk switch & space_swap: 
                COG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "systems", 
                                        "imports","cog_ctrl_import.abc")
                imported = cmds.file(COG_FILE, i=1, namespace="imp_cog", rnn=1)
                cmds.scale(1, 1, 1, imported)
                self.ctrl_cog = cmds.rename(imported[0], f"ctrl_COG")
                cmds.matchTransform(self.ctrl_cog, key["guide_list"][0],  pos=1, rot=0, scl=0)
                cmds.setAttr(f"{self.ctrl_cog}.overrideEnabled", 1)
                cmds.setAttr(f"{self.ctrl_cog}.overrideColor", 18)
                cmds.parent(self.ctrl_cog, self.ctrl_root)
                OPM.OpmCleanTool(self.ctrl_cog)
                key.update({"mdl_switch_ctrl_list": self.ctrl_cog})
    
                # 'joints': ['jnt_rig_0_root', 'jnt_rig_0_COG']
                cmds.parentConstraint(self.ctrl_root, key['joints'][0])
                cmds.parentConstraint(self.ctrl_cog, key['joints'][1])

            elif key["module"] == "neck_head":
                if rig_type == "FK":
                    print(f"IN NECK module: {self.neck_jnt_num}")
                    fk_neck_sys = neck_twistBend_sys.neck_sys(
                        guide_list=key["guide_list"], jnt_rig_list=key["joints"], 
                        neck_amount=self.neck_jnt_num, orientation=self.orientation_func())
                    # fk_ctrls = fk_neck_sys.get_ctrls()
            else:
                if rig_type == "FK":
                    # create fk joints, system & control, then constrain to rig_joints!
                    print(f"Build 'fk' joints! {master_guide}")
                    fk_joint_list = joints.joint(master_guide, system="fk")
                    fk_module = fk.create_fk_sys( key["module"], fk_joint_list, master_guide, 
                                                 key['guide_scale'], delete_end=0)
                    fk_ctrls = fk_module.get_ctrls()
                    print(f"list 1: {fk_joint_list}, list 2: {key['joints']}")
                    utils.constraint_from_lists_1to1(fk_joint_list, key["joints"],mo=1)
                    key.update({"fk_joint_list": fk_joint_list, "fk_ctrl_list": fk_ctrls})
                    # ------------------
                    # ikfk blend arrow ctrl or COG 
                    mdl_switch_ctrl = arrow_ctrl.cr_arrow_control(
                        module_name=key['module'], master_guide=key['master_guide'], 
                        side=key['side']
                        )
                    key.update({"mdl_switch_ctrl_list": mdl_switch_ctrl})
                    print("looking for update::::::::::::::::::::::: ", key)
                elif rig_type == "IK":
                    print(f"Build 'ik' joints! {master_guide}")
                    ik_joint_list = joints.joint(master_guide, system="ik")
                    ik_module = ik.create_ik_sys(key["module"], ik_joint_list, master_guide, 
                                                 key['guide_scale'], module.ik_joints)
                    ik_ctrls = ik_module.get_ctrls()
                    utils.constraint_from_lists_1to1(ik_joint_list, key["joints"],mo=1)
                    key.update({"ik_joint_list": ik_joint_list, "ik_ctrl_list": ik_ctrls})
                    # ------------------
                    # ikfk blend arrow ctrl or COG 
                    mdl_switch_ctrl = arrow_ctrl.cr_arrow_control(
                        module_name=key['module'], master_guide=key['master_guide'], 
                        side=key['side']
                        )
                    key.update({"mdl_switch_ctrl_list": mdl_switch_ctrl})
                    print("looking for update::::::::::::::::::::::: ", key)
                    
                elif rig_type == "IKFK":
                    
                    print(f"Build 'ikfk' joints! {master_guide}")
                    fk_joint_list = joints.joint(master_guide, system="fk")
                    fk_module = fk.create_fk_sys( key["module"], fk_joint_list, master_guide, 
                                                 key['guide_scale'], delete_end=0)
                    fk_ctrls = fk_module.get_ctrls()

                    ik_joint_list = joints.joint(master_guide, system="ik")
                    ik_module = ik.create_ik_sys(key["module"], ik_joint_list, master_guide, 
                                                 key['guide_scale'], module.ik_joints)
                    ik_ctrls = ik_module.get_ctrls()
            
                    utils.constraint_from_lists_2to1(fk_joint_list, ik_joint_list, key["joints"] ,mo=1)
                    key.update({"fk_joint_list": fk_joint_list, "fk_ctrl_list": fk_ctrls})
                    key.update({"ik_joint_list": ik_joint_list, "ik_ctrl_list": ik_ctrls})
                    # ------------------
                    # ikfk blend arrow ctrl or COG 
                    mdl_switch_ctrl = arrow_ctrl.cr_arrow_control(
                        module_name=key['module'], master_guide=key['master_guide'], 
                        side=key['side']
                        )
                    key.update({"mdl_switch_ctrl_list": mdl_switch_ctrl})
                    print("looking for update::::::::::::::::::::::: ", key)
                    # ------------------
                    # ikfk blend system
                    ikfk_switch.cr_ikfk_switch_sys(
                        rig_joints=key["joints"], mdl_switch_ctrl=mdl_switch_ctrl,
                        fk_ctrls=fk_ctrls, ik_ctrls=ik_ctrls, fk_joint_list=key['fk_joint_list'], 
                        ik_joint_list=key['ik_joint_list'], master_guide=master_guide)

                else:
                    cmds.error(f"Fat ERROR: 'rig_type' attr cannot be found!")
                
                # get stretch & squash attr & add system if 'Yes'
                if rig_type == "IKFK" or rig_type == "IK":
                    squash_stretch_attr = cmds.getAttr(
                        f"{master_guide}.{master_guide}_squash_stretch", asString=1
                        )
                    if squash_stretch_attr == "Yes":
                        # call squash & stretch system!
                        print(f"Build squahs_stretch system! {master_guide}")
                        squash_stretch_instance = []
                        squash_stretch.cr_squash_stretch(key, module.ik_joints, rig_type)
                
                '''system_group.grpSetup(self.ui.rig_master_name.text())''' # What does this do?
        
        for key in self.systems_to_be_made.values():
            if "root" in key["module"]:
                pass
            elif "spine" in key["module"]:
                print("This module is SPINE")
                cmds.parent(key["fk_ctrl_list"][-1], "ctrl_COG")
                OPM.OpmCleanTool(key["fk_ctrl_list"][-1])
            else:
                print(f"YEEEEAH >> follow connection for: {key['module']}")
                print(f"Fol_connections: mdl = {key['module']}  > sys_to_connect = {key['systems_to_connect']}" )
                # mdl_foll_connection.connecting_sys_to_connect(key["module"], key["systems_to_connect"], self.ctrl_root, key["side"])

        # Connect systems & add space_swapping!
        for key in self.systems_to_be_made.values():
            updated_rig_type = cmds.getAttr(f"{key['master_guide']}.{key['master_guide']}_rig_type", asString=1)
            if key["systems_to_connect"]:
                #print(f"connect modules after systems! {master_guide}")
                systems_to_connect = key["systems_to_connect"]
                # connect_modules.connect_polished(systems_to_connect)
            if updated_rig_type == "IKFK" or updated_rig_type == "IK":
                #print(f"Add space_swap sys {master_guide}")
                print(f"before calling spaceSwap: {key}")
                space_swap_mdl = space_swap.cr_spaceSwapping(key, self.ctrl_cog, self.ctrl_root)
        '''
        for key in self.systems_to_be_made.values():
            if "root" in key["module"]:
                pass
            elif "L" in key["side"]:
                print(f"Should be > Arm or leg: {key['module']}, > fk_ctrls: {key['fk_ctrl_list']},  ik_ctrls: {key['ik_ctrl_list']}, > MAKE RED")
            elif "R" in key["side"]:
                print(f"Should be > Arm or leg: {key['module']}, > fk_ctrls: {key['fk_ctrl_list']},  ik_ctrls: {key['ik_ctrl_list']}, > MAKE BLUE")
            elif None in key["side"]:
                print(f"Should be > spine: {key['module']}, > fk_ctrls: {key['fk_ctrl_list']},  ik_ctrls: {key['ik_ctrl_list']}, > MAKE YELLOW")
        
        # colour the controls: 
        colour_dict = {"L_colour":[], "C_colour":[], "R_colour":[]} # C stands for centre so yellow. 
        
        ctrl_list = cmds.ls("ctrl_*", type="transform")
        utils.colour_conrols(ctrl_list, colour_dict)
        cmds.select(cl=1)
        '''

    def polish_rig(self):
        pass

    def hide_guides(self):
        for key in self.systems_to_be_made.values():
            cmds.hide(key["master_guide"])
        cmds.hide("grp_guideConnector_clusters")

def main():
    ui = QtSampler()
    ui.show()
    return ui