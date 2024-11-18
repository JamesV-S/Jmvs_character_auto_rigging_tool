
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
        self.jnt_twistNeg_list = []
        self.jnt_att_list = []
        for i in range(self.neck_amnt): # 2 wth 3 from ui          
            jnt_att_neck = f"{self.pref_list[0]}_{self.first_guide[6:-2]}_{numLS[i]}"
            print(f"NName of att joint: {jnt_att_neck}")
            cmds.joint(n=jnt_att_neck)
            print(f"jnt_att_match_to: {self.jntAtt_match[i]}")
            cmds.matchTransform(jnt_att_neck, self.jntAtt_match[i], pos=1, rot=1, scl=0)
            cmds.makeIdentity(jnt_att_neck, a=1, t=0, r=1, s=0)
            self.jnt_att_list.append(jnt_att_neck)
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
            self.jnt_TwistNeg = f"{twist_neg_name}_{self.first_guide[6:-2]}_{numLS[i]}"
            cmds.joint(n=self.jnt_TwistNeg)
            cmds.matchTransform(self.jnt_TwistNeg, self.jntAtt_match[i]) 
            cmds.makeIdentity(self.jnt_TwistNeg, a=1, t=0, r=1, s=0)
            self.jnt_twistNeg_list.append(self.jnt_TwistNeg)
            
           
    def end_guide_att(self):
        bend_neg_name =  "jnt_BendNeg"

        jnt_att_end = f"{self.pref_list[0]}_{self.head_guide[6:]}"
        print(f"Neck_sys. end_joint: {jnt_att_end}")
        cmds.joint( n= jnt_att_end )
        cmds.matchTransform(jnt_att_end, self.head_guide, pos=1, rot=1, scl=0)
        cmds.makeIdentity(jnt_att_end, a=1, t=0, r=1, s=0)
        # Don't need to opm clean ctrls cus they will be zeroed out by the jnt's above them in Hi!
        self.jnt_att_list.append(jnt_att_end)

        #-------------
        self.jnt_bendNeg_end = f"{bend_neg_name}_{self.head_guide[6:]}"
        print(f"Neck_sys. bendNeg end_joint: {self.jnt_bendNeg_end}")
        cmds.joint( n= self.jnt_bendNeg_end )
        cmds.matchTransform(self.jnt_bendNeg_end, self.head_guide, pos=1, rot=1, scl=0)
        cmds.makeIdentity(self.jnt_bendNeg_end, a=1, t=0, r=1, s=0)
        cmds.select(cl=1)

        #-------------
        self.ctrl_att_head = f"{self.pref_list[1]}_{self.head_guide[6:]}"
        control_module = control_shape.Controls(self.scale, guide=f"{self.head_guide[5:]}", 
                    ctrl_name=self.ctrl_att_head, rig_type="fk" 
                    )
        cmds.matchTransform(self.ctrl_att_head, self.head_guide, pos=1, rot=1, scl=0)
        cmds.parent(self.ctrl_att_head, self.jnt_bendNeg_end)


    def add_attr(self):
        # create the custom attrib's on head control
        utils.add_locked_attrib(ctrl=self.ctrl_att_head, en=["NECK_SYS"])
        utils.add_float_attrib(ctrl=self.ctrl_att_head, flt=["Neck_Twist_Mult"], 
                               val=[0,0.95], limited=True)
        utils.add_float_attrib(ctrl=self.ctrl_att_head, flt=["Neck_Bend_Mult"], 
                               val=[0,1], limited=True)
        cmds.setAttr( f"{self.ctrl_att_head}.Neck_Twist_Mult", 0.5 )
        cmds.setAttr( f"{self.ctrl_att_head}.Neck_Bend_Mult", 0.5 )


    def add_nodes(self):
        # self.jnt_twistNeg_list = []
        
        cmds.setAttr(f"{self.ctrl_att_head}.rotateX", 90)

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
        
        # to UnitConv & Minus & to Mult
        utils.connect_attr(f"{self.ctrl_att_head}.Neck_Twist_Mult", 
                            f"{minTws}.input")
        utils.connect_attr(f"{minTws}.output", 
                            f"{N_root_NegMd}.input1{self.twist_axis}")
        
        utils.connect_attr(f"{self.ctrl_att_head}.Neck_Twist_Mult", 
                            f"{N_root_AttMd}.input1{self.twist_axis}")
        utils.connect_attr(f"{self.ctrl_att_head}.rotate{self.twist_axis}", 
                            f"{N_root_NegMd}.input2{self.twist_axis}")


        # Connect up to the att jnt!
        print(f"att_Jnts_Ls = {self.jnt_att_list}")
        print(f"att_Jnts_Ls[-2] = {self.jnt_att_list[-2]}")
        utils.connect_attr(f"{N_root_AttMd}.output{self.twist_axis}", 
                           f"{self.jnt_att_list[-2]}.rotate{self.twist_axis}")


        print(f"twist_neg_list = {self.jnt_twistNeg_list}")
        print(f"twist_neg_list[-1] = {self.jnt_twistNeg_list[-1]}")
        utils.connect_attr(f"{N_root_NegMd}.output{self.twist_axis}", 
                            f"{self.jnt_twistNeg_list[-1]}.rotate{self.twist_axis}")
        # ['jnt_TwistNeg_neck_1', 'jnt_TwistNeg_neck_2', 'jnt_BendNeg_head']
        

        #--------------------------------------------------------------------------------------
        # TWIST SYS - page 1-2
        #--------------------------------------------------------------------------------------
        # Twist moving down the chain: get value from parent att_Md node, 
        # plug that into 2 new att/Neg Md nodes for the current joint working on!
        # create fucntion that does this, so for the amount of neck joints, call this function that many times to 
        # dissiminate the twisting of the neck!
        # (the next chain always comes from the previous att_md node)
        # These joints need to get half of the value from it's parent jnt!

        divisible_value = 2 # Constant value
        
        # [neck_01, neck_02, neck_03, neck_04, head] - neck just before head is the neck_root! 
        # Everything before 'neck_04' is a list of joints

        just_neck_list = self.jnt_att_list[:-1] # remove head joint
        jnt_attNeck_children = just_neck_list[:-1]
        # ['jnt_att_0_neck_1', 'jnt_att_0_neck_2']
        jnt_attNeck_children.reverse() # reverse the order cus we're working form head down to bottom of neck joints.
        print(f"jnt_attNeck_children = {jnt_attNeck_children}")

        twisNeg_children = self.jnt_twistNeg_list[:-1]
        twisNeg_children.reverse()
        print(f"twisNeg_children = {twisNeg_children}")

        print(f"AYY == MD_att_{self.first_guide[6:-2]}")
        # AYY == MD_att_0_neck
        
        # -------------------------
        # build MD for eaxh neck att & do connections
        neck_order = create_list_from_integer(len(jnt_attNeck_children))
        neck_order.reverse()

        order_list = [self.divisibleList[i] for i in range(len(jnt_attNeck_children))]
        for x in range(len(jnt_attNeck_children)):
            # Set the att_Md input2X to positive 'Divisible_value' & neg_Md to negative 'Divisible_value'
            MD_1_att = f"MD_att_{self.first_guide[6:-2]}_{neck_order[x]}"
            utils.cr_node_if_not_exists(util_type=1, node_type="multiplyDivide", 
                                        node_name=MD_1_att, 
                                        set_attrs={f"input2{self.twist_axis}":order_list[x], "operation":2})
            
            MD_1_neg = f"MD_neg_{self.first_guide[6:-2]}_{neck_order[x]}"
            utils.cr_node_if_not_exists(util_type=1, node_type="multiplyDivide", 
                                        node_name=MD_1_neg, 
                                        set_attrs={f"input2{self.twist_axis}":-order_list[x], "operation":2})
            
            utils.connect_attr(f"{N_root_AttMd}.output{self.twist_axis}", f"{MD_1_att}.input1{self.twist_axis}")
            utils.connect_attr(f"{N_root_AttMd}.output{self.twist_axis}", f"{MD_1_neg}.input1{self.twist_axis}")
            
            # Connect to the att & Neg joint!
            utils.connect_attr(f"{MD_1_att}.output{self.twist_axis}", f"{jnt_attNeck_children[x]}.rotate{self.twist_axis}")
            utils.connect_attr(f"{MD_1_neg}.output{self.twist_axis}", f"{twisNeg_children[x]}.rotate{self.twist_axis}")
        
        
        #--------------------------------------------------------------------------------------
        # Bend SYS - page 4-5
        #--------------------------------------------------------------------------------------
        bend_ratio = f"MD_{self.first_guide[6:-2]}_bendRatio"
        utils.cr_node_if_not_exists(util_type=1, node_type="multiplyDivide", 
                                        node_name=bend_ratio, 
                                        set_attrs={"operation":2,})
        
        # begin with the 'N_root_AttMd'+ connect bending axes to it!
        for x in range(2):
            utils.connect_attr(f"{self.ctrl_att_head}.rotate{self.bend_axis[x]}", f"{N_root_AttMd}.input2{self.bend_axis[x]}")
            utils.connect_attr(f"{self.ctrl_att_head}.Neck_Bend_Mult", f"{N_root_AttMd}.input1{self.bend_axis[x]}")
            print(f"HERE BEND EXIS ===== {bend_ratio}.input2{self.bend_axis[x]}")
            cmds.setAttr(f"{bend_ratio}.input2{self.bend_axis[x]}", divisible_value)
            utils.connect_attr(f"{N_root_AttMd}.output{self.bend_axis[x]}", f"{bend_ratio}.input1{self.bend_axis[x]}")

        # Connect bend_ratio to all neck joints 
        # just_neck_list
        for x in range(self.neck_amnt):
            utils.connect_attr(f"{bend_ratio}.output{self.bend_axis[0]}", f"{just_neck_list[x]}.rotate{self.bend_axis[0]}")
            utils.connect_attr(f"{bend_ratio}.output{self.bend_axis[1]}", f"{just_neck_list[x]}.rotate{self.bend_axis[1]}")

        # for Bending neg: minus the value from 'N_root_AttMd' & 
        # put into the jnt_bend_Neg with 2 pma(sum) node into the right bending axis for the jnt_bend_neg!
        bend_UC = [cmds.shadingNode("unitConversion", au=1, n=f"UC_{self.first_guide[6:-2]}_bend_{self.bend_axis[i]}_min") for i in range(2)]
        Axis_pma = [cmds.shadingNode("plusMinusAverage", au=1, n=f"pma_{self.first_guide[6:-2]}_bendNeg_{self.bend_axis[i]}") for i in range(2)]
        for i in range(2):
            cmds.setAttr( bend_UC[i] + ".conversionFactor", -1 )
            utils.connect_attr(f"{N_root_AttMd}.output{self.bend_axis[i]}", f"{bend_UC[i]}.input")
            utils.connect_attr(f"{bend_UC[i]}.output", f"{Axis_pma[i]}.input1D[0]")
            utils.connect_attr(f"{Axis_pma[i]}.output1D", f"{self.jnt_bendNeg_end}.rotate{self.bend_axis[i]}")

    def get_ctrls(self):
        return self.fk_ctrls