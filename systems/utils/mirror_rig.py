import maya.cmds as cmds
import importlib
import os

from systems import joints
from systems.utils import utils

class mirror_data():
    def __init__(self, systems_to_be_made):
        self.data_to_be_checked = systems_to_be_made 
        self.mirror_data()
    
    def mirror_joints(self):
        # self.key is the key from the provided dict containing data on the module! 
        cmds.select(self.key["joints"][0])
        joint_list = cmds.mirrorJoint(mirrorYZ=1, mirrorBehavior=1, searchReplace=('_l', '_r'))
        return joint_list
        '''Data for the mirror class{
        'guide_root': {
        'module': 'root_basic', 
        'master_guide': 'guide_root', 
        'guide_list': ['crv_guide_COG'], 'scale': 1, 'joints': ['jnt_rig_root', 'jnt_rig_COG'], 
        'side': 'None', 
        'guide_connectors': ['crv_guide_COG'], 
        'systems_to_connect': [], 
        'ik_ctrl_list': [], 'fk_ctrl_list': [], 'ik_joint_list': [], 'fk_joint_list': []}, 

        'master_spine_basic_1': {
        'module': 'spine_basic', 
        'master_guide': 'master_spine_basic_1', 
        'guide_list': ['crv_guide_spine_5', 'crv_guide_spine_4', 'crv_guide_spine_3', 'crv_guide_spine_2', 'crv_guide_spine_1', 'crv_master_spine_basic_1'], 
        'scale': 1, 
        'joints': ['jnt_rig_spine_1', 'jnt_rig_spine_2', 'jnt_rig_spine_3', 'jnt_rig_spine_4', 'jnt_rig_spine_5'], 
        'side': 'None', 
        'guide_connectors': ['crv_guide_spine_5', 'crv_guide_spine_4', 'crv_guide_spine_3', 'crv_guide_spine_2', 'crv_guide_spine_1', 'crv_master_spine_basic_1'], 
        'systems_to_connect': ['guide_spine_1', 'guide_COG'], 
        'ik_ctrl_list': [], 'fk_ctrl_list': [], 'ik_joint_list': [], 'fk_joint_list': []}, 
        
        'master_biped_arm_l_1': {
        'module': 'biped_arm', 
        'master_guide': 'master_biped_arm_l_1', 
        'guide_list': ['crv_guide_wrist_l', 'crv_guide_elbow_l', 'crv_guide_shoulder_l', 'crv_guide_clavicle_l', 'crv_master_biped_arm_l_1'],
        'scale': 1, 
        'joints': ['jnt_rig_clavicle_l', 'jnt_rig_shoulder_l', 'jnt_rig_elbow_l', 'jnt_rig_wrist_l'], 
        'side': '_l', 
        'guide_connectors': ['crv_guide_wrist_l', 'crv_guide_elbow_l', 'crv_guide_shoulder_l', 'crv_guide_clavicle_l', 'crv_master_biped_arm_l_1'], 
        'systems_to_connect': ['guide_clavicle_l', 'guide_spine_4'], 
        'ik_ctrl_list': [], 'fk_ctrl_list': [], 'ik_joint_list': [], 'fk_joint_list': []}
        }'''

    def get_mirrored_side(self):
        if self.key["side"] == "_l":
            self.side = "_r"
            self.simple_side = "_r_"
        elif self.key["side"] == "_r":
            self.side = "_l"
            self.simple_side = "_l_"
        else:
            self.side = ""

    def get_mirrored_system_to_connect(self):
        systems_to_connect = self.key["systems_to_connect"]
        
        # I am looking for item with '_l' or '_r' & replace to opposite side
        # if the item has no side then it is the item needed to be parented to, 
        # so add it to the end of the 'mirrored_systems_to_connect' list.

        mirrored_systems_to_connect = [] 
        for item in systems_to_connect:
            if f"{self.key['side']}" in item:
                print(f"IF YES {self.key['side']} in {item} = @-A-@")
                mirrored_item = item.replace(f"{self.key['side']}", self.side, 1)
                print(f"if 'side' in item: {mirrored_item}")
            else:
                print(f"IF NOT {self.key['side']} in {item} = @-B-@")
                item_not_mirrored = item
                print(f"else: {item_not_mirrored}")
        mirrored_systems_to_connect.append(mirrored_item)
        mirrored_systems_to_connect.append(item_not_mirrored)
        print(f"Mirrored system to connect: {mirrored_systems_to_connect}")
        
        return mirrored_systems_to_connect
    
    def create_mirrored_guides(self): # create guide locators
        for jnt in self.joint_list:
            # Remove joint type prefix & create temp joint name
            for type in ["jnt_rig_", "jnt_ik_", "jnt_fk_"]:
                if type in jnt:
                    tmp_jnt = jnt.replace(type, "")
            # create locator at pos of jnt list 
            locator_name = cmds.spaceLocator(n=tmp_jnt)
            cmds.matchTransform(locator_name, jnt)
            # Add locators to locator list & reverse it
            self.locator_list.append(locator_name[0])
        self.locator_list.reverse()
        # Parent each locaotr to the next in the list
        for locator in range(len(self.locator_list)):
            try:
                cmds.parent(self.locator_list[locator], self.locator_list[locator+1])
            except: # operation contiues after even after trying to parent the last locator
                pass


    def create_mirrored_master_guide(self): # Create master guide
        split_master_guide = self.key["master_guide"].split("_")
        # change the side to the opposite one!
        master_guide = self.key["master_guide"].replace(f"_{split_master_guide[-2]}_",self.simple_side)
        self.proxy_obj_list = self.locator_list
        # create locator in master guide pos & parent the locaor's parent to it
        if "master" in master_guide:
            cmds.spaceLocator(n=master_guide)
            cmds.matchTransform(master_guide, self.joint_list[0])
            cmds.parent(self.locator_list[-1], master_guide)
            
            self.proxy_obj_list.append(master_guide)
        return master_guide


    def copy_mirrored_attrs(self): # copy attrs across
        self.non_proxy_attr_list = []
        for attr in cmds.listAttr(self.key["master_guide"], r=1, ud=1):
            if "_control_shape" in attr:
                pass
            else:
                try:
                    if attr == "master_guide":
                        cmds.addAttr(self.proxy_obj_list, ln="master_guide", at="enum", en=self.master_guide, k=0)
                    elif attr not in ['visibility', 'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ']:
                        try:
                            new_attr_name = attr.replace(f"{self.key['side']}_", self.simple_side)
                        except:
                            pass
                        cmds.addAttr(self.proxy_obj_list,ln=f"{new_attr_name}", proxy=f"{self.key['master_guide']}.{attr}")
                except:
                    pass
        # replace side with opposite for the attr & guide names. 
        print(f"Within 'copy_mirrored_attrs' the key is: ", self.key["guide_list"])
        for guide in self.key["guide_list"]:
            for attr in cmds.listAttr(guide, r=1, ud=1):
                if "_control_shape" in attr:
                    new_attr_name = attr.replace(f"{self.key['side']}_", self.simple_side)
                    mirror_guide = guide.replace(f"{self.key['side']}_", self.simple_side)
                    enum_value = cmds.getAttr(f"{guide}.{attr}", asString=1)
                    # Then add the attr to mirrored guide!
                    cmds.addAttr(mirror_guide, ln=f"{new_attr_name}", at="enum", en=enum_value)
        
    
    def mirror_data(self):
        # guide_pref = f"guide_{number_id}"
        otherSide_systems_to_be_made = {}
        # For loop to iterate through the keys in 'self.data_to_be_made'
        for key in self.data_to_be_checked.values():
            self.locator_list = []
            # Gather mirror_jnts attrib on each guide!
            mirror_attr_name = f"{key['master_guide']}.{key['master_guide']}_mirror_jnts"
            mirror_attribute = cmds.getAttr(mirror_attr_name, asString=1 )
            print(f"mirror attributes: {mirror_attribute} found on '{mirror_attr_name}'")

            if mirror_attribute == "Yes": # Yes mirror joint
                # Call the other functions
                self.key = key
                print(f"key is this:  {self.key}")
                self.joint_list = self.mirror_joints()
                self.get_mirrored_side()
                self.mirrored_system_to_connect = self.get_mirrored_system_to_connect()
                # 'systems_to_connect': ['guide_COG'] is wrong & should be ['guide_clavicle_r', 'guide_COG'] from ['guide_clavicle_l', 'guide_COG']

                self.create_mirrored_guides()
                self.master_guide = self.create_mirrored_master_guide()
                self.copy_mirrored_attrs() # to copy attributes across - to what tho, the joints? no probaly the mirrored guides

                # create temp dict to store same module data as 'add_module() from ui.py'
                temp_dictionary = {
                    "module": key["module"], 
                    "master_guide": self.master_guide,
                    "guide_list": self.locator_list,
                    "guide_scale": key["guide_scale"],
                    "joints": self.joint_list,
                    "side": self.side,
                    "guide_connectors": [],
                    "systems_to_connect": self.mirrored_system_to_connect, 
                    "ik_ctrl_list": [],
                    "fk_ctrl_list": [],
                    "ik_joint_list": [],
                    "fk_joint_list": []
                }

                # Assign the temp dict to 'otherSide_systems_to_be_made' w 'self.master_guide'
                # as the key!
                otherSide_systems_to_be_made[self.master_guide] = temp_dictionary
                print("***Data for the mirror class > ", otherSide_systems_to_be_made)
                # set attribute on mirrored master guides! 

        # Update the 'data_to_be_made' dict with this new data
        self.data_to_be_checked.update(otherSide_systems_to_be_made)
        print(f"Data for the mirror class{self.data_to_be_checked}")
        
    def get_mirror_data(self):
        return self.data_to_be_checked




