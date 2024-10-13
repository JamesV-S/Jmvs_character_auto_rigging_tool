
import maya.cmds as cmds
import importlib
from systems.utils import (OPM, utils, PV_position, control_shape)

importlib.reload(OPM)
importlib.reload(utils)
importlib.reload(PV_position)
importlib.reload(control_shape)

class create_fk_sys():
    def __init__(self, ik_joint_list, master_guide, scale, val_joints):
        # varibales for joints above & below
        self.above_root_joints = []
        self.below_root_joints = []
        self.val_joints = val_joints

        # Call the function: 
        self.ik_systems(ik_joint_list)
        # Group the ctrls & joints into two seperate groups.

    def ik_systems(self, ik_joint_list):
        # Joint Identification, pole vector & end joints based on val data
        self.other_joints = []
        for joint in ik_joint_list:
            if self.val_joints["start_joint"] in joint:
                self.start_joint = joint
            elif self.val_joints["pv_joint"] in joint:
                self.pv_joint = joint
            elif self.val_joints["end_joint"] in joint:
                self.end_joint = joint
        # call helper scripts to create pole vector control(location)
        # - collect other ctrls
        pv_ctrl = self.cr_pv()
        hdl_ctrl = self.cr_ik_handle() 
        root_ctrl = self.cr_top_handle_ctrl()
        above_ctrls = self.cr_above_root_ctrl()

        # collect other ctrls & organise them. 
        if above_ctrls:
            self.ik_ctrls = [pv_ctrl, hdl_ctrl, root_ctrl] + above_ctrls
            self.grouped_ctrls = [pv_ctrl, hdl_ctrl, above_ctrls[0]]
        else:
            self.ik_ctrls = [pv_ctrl, hdl_ctrl, root_ctrl] + above_ctrls
            self.grouped_ctrls = [pv_ctrl, hdl_ctrl, root_ctrl]

        # OPM zero out ik ctrls
        OPM.OpmCleanTool(self.ik_ctrls)

    def cr_pv(self):
        pv_ctrl = PV_position.create_pv(self.start_joint, self.pv_joint, 
                                        self.end_joint)
        cmds.rename(pv_ctrl, f"ctrl_pv_{self.pv_joint[6:]}")
        return f"ctrl_pv_{self.pv_joint[6:]}"


    def cr_ik_handle(self):
        control_module = control_shape.Controls(
            scale=[1,1,1], guide=self.end_joint[6:], 
            ctrl_name=f"ctrl_ik_{self.end_joint[6:]}", 
            rig_type="ik")
        control_module = str(control_module)
        print(f"create_IK_systems: ctrl_shape = {control_module}")


    def cr_top_handle_ctrl(self):
        pass


    def cr_above_root_ctrl(self):
        pass


    def get_ctrls(self):
        return self.ik_ctrls


    def get_handle(self):
        return self.ik_handle