
import maya.cmds as cmds
from systems.utils import control_shape, OPM
import importlib
importlib.reload(control_shape)
importlib.reload(OPM)

class create_fk_sys():
    def __init__(self, joint_list, master_guide, scale, delete_end):
        self.scale = scale
        # Call the function
        self.fk_system(joint_list, delete_end)
        
        # group the ctrls & joints into two seperate groups
        try:
            cmds.group(self.fk_ctrls[-1], n=f"grp_fk_ctrls_{master_guide}", w=1)
            cmds.group(joint_list[0], n=f"grp_fk_jnts_{master_guide}", w=1)
        except IndexError:
            pass
        
        
    def fk_system(self, joint_fk_list, delete_end):
        self.fk_ctrls = []
        jnt_fk_ctrls = []
        joint_fk_list.reverse()
        scale = self.scale

        # Instead of having to adapt for a leg or arm or biped or quad 
        # - creare for one & read data to fit the right module.
        for x in range(len(joint_fk_list)):
            #print(f"'create_fk_sys()', guide: {joint_fk_list[x][6:]}")
            control_module = control_shape.Controls(scale, guide=f"{joint_fk_list[x][6:]}", 
                ctrl_name=f"ctrl_fk{joint_fk_list[x][6:]}", rig_type="fk" 
                )
            # master_guide is not a string, but rather an instance of an controlTypes class.
            control_module = str(control_module) 
            #ctrl_shape = control_module.return_ctrl()
            cmds.matchTransform(f"ctrl_fk{joint_fk_list[x][6:]}", joint_fk_list[x])
            if delete_end is True:
                if cmds.listRelatives(joint_fk_list[x], c=1) is None:
                    cmds.delete(f"ctrl_fk{joint_fk_list[x][6:]}")
            elif "root" in joint_fk_list[x]:
                cmds.delete(f"ctrl_fk{joint_fk_list[x][6:]}")
            else:
                self.fk_ctrls.append(f"ctrl_fk{joint_fk_list[x][6:]}")
                jnt_fk_ctrls.append(joint_fk_list[x])
        
        # Parent the controls
        for ctrl in range(len(self.fk_ctrls)):
            try:
                cmds.parent(self.fk_ctrls[ctrl], self.fk_ctrls[ctrl+1])
            except:
                pass
        
        # Clean the controls
        for ctrl in self.fk_ctrls:
            OPM.OpmCleanTool(ctrl)

        # create a function & call it here to constrain fk joints to rig joints!
        self.constrain_fk_to_rig_joints(jnt_fk_ctrls)
        joint_fk_list.reverse()


    def constrain_fk_to_rig_joints(self, jnt_fk_ctrls):
        for item in range(len(self.fk_ctrls)):
            cmds.parentConstraint(
                self.fk_ctrls[item], jnt_fk_ctrls[item], 
                n=f"cons_prnt_{self.fk_ctrls[item]}"
            )

    def get_ctrls(self):
        return self.fk_ctrls

        

'''
My fk script:

def fk_joint_systems(self):
    num_index_list = [1,2,3,4]
    if self.IS_BIPED:
        fk_leg = 3
        fk_arm = 3
    else:
        fk_leg = 3
        fk_arm = 4
    # Setup Fk system on Clav OR hip with O.P.M
    cmds.connectAttr(("ctrl_fk_" + self.JNT_LMB_HI[0] + ".worldMatrix[0]"), 
                        ("fk_" + self.JNT_LMB_HI[0] + ".offsetParentMatrix"))
            
    # Connect rest of the fk_ctrl's to fk_joint's(directly)
    if self.IS_LEG:             
        #ctrl_fk_knee - [ knee, foot, ball ]
        for i in range(fk_leg):
            cmds.connectAttr(("ctrl_fk_" + self.JNT_LMB_HI[num_index_list[i]]
                            + ".rotate"), ("fk_" + 
                            self.JNT_LMB_HI[num_index_list[i]] + ".rotate"))
            cmds.connectAttr(("ctrl_fk_" + self.JNT_LMB_HI[num_index_list[i]] 
                            + ".translate"), ("fk_" + 
                            self.JNT_LMB_HI[num_index_list[i]] + 
                            ".translate"))
            
    else: #[ upperarm, lowerarm, wrist ]
        for i in range(fk_arm):
            cmds.connectAttr( ("ctrl_fk_" + 
                            self.JNT_LMB_HI[num_index_list[i]] + ".rotate"), 
                            ("fk_" + self.JNT_LMB_HI[num_index_list[i]] 
                                + ".rotate" ))
            cmds.connectAttr( ("ctrl_fk_" + 
                            self.JNT_LMB_HI[num_index_list[i]] + 
                            ".translate"), 
                            ("fk_" + self.JNT_LMB_HI[num_index_list[i]] + 
                                ".translate" ))

    self.joint_tag_func(self.JNT_LMB_HI[0], "FK_system")

'''