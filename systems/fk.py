
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
        '''
        # group the ctrls & joints into two seperate groups
        try:
            cmds.group(n=f"grp_fk_ctrls_{master_guide}", w=1)
            cmds.group(n=f"grp_fk_jnts_{master_guide}", w=1)
        except IndexError:
            pass
        '''
        

    def fk_system(self, fk_joint_list, delete_end):
        self.fk_ctrls = []
        jnt_fk_ctrls = []
        fk_joint_list.reverse()
        scale = self.scale

        # Instead of having to adapt for a leg or arm or biped or quad 
        # - creare for one & read data to fit the right module.
        for x in range(len(fk_joint_list)):
            print(f"'create_fk_sys()', guide: {fk_joint_list[x][6:]}")
            control_module = control_shape.Controls(scale, guide=f"{fk_joint_list[x][6:]}", 
                ctrl_name=f"ctrl_fk{fk_joint_list[x][6:]}", rig_type="fk" 
                )
            ctrl_shape = control_module.return_ctrl()
            cmds.matchTransform(f"ctrl_fk{fk_joint_list[x][6:]}", fk_joint_list[x])

        

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