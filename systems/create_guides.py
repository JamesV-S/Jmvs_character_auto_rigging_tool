import maya.cmds as cmds
import importlib
import os
from systems.utils import (connect_modules, utils, control_shape) #  reverse_foot, 
importlib.reload(connect_modules)
importlib.reload(utils)
importlib.reload(control_shape)
# importlib.reload(reverse_foot)


scale = 1

# control_shape.controlTypes().create_cube()
class Guides():
    def __init__(self, accessed_module, offset, side, to_connect_to, use_existing_attr):
        self.module = importlib.import_module(f"systems.modules.{accessed_module}")
        # [if] statement for "self.create_guide" variable {if == "hand"}
        # else:
        self.create_guide = self.guides
    def collect_guides(self):
        pass

    def creation(self, accessed_module, offset, side, to_connect_to, use_existing_attr, orientation):
        pass
        # 1) Setup & initialisation
       
        # 2) Determine Side
       
        # 3) Determine Orientation
       
        # 4) Guide creation loop
       
        # 5) Parenting & connecting guides
       
        # 6) Add attributes
       
        # 7) control shape attributes
       
        # 8) Return UI data