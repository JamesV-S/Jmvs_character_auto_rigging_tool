
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
    def __init__(self, guide_list, jnt_rig_list, neck_amount, orientation):
        
        # originally, locators already exist and the joints & system's are 
        # built off of that. 
        cmds.select(cl=1)
        # variables to pass through # 
        # joint list, guid_list, neck_amount, orientation
        self.master_guide = guide_list[-1]
        self.guide_list = guide_list[:-1]
        self.guide_list.reverse()

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

        # variables to store # 
        self.neck_amnt = self.neck_head_amnt-1
        self.ctrl_amnt = self.neck_head_amnt
        self.neck_guide_list = self.guide_list[-1]
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

        self.pref_list = ["jnt_att", "ctrl_att", "jnt_TwistNeg"]

        self.create_att_nod_Twistneg()

    def create_att_nod_Twistneg(self):
        numLS = create_list_from_integer(self.neck_amnt)
        for i in range(self.neck_amnt):            
            name_att_jnt = f"{self.pref_list[0]}_{self.neck_guide_list[6:-2]}_{numLS[i]}"
            print(f"NName of att joint: {name_att_jnt}")
            cmds.joint(n=name_att_jnt)
            cmds.matchTransform(name_att_jnt, self.jntAtt_match[i], pos=1, rot=1, scl=0)
            cmds.makeIdentity(name_att_jnt, a=1, t=0, r=1, s=0)

    def get_ctrls(self):
        return self.fk_ctrls