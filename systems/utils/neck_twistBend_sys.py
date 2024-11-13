
import maya.cmds as cmds
from systems.utils import control_shape, OPM
import importlib
importlib.reload(control_shape)
importlib.reload(OPM)
# importlib.reload(customAttr)

def override_color_(clr_num):
    sel = cmds.ls(selection=True)
    shape = cmds.listRelatives( sel, shapes = True )
    #add = cmds.select( add=True )
    for node in shape:
        cmds.setAttr (node + ".overrideEnabled" ,True)
        cmds.setAttr (node + ".overrideColor" , clr_num) 

def create_list_from_integer(value):
    # Create a list of string representations of integers from 1 to value
    my_list = [str(i) for i in range(1, value + 1)]
    return my_list

class neck_sys():
    def __init__(self, guide_list, jnt_rig_list, neck_amount, scale, orientation):
        
        # originally, locators already exist and the joints & system's are 
        # built off of that. 
        cmds.select(cl=1)
        # variables to pass through # 
        # joint list, guid_list, neck_amount, orientation
        self.master_guide = guide_list[-1]
        self.guide_list = guide_list[:-1]
        self.guide_list.reverse()

        self.scale = scale
        self.jnt_rig_list = jnt_rig_list
        self.neck_head_amnt = neck_amount
        self.orientation = orientation
        print(f"NECK_SYS <¬¬¬> master_guide: {self.master_guide},  guide_list: {self.guide_list}, jnt_rig_list: {self.jnt_rig_list}, neck_head_amnt: {self.neck_head_amnt}, orientation: {self.orientation}")
        
        '''
        NECK_SYS <¬¬¬> 
        master_guide: 'master_0_neck_head'
        guide_list: ['guide_0_neck_0', 'guide_0_neck_1', 'guide_0_neck_2'], 
        jnt_rig_list: ['jnt_rig_0_neck_0', 'jnt_rig_0_neck_1', 'jnt_rig_0_neck_2'], 
        neck_head_amnt: 3, 
        orientation: XYZ
        '''

        self.jntAtt_match = self.guide_list[:-1]
        self.first_guide = self.guide_list[0]

        self.neck_amnt = self.neck_head_amnt-1
        self.ctrl_amnt = self.neck_head_amnt
        
        self.twist_neg_amnt = self.neck_head_amnt-1

        self.head_guide = self.guide_list[-1]
        
        print(f"NECK_SYS <¬¬¬> neck_amnt: {self.neck_amnt}, ctrl_amnt: {self.ctrl_amnt}, twist_neg_amnt: {self.twist_neg_amnt}, head_guide: {self.head_guide}")
        '''
        NECK_SYS <¬¬¬> 
        neck_amnt: 2, 
        ctrl_amnt: 3, 
        twist_neg_amnt: 2, 
        head_guide: guide_0_neck_2
        '''
        
        if self.orientation == "XYZ":
            self.twist_axis = "X"
            self.bend_axis = ["Y", "Z"]
        elif self.orientation == "YZX":
            self.twist_axis = "Y"
            self.bend_axis = ["X", "Z"]
        print(f"NECK_SYS <¬¬¬> twist_axis: {self.twist_axis}, bend_axis: {self.bend_axis}")
        '''
        XYZ:
        NECK_SYS <¬¬¬> twist_axis: X, bend_axis: ['Y', 'Z']
        '''
        
        if self.neck_amnt < 5:
            self.divisibleList =  [ 2, 4, 8, 16, 32, 64 ]
            print("USING FOR HIGHER NUMBERS")
        else:
            self.divisibleList = [ 1.5, 3, 6, 12, 24, 48 ]
            print("USING FOR LOWER NUMBERS")

        self.pref_list = ["jnt_att", "ctrl_att"]

        self.cr_att_jnt_and_ctrl()
        self.end_guide_att()
        
        print(f"^^¬^^ Neck controls: {self.ctrl_att_neck}")
        print(f"^^¬^^ END Neck controls: {self.ctrl_att_head}")

    # Build the ctrl_att & jnt_att + twistneg_joint in the correct hierarchy!
    def cr_att_jnt_and_ctrl(self):
        numLS = create_list_from_integer(self.neck_amnt)
        twist_neg_name = "jnt_TwistNeg"
        ctrl_neck_list = []
        for i in range(self.neck_amnt): # 2 wth 3 from ui          
            jnt_att_neck = f"{self.pref_list[0]}_{self.first_guide[6:-2]}_{numLS[i]}"
            print(f"NName of att joint: {jnt_att_neck}")
            cmds.joint(n=jnt_att_neck)
            print(f"jnt_att_match_to: {self.jntAtt_match[i]}")
            cmds.matchTransform(jnt_att_neck, self.jntAtt_match[i], pos=1, rot=1, scl=0)
            cmds.makeIdentity(jnt_att_neck, a=1, t=0, r=1, s=0)

            #-------------
            self.ctrl_att_neck = f"{self.pref_list[1]}_{self.first_guide[6:-2]}_{numLS[i]}"
            print(f"NECK_ATT: guide for CTRL > {self.ctrl_att_neck}")
            control_module = control_shape.Controls(self.scale, guide=f"{self.jntAtt_match[i][5:]}", 
                    ctrl_name=self.ctrl_att_neck, rig_type="fk" 
                    )
            cmds.matchTransform(self.ctrl_att_neck, self.jntAtt_match[i], pos=1, rot=1, scl=0)
            cmds.parent(self.ctrl_att_neck, jnt_att_neck)
            ctrl_neck_list.append(self.ctrl_att_neck)

            #-------------
            jnt_TwistNeg_name = f"{twist_neg_name}_{self.first_guide[6:-2]}_{numLS[i]}"
            cmds.joint(n=jnt_TwistNeg_name)
            cmds.matchTransform(jnt_TwistNeg_name, self.jntAtt_match[i])
            cmds.makeIdentity(jnt_TwistNeg_name, a=1, t=0, r=1, s=0)
            
            cmds.parentConstraint( jnt_att_neck, self.ctrl_att_neck, w=1, mo=0 )
           

    def end_guide_att(self):
        bend_neg_name =  "jnt_BendNeg"

        jnt_att_end = f"{self.pref_list[0]}_{self.head_guide[6:]}"
        print(f"Neck_sys. end_joint: {jnt_att_end}")
        cmds.joint( n= jnt_att_end )
        cmds.matchTransform(jnt_att_end, self.head_guide, pos=1, rot=1, scl=0)
        cmds.makeIdentity(jnt_att_end, a=1, t=0, r=1, s=0)
        # Don't need to opm clean ctrls cus they will be zeroed out by the jnt's above them in Hi!

        #-------------
        jnt_bendNeg_end = f"{bend_neg_name}_{self.head_guide[6:]}"
        print(f"Neck_sys. bendNeg end_joint: {jnt_bendNeg_end}")
        cmds.joint( n= jnt_bendNeg_end )
        cmds.matchTransform(jnt_bendNeg_end, self.head_guide, pos=1, rot=1, scl=0)
        cmds.makeIdentity(jnt_bendNeg_end, a=1, t=0, r=1, s=0)
        cmds.select(cl=1)

        #-------------
        self.ctrl_att_head = f"{self.pref_list[1]}_{self.head_guide[6:]}"
        control_module = control_shape.Controls(self.scale, guide=f"{self.head_guide[5:]}", 
                    ctrl_name=self.ctrl_att_head, rig_type="fk" 
                    )
        cmds.matchTransform(self.ctrl_att_head, self.head_guide, pos=1, rot=1, scl=0)
        cmds.parent(self.ctrl_att_head, jnt_bendNeg_end)
    
    # rog joints alr exist
    def connecting_(self):
        pass
        

    def get_ctrls(self):
        return self.fk_ctrls