
import maya.cmds as cmds
from systems.utils import control_shape, OPM, utils
import importlib
importlib.reload(control_shape)
importlib.reload(OPM)
importlib.reload(utils)

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
        self.add_attr()
        self.add_nodes()
        
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

    def add_attr(self):
        # create the custom attrib's on head control
        utils.add_locked_attrib(ctrl=self.ctrl_att_head, en=["NECK_SYS"])
        utils.add_float_attrib(ctrl=self.ctrl_att_head, flt=["Neck_Twist_Mult"], 
                               val=[0,1], limited=True)
        utils.add_float_attrib(ctrl=self.ctrl_att_head, flt=["Neck_Bend_Mult"], 
                               val=[0,1], limited=True)
        cmds.setAttr( f"{self.ctrl_att_head}.Neck_Twist_Mult", 0.5 )
        cmds.setAttr( f"{self.ctrl_att_head}.Neck_Bend_Mult", 0.5 )


    def add_nodes(self):
        pass
        N_root_AttMd = f"MD_att_RT_{self.first_guide[6:-2]}"
        print(f"neck_root > {N_root_AttMd}") # MD_neck_0_neck_root
        utils.cr_node_if_not_exists(util_type=1, node_type="multiplyDivide", 
                                    node_name=N_root_AttMd, set_attrs=None)
        utils.connect_attr(f"{self.ctrl_att_head}.rotate{self.twist_axis}", 
                           f"{N_root_AttMd}.input2{self.twist_axis}")
        
        N_root_NegMd = f"MD_neg_RT_{self.first_guide[6:-2]}"
        utils.cr_node_if_not_exists(util_type=1, node_type="multiplyDivide", 
                                node_name=N_root_NegMd, set_attrs=None)
        
        minTws = f"UC_minus_twist_{self.first_guide[6:-2]}"
        utils.cr_node_if_not_exists(util_type=1, node_type="unitConversion", 
                                node_name=minTws, set_attrs={"conversionFactor": -1})
        
        # # to UnitConv & Minus & to Mult
        utils.connect_attr(f"{self.ctrl_att_head}.Neck_Twist_Mult", 
                           f"{minTws}.input")
        utils.connect_attr(f"{minTws}.output", 
                           f"{N_root_NegMd}.input1{self.twist_axis}")
        
        utils.connect_attr(f"{self.ctrl_att_head}.Neck_Twist_Mult", 
                           f"{N_root_AttMd}.input1{self.twist_axis}")
        utils.connect_attr(f"{self.ctrl_att_head}.rotate{self.twist_axis}", 
                           f"{N_root_NegMd}.input2{self.twist_axis}")

        # cmds.connectAttr( (self.ctrlLs[-1] + ".Neck_Twist_Mult"), (minTws + ".input"), f=1 )
        # cmds.connectAttr( (minTws + ".output"), (f"{N_root_NegMd}.input1{self.twistAxis}"), f=1 )
        # cmds.connectAttr( (self.ctrlLs[-1] + ".Neck_Twist_Mult"), (f"{N_root_AttMd}.input1{self.twistAxis}"), f=1 )
        # cmds.connectAttr( (self.ctrlLs[-1] + ".rotate" + self.twistAxis), (f"{N_root_NegMd}.input2{self.twistAxis}"), f=1 )
        
        '''
        # Connect up to the att jnt!
        utils.connect_attr(f"{N_root_AttMd}.output{self.twist_axis}", 
                           f"{minTws}.rotate")
        cmds.connectAttr( (f"{N_root_AttMd}.output{self.twistAxis}"), (f"{self.attJntsLs[-2]}.rotate{self.twistAxis}"), f=1 )
        
        # Connect to the Neg twist for same jnt
        cmds.connectAttr( (f"{N_root_NegMd}.output{self.twistAxis}"), (f"{self.TwistNeg[-2]}.rotate{self.twistAxis}"), f=1 )
        '''

        '''
        N_root_AttMd = cmds.shadingNode("multiplyDivide", au=1, n="neck_root" + "_att_MD")
        cmds.connectAttr( (f"{self.ctrlLs[-1]}.rotate{self.twistAxis}"), (f"{N_root_AttMd}.input2{self.twistAxis}"), f=1 )
        N_root_NegMd = cmds.shadingNode("multiplyDivide", au=1, n="neck_root" + "_neg_MD")
        minTws = cmds.shadingNode("unitConversion", au=1, n="neck_twist" + "_minus_UC")
        cmds.setAttr( minTws + ".conversionFactor", -1 )
        '''

    def get_ctrls(self):
        return self.fk_ctrls