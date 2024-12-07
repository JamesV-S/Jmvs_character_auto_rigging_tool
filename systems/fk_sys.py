
import maya.cmds as cmds
from systems.utils import control_shape, OPM, utils
import importlib

importlib.reload(control_shape)
importlib.reload(OPM)
importlib.reload(utils)

class Cr_Fk_Sys:
    def __init__(self, module_name, joints, guide_name, size, remove_end):
        print(f"FK Sys :::::: {joints}, guide: {guide_name}, size: {size}, remove_end: {remove_end}")
        self.module_name = module_name
        self.size = size
        self.cr_fk(joints, remove_end)
        self.group_ctrls_and_jnts(joints, guide_name)

    def cr_fk(self, joints, remove_end):
        self.fk_controls = []
        joint_controls = []
        joints.reverse()

        for idx, joint in enumerate(joints):
            control = control_shape.Controls(
                self.size,
                guide=joint[6:],
                ctrl_name=f"ctrl_fk{joint[6:]}",
                rig_type="fk")
            if 'arm' in self.module_name:
                cmds.scale(1*.01,1*.01,1*.01, f"ctrl_fk{joint[6:]}")
                cmds.makeIdentity(f"ctrl_fk{joint[6:]}.rotateZ", r=0, s=0, t=0)
            cmds.matchTransform(f"ctrl_fk{joint[6:]}", joint)

            if remove_end and cmds.listRelatives(joint, children=True) is None:
                cmds.delete(f"ctrl_fk{joint[6:]}")
            elif "root" in joint:
                cmds.delete(f"ctrl_fk{joint[6:]}")
            else:
                self.fk_controls.append(f"ctrl_fk{joint[6:]}")
                joint_controls.append(joint)
        
        utils.parent_controls(self.fk_controls)
        for ctrl in self.fk_controls:
            OPM.OpmCleanTool(ctrl)
        utils.constrain_to_joints(joint_controls, self.fk_controls)
        joints.reverse()

    def group_ctrls_and_jnts(self, joints, guide_name):
        try:
            cmds.group(self.fk_controls[-1], name=f"grp_fk_ctrls_{guide_name}", world=True)
            cmds.group(joints[0], name=f"grp_fk_joints_{guide_name}", world=True)
        except IndexError:
            print("No controls to group.")

    def get_controls(self):
        return self.fk_controls