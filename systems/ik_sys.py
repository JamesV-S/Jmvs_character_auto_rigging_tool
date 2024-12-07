
import maya.cmds as cmds
import importlib
from systems.utils import (OPM, cr_pole_vector, utils, control_shape)

importlib.reload(OPM)
importlib.reload(utils)
importlib.reload(cr_pole_vector)
importlib.reload(control_shape)

class create_ik_sys():
    def __init__(self, module, ik_joint_list, master_guide, scale, jnt_valid):
        # varibales for joints above & below
        self.above_root_joints = []
        self.below_root_joints = []
        self.jnt_valid = jnt_valid
        self.module = module
        self.master_guide = master_guide
        if 'finger' in self.module:
            self.scale = scale*2
        else: 
            self.scale = scale
        # Call the function: 
        self.IK_setup(ik_joint_list)

        # Group the ctrls & joints into two seperate groups.
        try:
            cmds.group(self.grouped_ctrls, n=f"grp_ik_ctrls_{master_guide}", w=1)
            cmds.group(ik_joint_list[0], n=f"grp_ik_jnts_{master_guide}", w=1)
            if 'finger' in self.module: 
                fing_ik_ctrl_ls = [self.hdl_ctrl,self.last_ctrl_name]
                cmds.parent(self.hdl_ctrl, self.last_ctrl_name)
                OPM.OpmCleanTool(fing_ik_ctrl_ls)
        except IndexError:
            pass
        

    def IK_setup(self, ik_joint_list):
        # Joint Identification, pole vector & end joints based on val data
        self.other_joints = []
        for joint in ik_joint_list:
            if self.jnt_valid["start_joint"] in joint:
                self.start_joint = joint
            elif self.jnt_valid["pv_joint"] in joint:
                self.pv_joint = joint
            elif self.jnt_valid["end_joint"] in joint:
                self.end_joint = joint
            if 'arm' in self.module and self.jnt_valid["top_joint"] in joint:
                    self.first_joint = joint
            if 'quad' in self.module and self.jnt_valid["calf_joint"] in joint:
                    self.quad_calf_joint = joint
            if 'finger' in self.module and self.jnt_valid["last_joint"] in joint:
                    self.last_joint = joint
        
        self.collect_other_controls(ik_joint_list)
        
        if 'quad' in self.module:
            self.cr_quad_driver_joints(ik_joint_list)

        pv_ctrl = self.cr_pv_ctrl()
        self.hdl_ctrl = self.cr_ik_handle() 
        root_ctrl = self.cr_first_handle_ctrl()
        upper_ctrl = self.cr_root_ctrl()
        if 'arm' in self.module:
            first_ctrl = self.edit_end_ctrl()

        # for quad driver joint to follow the torso:
        if 'quad' in self.module: # self.first_ctrl_cv
            utils.connect_attr(f"{self.first_ctrl_cv}.worldMatrix[0]", f"{self.driver_joint_list[0]}.offsetParentMatrix")
            axis_list = ["X", "Y", "Z"]
            for x in range(len(axis_list)):
                cmds.setAttr(f"{self.driver_joint_list[0]}.translate{axis_list[x]}", 0)
                cmds.setAttr(f"{self.driver_joint_list[0]}.rotate{axis_list[x]}", 0)
         
        # collect other ctrls & organise them. 
        if upper_ctrl:
            self.ik_ctrls = [pv_ctrl, self.hdl_ctrl, root_ctrl] + upper_ctrl
            self.grouped_ctrls = [pv_ctrl, self.hdl_ctrl, upper_ctrl[0]]
        else:
            self.ik_ctrls = [pv_ctrl, self.hdl_ctrl, root_ctrl]
            self.grouped_ctrls = [pv_ctrl, self.hdl_ctrl, root_ctrl]
            # if the module has the name arm in it: 
            if 'arm' in self.module:
                self.ik_ctrls.append(first_ctrl)
                self.grouped_ctrls.append(first_ctrl)
            if 'finger' in self.module:
                self.ik_ctrls.append(self.last_ctrl_name)
                self.grouped_ctrls.append(self.last_ctrl_name)
        OPM.OpmCleanTool(self.ik_ctrls)
        
    
    def collect_other_controls(self, ik_joint_list):
        start_index = ik_joint_list.index(self.start_joint)
        end_index = ik_joint_list.index(self.end_joint)
        
        for joint in self.other_joints:
            joint_index = ik_joint_list.index(joint)
            print(f"IK joint idex is: {joint_index}")
            if joint_index < start_index:
                self.above_root_joints.append(joint)
            elif joint_index > end_index:
                self.below_root_joints.append(joint)

    
    def cr_quad_driver_joints(self, ik_joint_list):
        self.driver_joint_list = []
        cmds.select(cl=1)
        for jnt in ik_joint_list:
            new_jnt_name = jnt.replace('ik', 'dvr')
            cmds.joint(n=new_jnt_name)
            cmds.matchTransform(new_jnt_name, jnt)
            cmds.makeIdentity(new_jnt_name, a=1, t=0, r=1, s=1)
            self.driver_joint_list.append(new_jnt_name)
        print(f"IK: Quadruped DRV joint list: {self.driver_joint_list}")

    
    def cr_pv_ctrl(self):
        pv_ctrl = cr_pole_vector.create_pole_vector(
            self.start_joint, self.pv_joint, self.end_joint)
        cmds.rename(pv_ctrl, f"ctrl_pv{self.pv_joint[6:]}")
        if 'finger' in self.module:
            for axis in ["X", "Y", "Z"]:
                cmds.setAttr(f"ctrl_pv{self.pv_joint[6:]}.scale{axis}", self.scale*2)
        return f"ctrl_pv{self.pv_joint[6:]}"


    def cr_ik_handle(self):
        ctrl_ik_end = f"ctrl_ik{self.end_joint[6:]}" 
        control_shape.Controls(scale=self.scale, guide=self.end_joint[6:], 
            ctrl_name=ctrl_ik_end, 
            rig_type="ik"
        )
        if 'biped' in self.module:
            print(f"create_IK_setup: = {ctrl_ik_end}")
            self.ik_handle = cmds.ikHandle(
            n=f"hdl_ik{self.end_joint[6:]}", solver="ikRPsolver",
            sj=self.start_joint, ee=self.end_joint 
            )
        
            cmds.poleVectorConstraint(
                f"ctrl_pv{self.pv_joint[6:]}", f"hdl_ik{self.end_joint[6:]}",
                n= f"pvCons{self.end_joint[6:]}")
            
            if self.jnt_valid["world_orientation"] is True:
                cmds.matchTransform(ctrl_ik_end, f"hdl_ik{self.end_joint[6:]}")
            else:
                cmds.matchTransform(ctrl_ik_end, self.end_joint)
            # Constrain the ik control to the ik handle!
            cmds.parentConstraint(ctrl_ik_end, f"hdl_ik{self.end_joint[6:]}", 
                                  mo=1, n=f"pCons_ik_hdl{self.end_joint[6:]}")
            cmds.addAttr(ctrl_ik_end, ln="handle", at="enum", en="True", k=0)

            if 'finger' in self.module:
                # self.last_ctrl
                self.last_ctrl_name = f"ctrl_ik{self.last_joint[6:]}"
                control_shape.Controls(scale=self.scale, guide=self.last_joint[6:], 
                                       ctrl_name=self.last_ctrl_name, 
                                       rig_type="ik"
                                       )
                self.sc_handle = cmds.ikHandle(
                n=f"hdl_ik{self.last_joint[6:]}", solver="ikSCsolver",
                sj=self.end_joint, ee=self.last_joint 
                )
                if self.jnt_valid["world_orientation"] is False:
                    cmds.matchTransform(self.last_ctrl_name, self.last_joint)
                cmds.parentConstraint(self.last_ctrl_name, f"hdl_ik{self.last_joint[6:]}", 
                                  mo=1, n=f"pCons_ik_hdl{self.last_joint[6:]}")
        

        elif 'quad' in self.module:          
            # Driver handle:
            self.dvr_hdl = cmds.ikHandle(
            n=f"hdl_dvr{self.end_joint[6:]}", solver="ikRPsolver",
            sj=self.driver_joint_list[0], ee=self.driver_joint_list[-1]
            )
            # ik handles:
            self.calf_ik_hdl = cmds.ikHandle(
            n=f"hdl_ik{self.quad_calf_joint[6:]}", solver="ikRPsolver",
            sj=self.start_joint, ee=self.quad_calf_joint
            )
            hock_ik_hdl_name = f"hdl_ik{self.end_joint[6:]}".replace('Ankle', 'Hock')
            self.hock_ik_hdl = cmds.ikHandle(
            n=hock_ik_hdl_name, solver="ikSCsolver",
            sj=self.quad_calf_joint, ee=self.end_joint
            )
            if self.jnt_valid["world_orientation"] is True:
                cmds.matchTransform(ctrl_ik_end, self.dvr_hdl, pos=1, rot=0)
            else:
                cmds.matchTransform(ctrl_ik_end, self.end_joint)

            cmds.parent(self.dvr_hdl[0], ctrl_ik_end)
            cmds.parent(self.calf_ik_hdl[0], self.driver_joint_list[2])
            cmds.parent(self.hock_ik_hdl[0],  self.driver_joint_list[-1])

            # Hock functionality:
            self.hock_ctrl = f"ctrl_ik{self.quad_calf_joint[6:]}"
            control_shape.Controls(scale=self.scale, guide=f"{self.quad_calf_joint[6:]}", 
                ctrl_name=self.hock_ctrl, 
                rig_type="ik"
            )
            cmds.matchTransform(self.hock_ctrl, self.quad_calf_joint)
            cmds.parent(self.hock_ctrl, ctrl_ik_end)
            OPM.OpmCleanTool(self.hock_ctrl)
            hock_grp = cmds.group(n=f"grp_hock{self.end_joint[6:]}", em=1)
            cmds.matchTransform(hock_grp, self.hock_ctrl)
            cmds.matchTransform(hock_grp, ctrl_ik_end, rot=0, 
                                        scl=0, pos=1)
            cmds.parent(hock_grp, self.driver_joint_list[2])
            OPM.OpmCleanTool(hock_grp)
            cmds.parent(self.calf_ik_hdl[0], hock_grp)

            # ---------------------------
            # HOCK GRP CONNECTIONS
            TraAx = "Z" # forward
            rotAX = "Y" # side
            remainingAX = "X"
            hock_MD = f"MD_{self.quad_calf_joint[6:]}"
            utils.cr_node_if_not_exists(1, "multiplyDivide", hock_MD)
            
            if self.master_guide[-2:] == "_L":
                cmds.setAttr(f"{hock_MD}.input2{rotAX}", -1)
                cmds.setAttr(f"{hock_MD}.input2{TraAx}", 1)
            elif self.master_guide[-2:] == "_R":
                cmds.setAttr(f"{hock_MD}.input2{rotAX}", 1)
                cmds.setAttr(f"{hock_MD}.input2{TraAx}", -1)
        
            utils.connect_attr(f"{self.hock_ctrl}.translate", f"{hock_MD}.input1")
            utils.connect_attr(f"{hock_MD}.output{TraAx}", f"{hock_grp}.rotate{rotAX}")
            utils.connect_attr(f"{hock_MD}.output{rotAX}", f"{hock_grp}.rotate{TraAx}")
            # ---------------------------
            
            # PoleVector
            cmds.poleVectorConstraint(
                f"ctrl_pv{self.pv_joint[6:]}", self.calf_ik_hdl[0],
                n= f"pvCons{self.end_joint[6:]}")

            cmds.select(cl=1)
        # Make the foot stay level (orient constraint)
        cmds.orientConstraint(ctrl_ik_end, self.end_joint, mo=1, w=1)
        return ctrl_ik_end     
        

    def cr_first_handle_ctrl(self):
        self.first_ctrl_cv = f"ctrl_ik{self.start_joint[6:]}"
        control_shape.Controls(scale=self.scale, guide=self.start_joint[6:], 
            ctrl_name=self.first_ctrl_cv, 
            rig_type="ik"
        )
        cmds.matchTransform(self.first_ctrl_cv, self.start_joint)
        cmds.parentConstraint(self.first_ctrl_cv, self.start_joint, mo=1, n=f"pCons{self.start_joint[6:]}")
        return self.first_ctrl_cv
    

    def edit_end_ctrl(self):
        first_ctrl_name = f"ctrl_ik{self.first_joint[6:]}"
        control_shape.Controls(scale=self.scale, guide=self.first_joint[6:], 
            ctrl_name=first_ctrl_name, 
            rig_type="ik")
        # set custom control orientation
        ctrl_ori = control_shape.Controls.return_ctrl_ori()
        if 'object' in ctrl_ori:
            cmds.matchTransform(first_ctrl_name, self.first_joint)
        else:
            cmds.matchTransform(first_ctrl_name, self.first_joint)
            cmds.makeIdentity(first_ctrl_name, a=1, t=0, r=1, s=1)
        cmds.parentConstraint(first_ctrl_name, self.first_joint, mo=1, n=f"pCons{self.first_joint[6:]}")
        return first_ctrl_name
    

    def cr_root_ctrl(self):
        if not self.above_root_joints:
            # return empty ls
            return []
        self.control_cvs = []
        # cr ctrl & parent constraint for each. 
        for joint in self.above_root_joints:
            ctrl_name = f"ctrl_ik{joint[6:]}"
            control_shape.Controls(scale=self.scale, guide=joint[6:], 
                                ctrl_name=ctrl_name, rig_type="ik")
            cmds.matchTransform(ctrl_name, joint)
            cmds.parentConstraint(ctrl_name, joint, mo=True, n=f"pCons{joint[6:]}")
            self.control_cvs.append(ctrl_name)

        # Parent the fst control to the top control
        if self.control_cvs:
            cmds.parent(self.first_ctrl_cv, self.control_cvs[0])
            for i in range(1, len(self.control_cvs)):
                cmds.parent(self.control_cvs[i], self.control_cvs[i - 1])
        return self.control_cvs
        

    def get_ctrls(self):
        return self.ik_ctrls


    def get_handle(self):
        return self.ik_handle