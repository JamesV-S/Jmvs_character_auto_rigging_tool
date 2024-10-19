
import maya.cmds as cmds
import importlib
import re
import maya.api.OpenMaya as om

from systems.utils import (utils)

importlib.reload(utils)

# space_swap for 3 things: 

class cr_spaceSwapping():
    def __init__(self, key, ctrl_cog, ctrl_root):
        self.key = key
        self.ctrl_cog = ctrl_cog
        self.ctrl_root = ctrl_root
        self.space_space_list_names = self.key["space_swap"]
        self.master_space_name = self.space_space_list_names[0]
        self.pv_space_names = self.space_space_list_names[1]
        self.top_space_names = self.space_space_list_names[2]
        
        print(f"master; {self.master_space_name}, pv; {self.pv_space_names}, top; {self.top_space_names}")

        # self.guide_list = self.key["guide_list"]
        self.ik_ctrl_list = self.key["ik_ctrl_list"]
        
        rig_type = cmds.getAttr(f"{self.key['master_guide']}.{self.key['master_guide']}_rig_type", asString=1)
        if rig_type == "IKFK" or rig_type == "IK":
            # self.space_space_locators = self.create_locators() # swappos locators!
            loc_master_list = self.create_locators(self.master_space_name) # ['swappos_world_biped_arm_0_L', 
            # 'swappos_COG_biped_arm_0_L', 'swappos_shoulder_biped_arm_0_L', 'swappos_custom_biped_arm_0_L']

            print(f"loc_master_list is : {loc_master_list}")
            loc_pv_list = self.create_locators(self.pv_space_names)
            loc_top_list = self.create_locators(self.top_space_names)

            self.master_space_ctrl = [item for item in self.ik_ctrl_list if 'wrist' in item or 'ankle' in item][0]
            self.pv_ctrl = [item for item in self.ik_ctrl_list if 'pv' in item][0]
            self.top_ctrl = [item for item in self.ik_ctrl_list if 'shoulder' in item or 'hip' in item or 'scapula' in item][0]
                        
            self.match_and_parent_to_ctrl(loc_master_list, self.master_space_ctrl)
            self.match_and_parent_to_ctrl(loc_pv_list, self.pv_ctrl)
            self.match_and_parent_to_ctrl(loc_top_list, self.top_ctrl)
        

    def create_locators(self, space_loc_names):
        self.custom_loc_name_id = f"{self.key['module']}_{int(self.key['guide_number'])}{self.key['side']}"
        print(f"swappos names: {self.custom_loc_name_id}")
        created_loc_list = []
        print(f"loc names: {space_loc_names}")
        for item in space_loc_names:
            locator_name = f"swappos_{item}_{self.custom_loc_name_id}"
            if not cmds.objExists(locator_name):
                created_loc_list.append(cmds.spaceLocator(n=locator_name)[0])
        return created_loc_list
                

    def cr_attr(self):
        pass

    # from the created locator list parent to location. 
    # Locators are matched to the same control, like pv or master_ctrl, 
    # then parented to dpaceswap like root, cog...
    def match_and_parent_to_ctrl(self, locator_ls, ctrl):
        for loc in locator_ls:
            cmds.setAttr(f"{loc}.overrideEnabled", 1)
            cmds.setAttr(f"{loc}.overrideColor", 14)
            print(f"match : {loc} to {ctrl}")
            cmds.matchTransform(loc, ctrl)
            
            if "COG" in loc:
                print(f"found COG in locator list > {loc}")
                cmds.parent(loc, self.ctrl_cog)
            elif "world" in loc or "custom" in loc:
                print(f"found world in loc list > {loc}")
                try: cmds.parent(loc, self.ctrl_root)
                except: pass
            elif "spine" in loc: 
                temp_spine_grp = cmds.group(loc, n=f"tmp_swappos_TOPLOC_{self.custom_loc_name_id}")
                cmds.parent(temp_spine_grp, self.ctrl_root)
                
                # Find out if there are any spine joints in the scene!
                spine_jnt_nm_pattern = re.compile(r"jnt_rig_\d+_spine_\d+")
                all_obj = cmds.ls()
                spine_jnts = [obj for obj in all_obj if spine_jnt_nm_pattern.match(obj)]
                print(spine_jnts)
                if spine_jnts:
                    # figure out which spine_joints are closest to the locator!
                    def get_position(obj_name):
                        return om.MVector(cmds.xform(obj_name, query=True, 
                                                     worldSpace=True, translation=True))
                    
                    def find_closest_joint(locator, joints):
                        locator_pos = get_position(locator)
                        return min(joints, key=lambda joint: (locator_pos - get_position(joint)).length())
                    
                    closest_joint = find_closest_joint(loc, spine_jnts)
                    print(f"The closest joint to {loc} is {closest_joint}")
                    
                    for jnt in spine_jnts:
                        print(jnt)
                    print("identified that this module has a spine module!")
                else:
                    print("did NOT IDNETIFY that this module has a spine module!")
                    # if the spine module doesn't exist, create temp grp for the top_locator to parent to,
                    # otherwise find the closest spine(connect to spine) joint & constrain the locator to it, 
                    
            else:
                id = loc.split('_')[1]
                print(f"id: {id}")
                print(f"ctrl_ik_{int(self.key['guide_number'])}_{id}{self.key['side']}")
                ik_ctrl = f"ctrl_ik_{int(self.key['guide_number'])}_{id}{self.key['side']}"
                cmds.parent(loc, ik_ctrl)
        # swappos_shoulder_biped_arm_0_L > ctrl_ik_0_#_L
        # id = swappos_shoulder_biped_arm_0_L.split('_')[1]
        # ik_ctrl = f"ctrl_ik_{int(self.key['guide_number'])}_shoulder{self.key['side']}"
        

     
    def get_loc(self):
        pass


    def cr_sys(self):
        pass

