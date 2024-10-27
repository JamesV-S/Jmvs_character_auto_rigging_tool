
import maya.cmds as cmds
import importlib
from systems.utils import (OPM, cr_pole_vector, utils, control_shape)

importlib.reload(OPM)
importlib.reload(utils)
importlib.reload(cr_pole_vector)
importlib.reload(control_shape)

class create_ik_sys():
    def __init__(self, module, ik_joint_list, master_guide, scale, val_joints):
        # varibales for joints above & below
        self.above_root_joints = []
        self.below_root_joints = []
        self.val_joints = val_joints
        self.module = module
        self.master_guide = master_guide

        if 'arm' in self.module: 
            print("IK system has found 'arm' name in the module")
        else:
            print("IK system has NOT found 'arm' name in the module")

        # Call the function: 
        self.ik_systems(ik_joint_list)
        # Group the ctrls & joints into two seperate groups.
        
        '''
        try:
            cmds.group(self.grouped_ctrls, n=f"grp_ik_ctrls_{master_guide}", w=1)
            
            #if 'quad' in self.module:
            #    cmds.group(ik_joint_list[0], n=f"grp_ik_jnts_{master_guide}", w=1)
            #    cmds.parent(self.driver_joint_list[0], f"grp_ik_jnts_{master_guide}")
           #     print(f"----------------- @@@@@@@@@@ ----------------- : Checking quad in module: {self.module}")
           #     print(f" ----------------- IK SYS: self.driver_joint_list[0] is: {self.driver_joint_list[0]}")#  self.driver_joint_list[0], 
            #else:
            cmds.group(ik_joint_list[0], n=f"grp_ik_jnts_{master_guide}", w=1)
        except IndexError:
            pass
        '''


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
            if 'arm' in self.module: 
                if self.val_joints["top_joint"] in joint:
                    self.top_joint = joint
                print(f"IK self.top_joint is :{self.top_joint}")
            if 'quad' in self.module:
                if self.val_joints["calf_joint"] in joint:
                    self.quad_calf_joint = joint
            #if 'quad' in self.module:
            #    if self.val_joints["calf_joint"] in joint:
            #        self.calf_joint = joint


        # call helper scripts to create pole vector control(location)
        # - collect other ctrls
        self.collect_other_controls(ik_joint_list)
        
        if 'quad' in self.module:
            self.cr_quad_driver_joints(ik_joint_list)

        pv_ctrl = self.cr_pv()
        hdl_ctrl = self.cr_ik_handle() 
        root_ctrl = self.cr_top_handle_ctrl()
        above_ctrls = self.cr_above_root_ctrl()
        if 'arm' in self.module:
            top_ctrl = self.cr_top_ctrl()
        
        # for quad driver joint to follow the torso:
        if 'quad' in self.module: # self.top_ctrl_cv
            utils.connect_attr(f"{self.top_ctrl_cv}.worldMatrix[0]", f"{self.driver_joint_list[0]}.offsetParentMatrix")
            axis_list = ["X", "Y", "Z"]
            for x in range(len(axis_list)):
                cmds.setAttr(f"{self.driver_joint_list[0]}.translate{axis_list[x]}", 0)
                cmds.setAttr(f"{self.driver_joint_list[0]}.rotate{axis_list[x]}", 0)
         
        '''
        # collect other ctrls & organise them. 
        if above_ctrls:
            self.ik_ctrls = [pv_ctrl, hdl_ctrl, root_ctrl] + above_ctrls
            self.grouped_ctrls = [pv_ctrl, hdl_ctrl, above_ctrls[0]]
        else:
            
            self.ik_ctrls = [pv_ctrl, hdl_ctrl, root_ctrl]
            self.grouped_ctrls = [pv_ctrl, hdl_ctrl, root_ctrl]
            # if the module has the name arm in it: 
            if 'arm' in self.module:
                self.ik_ctrls.append(top_ctrl)
                self.grouped_ctrls.append(top_ctrl)
            print(f"ik_system > module: {self.module} & hdl_ctrl = {hdl_ctrl}")
        
        # OPM zero out ik ctrls
        OPM.OpmCleanTool(self.ik_ctrls)
        '''
    
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
        print(f"IK self.above_root_joint is: {self.above_root_joints}")

    
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
        # ['jnt_dvr_0_quadHip_L', 'jnt_dvr_0_quadKnee_L', 'jnt_dvr_0_quadCalf_L', 'jnt_dvr_0_quadAnkle_L']


    def cr_quad_hock_ctrl(self):
        pass

    def cr_quad_func(self):

        if not self.IS_BIPED: #quad leg only
                if self.IS_LEG:
                    cmds.group(n=("grp" + self.LEG_OR_ARM + "_hock_ctrl" + 
                                   self.WCH_SIDE), em=1)
                    hock_func_grp = ("grp" + self.LEG_OR_ARM + "_hock_ctrl" + 
                                     self.WCH_SIDE)
                    
                    # match grp to ctrl_hock rot & trans
                    cmds.matchTransform(hock_func_grp, self.hock_ctrl_nm)
                    
                    # then match grp to ik_foot's transforms only!
                    cmds.matchTransform( hock_func_grp, 
                                        ("ik_" + self.JNT_LMB_HI[3]), rot=0, 
                                        scl=0, pos=1 )
                    # prnt grp to driver_calf
                    cmds.parent(hock_func_grp, ("driver_"+self.JNT_LMB_HI[2]))
                    
                    #parent ik_caf_hdl to grp_hock    
                    cmds.parent(ik_caf_hdl[0], hock_func_grp) 
                    cmds.select(hock_func_grp)
                    OPM.OpmCleanTool()
                    Deslect()
                
        def hock_functionality():
            # Make ctrl_hock's translations drive grp_hock's rotations
            if not self.IS_BIPED:
                if self.IS_LEG:
                    if self.WCH_SIDE[1:] == "Bl":
                        multiValue = .5
                    else:
                        multiValue = -.5
                else:
                    multiValue = 2.5      
            
            TraAx = "Z" # forward
            rotAX = "X" # side
            remainingAX = "Y"

            if not self.IS_BIPED:
                cmds.shadingNode( "multiplyDivide", au=1, n=("hock_multi" 
                                    + self.LEG_OR_ARM + self.WCH_SIDE) )
                hockMulti = ("hock_multi" + self.LEG_OR_ARM + 
                                self.WCH_SIDE)
                
                cmds.connectAttr( (self.hock_ctrl_nm + ".translate"), 
                                (hockMulti + ".input1"), f=1)
                
                if self.IS_LEG:
                    cmds.connectAttr( (f"{hockMulti}.output{TraAx}"), 
                                        (f"{hock_func_grp}.rotate{rotAX}"), 
                                        f=1 )
                    cmds.connectAttr( (f"{hockMulti}.output{rotAX}"), 
                                        (f"{hock_func_grp}.rotate{TraAx}"), 
                                        f=1 )
                    cmds.setAttr( (f"{hockMulti}.input2{TraAx}"), 
                                    multiValue )
                    cmds.setAttr( (f"{hockMulti}.input2{rotAX}"), 
                                    multiValue*-1) # -1 for left
                else:
                    cmds.connectAttr( (f"{hockMulti}.output{TraAx}"), 
                                    (arm_grp_hok + ".rotate" + remainingAX), 
                                    f=1 )
                    cmds.connectAttr( (f"{hockMulti}.output{remainingAX}"),
                                    (f"{arm_grp_hok}.rotate{TraAx}"), f=1 )
                    cmds.setAttr((hockMulti + ".input2" + remainingAX), 
                                    multiValue*-1 )
                
        if not self.IS_BIPED:
            if self.IS_LEG:
                hock_functionality()

    
    def cr_pv(self):
        pv_ctrl = cr_pole_vector.create_pole_vector(self.start_joint, self.pv_joint, self.end_joint)
        cmds.rename(pv_ctrl, f"ctrl_pv{self.pv_joint[6:]}")
        return f"ctrl_pv{self.pv_joint[6:]}"


    def cr_ik_handle(self):
        if 'biped' in self.module:
            ctrl_ik_end = f"ctrl_ik{self.end_joint[6:]}" 
            control_shape.Controls(scale=[1,1,1], guide=self.end_joint[6:], 
                ctrl_name=ctrl_ik_end, 
                rig_type="ik"
            )
            print(f"create_IK_systems: = {ctrl_ik_end}")
            self.ik_handle = cmds.ikHandle(
            n=f"hdl_ik{self.end_joint[6:]}", solver="ikRPsolver",
            sj=self.start_joint, ee=self.end_joint 
            )
        
        
            cmds.poleVectorConstraint(
                f"ctrl_pv{self.pv_joint[6:]}", f"hdl_ik{self.end_joint[6:]}",
                n= f"pvCons{self.end_joint[6:]}")
            
            if self.val_joints["world_orientation"] is True:
                cmds.matchTransform(ctrl_ik_end, f"hdl_ik{self.end_joint[6:]}")
            else:
                cmds.matchTransform(ctrl_ik_end, self.end_joint)
            # Constrain the ik control to the ik handle!
            cmds.parentConstraint(ctrl_ik_end, f"hdl_ik{self.end_joint[6:]}", mo=1, n=f"pCons_ik_hdl{self.end_joint[6:]}")
            cmds.addAttr(ctrl_ik_end, ln="handle", at="enum", en="True", k=0)
            return ctrl_ik_end
        elif 'quad' in self.module:
            print(f"IK SYS: cr_ik_hdl for quadruped")
            # Driver handle: 
            ctrl_ik_end = f"ctrl_ik{self.end_joint[6:]}" 
            control_shape.Controls(scale=[1,1,1], guide=self.end_joint[6:], 
                ctrl_name=ctrl_ik_end, 
                rig_type="ik"
            )
            
            if self.val_joints["world_orientation"] is True:
                cmds.matchTransform(ctrl_ik_end, f"jnt_dvr{self.end_joint[6:]}")
            else:
                cmds.matchTransform(ctrl_ik_end, self.end_joint)

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

            cmds.parent(self.dvr_hdl[0], ctrl_ik_end)
            cmds.parent(self.calf_ik_hdl[0], self.driver_joint_list[2])
            cmds.parent(self.hock_ik_hdl[0],  self.driver_joint_list[-1])

            # Make leg follow torso - done after the whole systemis built 
            # becuase i need the top control which comes afer.

            # Make the foot stay level (orient constraint)
            cmds.orientConstraint()

            cmds.select(cl=1)

        '''
        if 'quad' in self.module:
            self.ik_handle = cmds.ikHandle(
                n=f"hdl_ik{self.end_joint[6:]}", solver="ikRPsolver",
                sj=self.calf_joint, ee=self.end_joint 
                )
            self.driver_handle = cmds.ikHandle(
                n=f"hdl_driver{self.driver_joint_list[-1][7:]}", solver="ikRPsolver",
                sj=self.driver_joint_list[0], ee=self.driver_joint_list[-1] 
                )
            # cmds.parent(self.driver_handle[0], ctrl_ik_end)
            print(f"IK-----IK - driver_handle is: hdl_driver{self.driver_joint_list[-1][7:]}")
            
            #self.ik_calf_handle = cmds.ikHandle(
            #    n=f"hdl_ik{self.calf_joint[6:]}", solver="ikRPsolver",
            #    sj=self.start_joint, ee=self.calf_joint 
            #    )
            print(f"IK-----IK - ik_calf_handle is: hdl_ik{self.calf_joint[6:]}")
            #self.hock_handle = cmds.ikHandle(
            #    n=f"hdl_ik{self.end_joint[6:]}", solver="ikSCsolver",
            #    sj=self.start_joint, ee=self.end_joint 
            #    )
            print(f"IK-----IK - hock_handle is: hdl_ik{self.end_joint[6:]}")
        '''
        
        



    def cr_top_handle_ctrl(self):
        self.top_ctrl_cv = f"ctrl_ik{self.start_joint[6:]}"
        control_shape.Controls(scale=1, guide=self.start_joint[6:], 
            ctrl_name=self.top_ctrl_cv, 
            rig_type="ik"
        )
        cmds.matchTransform(self.top_ctrl_cv, self.start_joint)
        cmds.parentConstraint(self.top_ctrl_cv, self.start_joint, mo=1, n=f"pCons{self.start_joint[6:]}")
        return self.top_ctrl_cv
    
    def cr_top_ctrl(self):
        top_ctrl_name = f"ctrl_ik{self.top_joint[6:]}"
        top_ctrl = control_shape.Controls(scale=[1,1,1], guide=self.top_joint[6:], 
            ctrl_name=top_ctrl_name, 
            rig_type="ik"
        )
        ctrl_ori = control_shape.Controls.return_ctrl_ori()
        if 'object' in ctrl_ori:
            cmds.matchTransform(top_ctrl_name, self.top_joint)
        else:
            cmds.matchTransform(top_ctrl_name, self.top_joint)
            cmds.makeIdentity(top_ctrl_name, a=1, t=0, r=1, s=1)
        cmds.parentConstraint(top_ctrl_name, self.top_joint, mo=1, n=f"pCons{self.top_joint[6:]}")
        return top_ctrl_name


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
            cmds.parent(self.top_ctrl_cv, self.to_be_parented[0])
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
        pass
        # return self.ik_ctrls


    def get_handle(self):
        pass
        # return self.ik_handle