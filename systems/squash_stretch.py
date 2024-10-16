
import maya.cmds as cmds
import importlib

from systems.utils import (utils)

importlib.reload(utils)

class cr_squash_stretch():
    def __init__(self, key, val_joints, rig_type):
        self.key = key
        self.val_joints = val_joints
        self.rig_type = rig_type
        print(f"STRETCH KEY: {self.key}")
        self.define_names()
        self.cr_attr()
        self.cr_nodes()
        self.connect_nodes()

    # function for 'name_definition'
    def define_names(self):
        for joint in self.key['ik_joint_list']:
            if self.val_joints["start_joint"] in joint:
                self.start_joint = joint
            elif self.val_joints["pv_joint"] in joint:
                self.pv_joint = joint
            elif self.val_joints["end_joint"] in joint:
                self.end_joint = joint

        for guide in self.key['guide_list']:
            if self.val_joints["start_joint"] in guide:
                self.start_guide = guide
                self.start_ctrl = f"ctrl_ik_{self.start_guide[6:]}"
            elif self.val_joints["end_joint"] in guide:
                self.end_guide = guide
                self.end_ctrl = f"ctrl_ik_{self.end_guide[6:]}"

    # func for create attr
    def cr_attr(self):
        print(self.key['mdl_switch_ctrl_list'])
        self.switch_Attr = "ik_fk_Switch"
        self.stretchy_attr = "strechiness"
        self.stretch_type = "stretch_type"
        stretch_options_enum = "Both:Stretch:Squash"
        utils.add_locked_attrib(self.key['mdl_switch_ctrl_list'], ["STRETCH"])
        utils.add_float_attrib(self.key['mdl_switch_ctrl_list'], [self.stretchy_attr], 
                               [0,1], True)
        print("here bruv : ", self.key['mdl_switch_ctrl_list'])
        utils.custom_enum_attr(self.key['mdl_switch_ctrl_list'], self.stretch_type, stretch_options_enum) 
        
        for x in range(len(self.key['ik_ctrl_list'])):
            utils.add_locked_attrib(self.key['ik_ctrl_list'][x], ["STRETCH"])
            utils.proxy_attr_list(self.key['mdl_switch_ctrl_list'],
                                  self.key['ik_ctrl_list'][x], self.stretchy_attr)
            utils.proxy_attr_list(self.key['mdl_switch_ctrl_list'], 
                                  self.key['ik_ctrl_list'][x], self.stretch_type)
        
        
    # func for create nodes
    def cr_nodes(self):
        print(f"{self.key['master_guide']}")
        self.stretch_distance = f"{self.key['master_guide'].replace('master_', 'DIST_str_')}"
        print(self.stretch_distance)
        utils.cr_node_if_not_exists(1, "distanceBetween", self.stretch_distance)
        self.scalefactor = f"{self.key['master_guide'].replace('master_', 'SCLFACTMULTI_str_')}"
        utils.cr_node_if_not_exists(1, "multiplyDivide", self.scalefactor, {"operation": 2})
        self.blend_colours_1 = f"{self.key['master_guide'].replace('master_', 'BC1_str_')}"
        utils.cr_node_if_not_exists(1, "blendColors", self.blend_colours_1, {"color2R": 1, "color2G": 1, "color2B": 1} )
        self.control_pma = f"{self.key['master_guide'].replace('master_', 'PMA_')}"
        utils.cr_node_if_not_exists(1, "plusMinusAverage", self.control_pma, {"input1D[0]": 1})
        self.condition = f"{self.key['master_guide'].replace('master_', 'COND_str_')}"
        utils.cr_node_if_not_exists(1, "condition", self.condition, {"secondTerm": 1})
        self.volume_multi = f"{self.key['master_guide'].replace('master_', 'VOLMULTI_str_')}"
        utils.cr_node_if_not_exists(1, "multiplyDivide", self.volume_multi, {"operation": 3, "input2X":-1})
        self.blend_colours_2 = f"{self.key['master_guide'].replace('master_', 'BC2_str_')}"
        utils.cr_node_if_not_exists(1, "blendColors", self.blend_colours_2)
        
        
    # func for connect nodes
    def connect_nodes(self):
        loc_endposs = cmds.spaceLocator(n=f"{self.end_guide.replace('guide_', 'loc_')}_stretchEndPoss")[0]
        cmds.matchTransform(loc_endposs, self.end_ctrl)
        cmds.parent(loc_endposs, self.end_ctrl)

        loc_startposs = cmds.spaceLocator(n=f"{self.start_guide.replace('guide_', 'loc_')}_stretchEndPoss")[0]
        cmds.matchTransform(loc_startposs, self.start_ctrl)
        cmds.parent(loc_startposs, self.start_ctrl)
        
        utils.connect_attr(f"{loc_startposs}.worldMatrix[0]", f"{self.stretch_distance}.inMatrix1")
        utils.connect_attr(f"{loc_endposs}.worldMatrix[0]", f"{self.stretch_distance}.inMatrix2")
        
        mid_joint_length = cmds.getAttr(f"{self.pv_joint}.translateX") 
        end_joint_length = cmds.getAttr(f"{self.end_joint}.translateX") 
        distance_value = mid_joint_length + end_joint_length
        print(f" DISTACNE VALUE: {distance_value}")
        utils.connect_attr(f"{self.stretch_distance}.distance", f"{self.scalefactor}.input1X")
        cmds.setAttr(f"{self.scalefactor}.input2X", distance_value)

        #connectAttr -f arm_L_ik_ctrl.Stretchiness arm_l_stretch_blend.blender;
        # connectAttr -f arm_l_scalefactor_mult.outputX arm_l_stretch_blend.color1R
        utils.connect_attr(f"{self.key['mdl_switch_ctrl_list']}.{self.stretchy_attr}", f"{self.blend_colours_1}.blender")
        utils.connect_attr(f"{self.scalefactor}.outputX", f"{self.blend_colours_1}.color1R")

        # connectAttr -f arm_L_ik_ctrl.Stretch_Type arm_l_stretch_control_pma.input1D[1]
        # connectAttr -f arm_L_ik_ctrl.Stretch_Type arm_l_stretch_control_pma.input1D[2]
        utils.connect_attr(f"{self.key['mdl_switch_ctrl_list']}.{self.stretch_type}", f"{self.control_pma}.input1D[1]")
        utils.connect_attr(f"{self.key['mdl_switch_ctrl_list']}.{self.stretch_type}", f"{self.control_pma}.input1D[2]")
        
        # connectAttr -f arm_l_stretch_control_pma.output1D arm_l_stretch_condition.operation
        # connectAttr -f arm_l_scalefactor_mult.outputX arm_l_stretch_condition.firstTerm
        # connectAttr -f arm_l_stretch_blend.outputR arm_l_stretch_condition.colorIfTrueR
        utils.connect_attr(f"{self.control_pma}.output1D", f"{self.condition}.operation")
        utils.connect_attr(f"{self.scalefactor}.outputX", f"{self.condition}.firstTerm")
        utils.connect_attr(f"{self.blend_colours_1}.outputR", f"{self.condition}.colorIfTrueR")

        # connectAttr -f arm_l_stretch_condition.outColorR arm_l_volume_multi.input1X
        utils.connect_attr(f"{self.condition}.outColorR", f"{self.volume_multi}.input1X")

        # connectAttr -f arm_L_ik_ctrl.FK_IK_Switch arm_l_stretch_ik_blend.blender
        if self.rig_type == "IKFK":
            utils.connect_attr(f"{self.key['mdl_switch_ctrl_list']}.{self.switch_Attr}", f"{self.blend_colours_2}.blender")
        elif self.rig_type == "IK":
            cmds.setAttr(f"{self.blend_colours_2}.blender", 0)

        utils.connect_attr(f"{self.condition}.outColorR", f"{self.blend_colours_2}.color2R")
        utils.connect_attr(f"{self.volume_multi}.outputX", f"{self.blend_colours_2}.color2G")

        # Connect to the joints:
        # connect to joint scale
        
        cmds.connectAttr(f"{self.blend_colours_2}.outputR",f"{self.start_joint}.scaleX")
        cmds.connectAttr(f"{self.blend_colours_2}.outputR",f"{self.pv_joint}.scaleX")

        cmds.connectAttr(f"{self.blend_colours_2}.outputG",f"{self.start_joint}.scaleY")
        cmds.connectAttr(f"{self.blend_colours_2}.outputG",f"{self.pv_joint}.scaleY")
        cmds.connectAttr(f"{self.blend_colours_2}.outputG",f"{self.start_joint}.scaleZ")
        cmds.connectAttr(f"{self.blend_colours_2}.outputG",f"{self.pv_joint}.scaleZ")
        