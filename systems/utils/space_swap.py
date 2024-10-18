
import maya.cmds as cmds
import importlib

from systems.utils import (utils)

importlib.reload(utils)

class cr_spaceSwapping():
    def __init__(self, key):
        self.key = key
        self.locator_list = self.key["space_swap"]
        self.guide_list = self.key["guide_list"]

        rig_type = cmds.getAttr(f"{self.key['master_guide']}.{self.key['master_guide']}_rig_type", asString=1)
        print(f"Space_swapp: {self.guide_list} > {rig_type}")
        if rig_type == "IKFK":
            self.space_swap_locators = self.create_locators()
        
    # might need to create temporary ctrl_root to work as the inverse_matrix. 
    def create_locators(self):
       # created_loc_list = [cmds.spaceLocator(n=f"loc_swappos{x}")[0] 
       #                     for x in self.guide_list[6:] for item in self.locator_list if item in x] 
        
        custom_module_name_id = f"{self.key['module']}_{self.key['guide_number']}{self.key['side']}"
        created_loc_list = []
        for item in self.locator_list:
            created_loc_list.append(cmds.spaceLocator(n=f"loc_swappos_{item}_{custom_module_name_id}")[0])
        print(f"Created loc list: {created_loc_list}")
        print()
        
        
        


    def parent_to_location(self):
        pass


    def get_loc(self):
        pass


    def blend_matrix(self):
        pass

