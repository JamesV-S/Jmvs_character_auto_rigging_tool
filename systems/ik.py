
import maya.cmds as cmds
import importlib
from systems.utils import (OPM, cr_pole_vector, utils, control_shape)

importlib.reload(OPM)
importlib.reload(utils)
importlib.reload(cr_pole_vector)
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
        try:
            cmds.group(self.grouped_ctrls, n=f"grp_ik_ctrls_{master_guide}", w=1)
            cmds.group(ik_joint_list[0], n=f"grp_ik_jnts_{master_guide}", w=1)
        except IndexError:
            pass

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
        self.collect_other_controls(ik_joint_list)

        pv_ctrl = self.cr_pv()
        hdl_ctrl = self.cr_ik_handle() 
        root_ctrl = self.cr_top_handle_ctrl()
        above_ctrls = self.cr_above_root_ctrl()

        # collect other ctrls & organise them. 
        if above_ctrls:
            self.ik_ctrls = [pv_ctrl, hdl_ctrl, root_ctrl] + above_ctrls
            self.grouped_ctrls = [pv_ctrl, hdl_ctrl, above_ctrls[0]]
        else:
            self.ik_ctrls = [pv_ctrl, hdl_ctrl, root_ctrl]
            self.grouped_ctrls = [pv_ctrl, hdl_ctrl, root_ctrl]

        # OPM zero out ik ctrls
        OPM.OpmCleanTool(self.ik_ctrls)

    
    def collect_other_controls(self, ik_joint_list):
        start_index = ik_joint_list.index(self.start_joint)
        end_index = ik_joint_list.index(self.end_joint)
        for joint in self.other_joints:
            joint_index = ik_joint_list.index(joint)
            if joint_index < start_index:
                self.above_root_joints.append(joint)
            elif joint_index > end_index:
                self.below_root_joints.append(joint)
    
    def cr_pv(self):
        pv_ctrl = cr_pole_vector.create_pole_vector(self.start_joint, self.pv_joint, self.end_joint)
        cmds.rename(pv_ctrl, f"ctrl_pv{self.pv_joint[6:]}")
        return f"ctrl_pv{self.pv_joint[6:]}"


    def cr_ik_handle(self):
        ctrl_cv = f"ctrl_ik{self.end_joint[6:]}"
        control_shape.Controls(scale=[1,1,1], guide=self.end_joint[6:], 
            ctrl_name=ctrl_cv, 
            rig_type="ik"
        )
        print(f"create_IK_systems: = {ctrl_cv}")
        self.ik_handle = cmds.ikHandle(
            n=f"hdl_ik{self.end_joint[6:]}", solver="ikRPsolver",
            sj=self.start_joint, ee=self.end_joint 
            )
        cmds.poleVectorConstraint(
            f"ctrl_pv{self.pv_joint[6:]}", f"hdl_ik{self.end_joint[6:]}", 
            n= f"pvCons{self.end_joint[6:]}")
        
        if self.val_joints["world_orientation"] is True:
            cmds.matchTransform(ctrl_cv, f"hdl_ik{self.end_joint[6:]}")
        else:
            cmds.matchTransform(ctrl_cv, self.end_joint)
        # Constrain the ik control to the ik handle!
        cmds.parentConstraint(ctrl_cv, f"hdl_ik{self.end_joint[6:]}", mo=1, n=f"pCons_ik_hdl{self.end_joint[6:]}")
        cmds.addAttr(ctrl_cv, ln="handle", at="enum", en="True", k=0)
        return ctrl_cv


    def cr_top_handle_ctrl(self):
        self.start_ctrl_cv = f"ctrl_ik{self.start_joint[6:]}"
        control_shape.Controls(scale=1, guide=self.start_joint[6:], 
            ctrl_name=self.start_ctrl_cv, 
            rig_type="ik"
        )
        cmds.matchTransform(self.start_ctrl_cv, self.start_joint)
        cmds.parentConstraint(self.start_ctrl_cv, self.start_joint, mo=1, n=f"pCons{self.start_joint[6:]}")
        return self.start_ctrl_cv

    def cr_above_root_ctrl(self):
        self.to_be_parented = []
        if self.above_root_joints:
            for joint in self.above_root_joints:
                ctrl_crv_tmp = f"ctrl_ik{joint[6:]}"
                control_shape.Controls(scale=1, guide=joint[6:], 
                    ctrl_name=ctrl_crv_tmp, rig_type="ik"
                )
                self.to_be_parented.append(ctrl_crv_tmp)
                cmds.matchTransform(ctrl_crv_tmp, joint)
                cmds.parentConstraint(ctrl_crv_tmp, joint, mo=1, n= f"pCons{joint[6:]}")
            cmds.parent(self.start_ctrl_cv, self.to_be_parented[0])
            for ctrl in range(len(self.to_be_parented)):
                if ctrl == 0:
                    pass
                else:
                    try:
                        cmds.parent(self.to_be_parented[ctrl], self.to_be_parented[ctrl+1])
                    except:
                        pass
        return self.to_be_parented 
    
    

    def get_ctrls(self):
        return self.ik_ctrls


    def get_handle(self):
        return self.ik_handle