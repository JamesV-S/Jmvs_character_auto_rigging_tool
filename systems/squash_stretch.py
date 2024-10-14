
import maya.cmds as cmds
import importlib

from systems.utils import (utils)

importlib.reload(utils)

class cr_squash_stretch():
    def __init__(self, key, val_joints):
        self.key = key
        self.val_joints = val_joints
        print(f"STRETCH KEY: {self.key}")

        self.cr_attr()
    # function for 'name_definition'

    # func for create attr
    def cr_attr(self):
        print(self.key['mdl_switch_ctrl_list'])
        stretchy_attr = "strechiness"
        utils.add_locked_attrib(self.key['mdl_switch_ctrl_list'], ["STRETCH"])
        utils.add_float_attrib(self.key['mdl_switch_ctrl_list'], [stretchy_attr], [0,1], True) 
        for x in range(len(self.key['ik_ctrl_list'])):
            utils.add_locked_attrib(self.key['ik_ctrl_list'][x], ["STRETCH"])
            utils.proxy_attr_list(self.key['mdl_switch_ctrl_list'], 
                                  self.key['ik_ctrl_list'][x], stretchy_attr)
        

    # func for create nodes


    # func for connect nodes