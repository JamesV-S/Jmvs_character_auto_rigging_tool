
import maya.cmds as cmds
import importlib

from systems.utils import (utils)

importlib.reload(utils)

# space_swap for 3 things: 

class cr_spaceSwapping():
    def __init__(self, key, ctrl_cog, ctrl_root, ):
        self.key = key
        self.ctrl_cog = ctrl_cog
        self.ctrl_root = ctrl_root
        ''' atm it's just locators for the hand, need a list of locators for the pv & shoulder/hip '''
        self.locator_list = self.key["space_swap"]
        
        # self.locator_dict = 

        self.guide_list = self.key["guide_list"]
        self.ik_ctrl_list = self.key["ik_ctrl_list"]

        rig_type = cmds.getAttr(f"{self.key['master_guide']}.{self.key['master_guide']}_rig_type", asString=1)
        if rig_type == "IKFK":
            self.space_swap_locators = self.create_locators()
            print(self.space_swap_locators)
            self.pv_ctrl = [item for item in self.ik_ctrl_list if 'pv' in item][0]
            self.master_swap_ctrl = [item for item in self.ik_ctrl_list if 'wrist' in item or 'ankle' in item][0]
            self.top_ctrl = [item for item in self.ik_ctrl_list if 'shoulder' in item or 'hip' in item or 'scapula' in item][0]
            
            print(f"top_joint : {self.top_ctrl}")

            self.parent_to_location()
        

    # might need to create temporary ctrl_root to work as the inverse_matrix. 
    def create_locators(self):
       # created_loc_list = [cmds.spaceLocator(n=f"loc_swappos{x}")[0] 
       #                     for x in self.guide_list[6:] for item in self.locator_list if item in x] 
        custom_loc_name_id = f"{self.key['module']}_{int(self.key['guide_number'])}{self.key['side']}"
        print(f"swappos names: {custom_loc_name_id}")
        created_loc_list = []
        for item in self.locator_list:
            created_loc_list.append(cmds.spaceLocator(n=f"swappos_{item}_{custom_loc_name_id}")[0])
        
        '''
        tmp_list = []
        for x in self.locator_list:
            for item in ["root", "COG"]:
                if item in x:
                    tmp_list.append(cmds.spaceLocator(n=f"swappos_{item}_#")[0])
        '''

        if "custom" in self.locator_list:
            loc = cmds.spaceLocator(n="swappos_custom_#")[0]
            created_loc_list.append(loc)
            self.custom_loc = loc
        return created_loc_list
        

    def cr_attr(self):
        pass

    # from the created locator list parent to location. 
    # Locators are matched to the same control, like pv or master_ctrl, 
    # then parented to dpaceswap like root, cog...
    def parent_to_location(self):
        # ['swappos_world_biped_arm_0_L', 'swappos_COG_biped_arm_0_L', 'swappos_shoulder_biped_arm_0_L', 'swappos_custom_biped_arm_0_L', 'swappos_custom_1']
    
        # match these lists of locator's to the master
        #cmds.matchTransform(locator, self.master_swap_ctrl)
        print("test loc list; ", self.space_swap_locators)
        for locator in self.space_swap_locators:
            if "COG" in locator:
                print(f"found COG in locator list > {locator}")
                cmds.parent(locator, self.ctrl_cog)
            elif "world" in locator:
                print(f"found world in locator list > {locator}")
                cmds.parent(locator, self.ctrl_root)
            elif f"{locator[10:-2]}" in locator:
                cmds.parent(locator, self.top_ctrl)

                
                




    def get_loc(self):
        pass


    def blend_matrix(self):
        pass

