
import maya.cmds as cmds
import importlib

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
        if rig_type == "IKFK":
            # self.space_space_locators = self.create_locators() # swappos locators!
            loc_master_list = self.create_locators(self.master_space_name) # ['swappos_world_biped_arm_0_L', 
            # 'swappos_COG_biped_arm_0_L', 'swappos_shoulder_biped_arm_0_L', 'swappos_custom_biped_arm_0_L']

            print(f"loc_master_list is : {loc_master_list}")
            #loc_pv_list = self.create_locators(self.pv_space_names)
            #loc_top_list = self.create_locators(self.top_space_names)
            self.master_space_ctrl = [item for item in self.ik_ctrl_list if 'wrist' in item or 'ankle' in item][0]
            self.pv_ctrl = [item for item in self.ik_ctrl_list if 'pv' in item][0]
            self.top_ctrl = [item for item in self.ik_ctrl_list if 'shoulder' in item or 'hip' in item or 'scapula' in item][0]
            
            
            self.match_and_parent_to_ctrl(loc_master_list, self.master_space_ctrl)
        
    # might need to create temporary ctrl_root to work as the inverse_matrix. 
    def create_locators(self, space_loc_names):
       # created_loc_list = [cmds.spaceLocator(n=f"loc_swappos{x}")[0] 
       #                     for x in self.guide_list[6:] for item in self.space_space_list_names if item in x] 
        custom_loc_name_id = f"{self.key['module']}_{int(self.key['guide_number'])}{self.key['side']}"
        print(f"swappos names: {custom_loc_name_id}")
        created_loc_list = []
        print(f"loc names: {space_loc_names}")
        for item in space_loc_names:
            print(f"CREATED LOCATOR:  {item}")
            created_loc_list.append(cmds.spaceLocator(n=f"swappos_{item}_{custom_loc_name_id}")[0])
        return created_loc_list
                

    def cr_attr(self):
        pass

    # from the created locator list parent to location. 
    # Locators are matched to the same control, like pv or master_ctrl, 
    # then parented to dpaceswap like root, cog...
    def match_and_parent_to_ctrl(self, locator_ls, ctrl):
        for loc in locator_ls:
            print(f"match : {loc} to {ctrl}")
            cmds.matchTransform(loc, ctrl)
            
            '''
            if "COG" in loc:
                print(f"found COG in locator list > {loc}")
                cmds.parent(loc, self.ctrl_cog)
            elif "world" in loc:
                print(f"found world in loc list > {loc}")
                cmds.parent(loc, self.ctrl_root)
            elif f"{loc[10:-2]}" in loc:
                cmds.parent(loc, self.top_ctrl)
            '''

                
                




    def get_loc(self):
        pass


    def blend_matrix(self):
        pass

