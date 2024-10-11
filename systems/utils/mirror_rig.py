import maya.cmds as cmds
import importlib
import os

from systems import joints
from systems.utils import (utils, control_shape, guide_data)
importlib.reload(joints)
importlib.reload(utils)
importlib.reload(control_shape)
importlib.reload(guide_data)

class mirror_data():
    def __init__(self, systems_to_be_made):
        self.data_to_be_checked = systems_to_be_made 
        self.mirror_data()
    
    def get_mirrored_side(self):
        if self.key["side"] == "_L":
            self.side = "_R"
            #self.simple_side = "_r_"
        elif self.key["side"] == "_R":
            self.side = "_L"
            #self.simple_side = "_l_"
        else:
            self.side = ""

    def create_mirrored_guides(self): # create locators to act as guides for the mirrored side!
        GUIDE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  "..", "imports","guide_shape.abc")
        print(f"GUIDE SHAPE FILE : {GUIDE_FILE}")
        tmp_guide_list = []
        guide_connector_list = []

        for guide in self.key["guide_list"]:
            pos = cmds.xform(guide, r=1, ws=1, q=1, t=1)
            rot = cmds.xform(guide, r=1, ws=1, q=1, ro=1)

            if "master" in guide:
                guide_name = f"master_{guide[7:-2]}{self.side}" # master_0_biped_arm_L
                # Might have to include 'number_id' to update properly!
                imported_guide = control_shape.controlTypes(
                    guide_name, [5, 5, 5]).create_octagon() # f"master_{number_id}_{accessed_module}{side}"
                cmds.setAttr(f"{guide_name}.overrideEnabled", 1)
                cmds.setAttr(f"{guide_name}.overrideColor", 9)
                cmds.scale(8, 8, 8, guide_name)
            else:
                guide_name =  f"{guide[:-2]}{self.side}" # guide_0_shoulder_L remove '_L' & add '_R'
                tmp = cmds.file(GUIDE_FILE, i=1, namespace="guide_shape_import", rnn=1)
                cmds.scale(self.module.guide_scale+1, self.module.guide_scale+1, 
                            self.module.guide_scale+1, tmp)
                imported_guide = guide = cmds.rename(tmp[0], guide_name)
                utils.colour_guide_custom_shape(guide_name) #       shape_list = cmds.listRelatives(custom_crv, shapes=1)
                                                                    #                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                    # ValueError: No object matches name: guide_0_wrist_R
                

            cmds.xform(imported_guide, t=pos, ro=rot)
            tmp_guide_list.append(imported_guide)
        
        # this works to avoide mirroring transform issue
        grp_name = cmds.group(n="mirroring_transform", em=1)
        cmds.parent(tmp_guide_list, grp_name)
        cmds.xform(grp_name, scale=[-1, 1, 1])
        cmds.parent(tmp_guide_list, w=1)
        cmds.makeIdentity(tmp_guide_list[-1], apply=1, s=1)
        cmds.delete(grp_name)

        
        print(f"CONNECTING GUIDES Mirror : {tmp_guide_list}")
        for guide in range(len(tmp_guide_list)):
            try:
                cmds.parent(tmp_guide_list[guide], tmp_guide_list[guide+1])
                # create connectors:
                guide_connector = utils.guide_curve_connector(tmp_guide_list[guide], tmp_guide_list[guide+1])
                guide_connector_list.append(guide_connector)
            except:
                pass # ignore trying to parent last guide in the list
        
        if "grp_guideConnector_clusters" in cmds.ls("grp_guideConnector_clusters"):
            cmds.parent(guide_connector_list, "grp_guideConnector_clusters")
        else: 
            cmds.group(guide_connector_list, n="grp_guideConnector_clusters", w=1)
        cmds.select(cl=1)
        
        self.master_guide = tmp_guide_list[-1]
        self.guide_list = tmp_guide_list

        # Create the data guide for the mirrored side!
        if "root" in self.module.system: # or "proximal" in self.module.system:
            data_guide_name = f"data_{self.master_guide}"
        else:
            data_guide_name = self.master_guide.replace("master_", "data_")
        self.data_guide = cmds.spaceLocator(n=data_guide_name)[0]
        cmds.matchTransform(data_guide_name, self.master_guide)
        cmds.parent(data_guide_name, self.master_guide)

    
    def copy_mirrored_attrs(self): # copy attrs across
        self.non_proxy_attr_list = []
        proxy_obj_list = self.guide_list
        for attr in cmds.listAttr(self.key["master_guide"], r=1, ud=1):
            if "_control_shape" in attr:
                pass
            else:
                try:
                    if attr == "master_guide":
                        cmds.addAttr(proxy_obj_list, ln="master_guide", at="enum", en=self.master_guide, k=0)
                    elif attr not in ['visibility', 'translateX', 'translateY', 
                                      'translateZ', 'rotateX', 'rotateY', 
                                      'rotateZ', 'scaleX', 'scaleY', 'scaleZ']:
                        try:
                            new_attr_name = attr.replace(f"{self.key['side']}", self.side, 1)
                        except:
                            pass
                        cmds.addAttr(proxy_obj_list,ln=f"{new_attr_name}", proxy=f"{self.key['master_guide']}.{attr}")
                except:
                    pass
        # replace side with opposite for the attr & guide names. 
        print(f"Within 'copy_mirrored_attrs' the key is: ", self.key["guide_list"])
        for guide in self.key["guide_list"]:
            for attr in cmds.listAttr(guide, r=1, ud=1):
                if "_control_shape" in attr:
                    new_attr_name = attr.replace(f"{self.key['side']}", self.side)
                    mirrored_guide = guide.replace(f"{self.key['side']}", self.side)
                    enum_value = cmds.getAttr(f"{guide}.{attr}", asString=1)
                    # Then add the attr to mirrored guide!
                    cmds.addAttr(mirrored_guide, ln=f"{new_attr_name}", at="enum", en=enum_value)


    def mirror_joints(self):
        joint_list = joints.joint(top_skeleton_joint=self.master_guide, system="rig")
        # the 'self.master_guide' is the mirrored one
        return joint_list


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
        
    
    def mirror_data(self):
        # guide_pref = f"guide_{number_id}"
        temp_otherside_systems_to_be_made = {}
        # For loop to iterate through the keys in 'self.data_to_be_made'
        for key in self.data_to_be_checked.values():
            #self.locator_list = []
            accessed_module = key["module"]
            self.module = importlib.import_module(f"systems.modules.{accessed_module}")
            importlib.reload(self.module)
            # Gather mirror_jnts attrib on each guide!
            mirror_attribute = cmds.getAttr(
                f"{key['master_guide']}.{key['master_guide']}_mirror_jnts", 
                asString=1
            )

            if mirror_attribute == "Yes": # Yes mirror joint
                # Call the other functions
                self.key = key
                print(f"key is this:  {self.key}")                
                
                # Get the mirrored side 'R' or 'L'
                self.get_mirrored_side()
                # Create mirrored guides with custom shape including master_guide
                self.create_mirrored_guides()
                # Copy the attributes across too
                self.copy_mirrored_attrs()
                
                # Test if i should do this: 
                self.joint_list = self.mirror_joints()
                
                self.mirrored_system_to_connect = self.get_mirrored_system_to_connect()
                # 'systems_to_connect': ['guide_COG'] is wrong & should be ['guide_clavicle_r', 'guide_COG'] from ['guide_clavicle_l', 'guide_COG']

                # create temp dict to store same module data as 'add_module() from ui.py'
                temp_dictionary = {
                    "module": key["module"], 
                    "master_guide": self.master_guide,
                    "guide_list": self.guide_list,
                    "guide_scale": key["guide_scale"],
                    "joints": self.joint_list, # Test if i should use this. Probbly need it.
                    "side": self.side,
                    "guide_connectors": [],
                    "systems_to_connect": self.mirrored_system_to_connect, 
                    "ik_ctrl_list": [],
                    "fk_ctrl_list": [],
                    "ik_joint_list": [],
                    "fk_joint_list": [] # Might have to include 'number_id' to update properly!
                }


                # Assign the temp dict to 'otherSide_systems_to_be_made' w 'self.master_guide'
                # as the key!
                temp_otherside_systems_to_be_made[self.master_guide] = temp_dictionary
                print("***Data for the mirror class > ", temp_otherside_systems_to_be_made)
                # set attribute on mirrored master guides! 
                cmds.setAttr(
                f"{key['master_guide']}.{key['master_guide']}_mirror_jnts", 0
                )


        # Update the 'data_to_be_made' dict with this new data
        self.data_to_be_checked.update(temp_otherside_systems_to_be_made)
        print(f"Data for the mirror class{self.data_to_be_checked}")
        
        if mirror_attribute == "Yes":
            guide_data.setup(temp_dictionary, self.data_guide)
        
    def get_mirror_data(self):
        return self.data_to_be_checked




