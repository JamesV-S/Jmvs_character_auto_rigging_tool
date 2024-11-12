#---------------------------
import maya.cmds as cmds 
import importlib
# module imports----------------------------------------------------------
import BQ_Almb_removePref_mdl as rmv_pref
import BQ_Almb_addPref_mdl as add_pref
import OPM
import cr_enum_float_attrib_mdl as customAttr

# Reload the modules
importlib.reload(rmv_pref)
importlib.reload(add_pref)
importlib.reload(OPM)
importlib.reload(customAttr)

def override_color_(clr_num):
    sel = cmds.ls(selection=True)
    shape = cmds.listRelatives( sel, shapes = True )
    #add = cmds.select( add=True )
    for node in shape:
        cmds.setAttr (node + ".overrideEnabled" ,True)
        cmds.setAttr (node + ".overrideColor" , clr_num)  

def Deslect():
    cmds.select(cl=1)

def create_list_from_integer(value):
    # Create a list of string representations of integers from 1 to value
    my_list = [str(i) for i in range(1, value + 1)]
    return my_list

class jmvs_Neck_systems():
    def __init__(self):

        # Check the selection is valid
        self.selCheck = cmds.ls(sl=1, type="transform")

        # Error check to make sure a joint is selected
        if not self.selCheck:
            cmds.error("Please select the root Locator.")
        else:
            self.locRoot = cmds.ls(sl=1, type="transform")[0]

        print(self.locRoot)
        self.locHi = cmds.listRelatives(self.locRoot, ad=1, type="transform")

        self.locHi.append(self.locRoot)

        self.locHi.reverse()

        print(self.locHi)
        Deslect()

        self.jntAtt_match = self.locHi[:-1]
        print("jnts ATT & twsitNeg to match to!", self.jntAtt_match)

        self.ctrl_size = 12

        self.neckAmnt = len(self.locHi[:-1])
        self.ctrlAmnt = len(self.locHi)
        self.TwistNegAmnt = len(self.locHi[:-1])
        self.locHead = self.locHi[-1]

        self.twistAxis = "Y"
        self.bendAxis = ["X", "Z"]

        if self.neckAmnt < 5:
            self.divisibleList =  [ 2, 4, 8, 16, 32, 64 ]
            print("USING HIGHER NUMBERS")
        else:
            self.divisibleList = [ 1.5, 3, 6, 12, 24, 48 ]
            print("USING LOWER NUMBERS")

        # Create fst jnt_att_neck_#, ctrl_att_neck_#, jnt_twistNeg_neck_#,
        # all these are matched to same location!
        # how many times do i do this? = self.neckAmnt aka '2'
        self.prefLs = ["jnt_att_", "ctrl_att_", "jnt_TwistNeg_"]

        
        self.create_att_nod_Twistneg()
        self.cr_head_att_nod_BendNeg()
        self.cr_thing_you_need() # aka the rig & skn joints!
        #self.cr_ctrl()
        self.fix_hierarchy()
        self.node_connections()
    #-------------
                
    
    def create_att_nod_Twistneg(self):
        numLS = create_list_from_integer(self.neckAmnt)
        
        for i in range(self.neckAmnt):
            NMprefLs = ["jnt_att_", "ctrl_att_", "jnt_TwistNeg_"]
            
            jnt_att_neck = self.prefLs[0] + "neck_" + numLS[i]
            
            cmds.joint( n= jnt_att_neck )
            cmds.matchTransform(jnt_att_neck, self.jntAtt_match[i])
            cmds.makeIdentity(jnt_att_neck, a=1, t=0, r=1, s=0)

            #-------------
            '''
            self.node_att_name = NMprefLs[1] + "neck_" + numLS[i]
            cmds.group( n=self.node_att_name, em=1)
            cmds.matchTransform(self.node_att_name, self.jntAtt_match[i])
            cmds.parent(self.node_att_name, jnt_att_neck)
            Deslect()
            '''

            self.ctrl_att_neck = NMprefLs[1] + "neck_" + numLS[i]
            if self.twistAxis == "X":
                cmds.circle( n=self.ctrl_att_neck, nr=(1, 0, 0), c=(0, 0, 0), sw=360, s=8, ut=0 )
            elif self.twistAxis == "Y":
                cmds.circle( n=self.ctrl_att_neck, nr=(0, 1, 0), c=(0, 0, 0), sw=360, s=8, ut=0 )
            else:
                cmds.circle( n=self.ctrl_att_neck, nr=(0, 0, 1), c=(0, 0, 0), sw=360, s=8, ut=0 )
            cmds.matchTransform(self.ctrl_att_neck, self.jntAtt_match[i])
            cmds.scale(self.ctrl_size,self.ctrl_size,self.ctrl_size, (self.ctrl_att_neck + '.cv[0:7]'), r=1 )
            override_color_(17)
            cmds.parent(self.ctrl_att_neck, jnt_att_neck)

            #-------------
            jnt_TwistNeg_name = NMprefLs[2] + "neck_" + numLS[i]
            cmds.joint( n= jnt_TwistNeg_name )
            cmds.matchTransform(jnt_TwistNeg_name, self.jntAtt_match[i])
            cmds.makeIdentity(jnt_TwistNeg_name, a=1, t=0, r=1, s=0)
            #cmds.parent(jnt_TwistNeg_name, self.ctrl_att_neck)
        #Deslect()
    # create the head jnt_att, ctrl & BEND_Neg only once! ony on the lasty joint in the list!
    
    def cr_head_att_nod_BendNeg(self):
        NMprefLs = ["jnt_att_", "nod_att_", "jnt_BendNeg_"]
            
        jnt_att_name = self.prefLs[0] + "head" 
        
        cmds.joint( n= jnt_att_name )
        cmds.matchTransform(jnt_att_name, self.locHead)
        cmds.makeIdentity(jnt_att_name, a=1, t=0, r=1, s=0)
        # Don't need to opm clean ctrls cus they will be zeroed out by the jnt's above them in Hi!

        #-------------
        jnt_BendNeg_name = NMprefLs[2] + "head" 
        cmds.joint( n= jnt_BendNeg_name )
        cmds.matchTransform(jnt_BendNeg_name, self.locHead)
        cmds.makeIdentity(jnt_BendNeg_name, a=1, t=0, r=1, s=0)
        #cmds.parent(jnt_BendNeg_name, jnt_att_name)
        Deslect()

         #-------------
        self.ctrl_att_head = "ctrl_att_head" 
        if self.twistAxis == "X":
            cmds.circle( n=self.ctrl_att_head, nr=(1, 0, 0), c=(0, 0, 0), sw=360, s=8, ut=0 )
        elif self.twistAxis == "Y":
            cmds.circle( n=self.ctrl_att_head, nr=(0, 1, 0), c=(0, 0, 0), sw=360, s=8, ut=0 )
        else:
            cmds.circle( n=self.ctrl_att_head, nr=(0, 0, 1), c=(0, 0, 0), sw=360, s=8, ut=0 )
        cmds.matchTransform(self.ctrl_att_head, self.locHead)
        cmds.scale(self.ctrl_size,self.ctrl_size,self.ctrl_size, (self.ctrl_att_head + '.cv[0:7]'), r=1 )
        override_color_(17)
        cmds.parent(self.ctrl_att_head, jnt_BendNeg_name)
        '''
        self.node_att_name = NMprefLs[1] + "head"
        cmds.group( n=self.node_att_name, em=1)
        cmds.matchTransform(self.node_att_name, self.locHead)
        cmds.parent(self.node_att_name, jnt_BendNeg_name)
        Deslect()
        '''

        cmds.select("ctrl_att_neck_*")
        self.ctrlLs= cmds.ls(sl=1, type="transform")
        self.ctrlLs.append(self.ctrl_att_head)
        print("look here: ", self.ctrlLs) #['ctrl_att_neck_1', 'ctrl_att_neck_2', 'ctrl_att_head']

    # Create the skn joints now!
    def cr_thing_you_need(self):
        cmds.select("jnt_att_neck_*")
        self.attJntsLs = cmds.ls(sl=1, type="joint")
        self.attJntsLs.append("jnt_att_head")
        print(self.attJntsLs)
        Deslect()
        
        rnm_hi_list = []
        for i in range(len(self.attJntsLs)):
            rnm_hi_list.append(self.attJntsLs[i].split('_')[2:])    
                            
        joined_list = ['_'.join(rnm_hi_list[i]) for i in range(len(self.attJntsLs))]
        print("joined list: ", joined_list)
        print("split list: ", rnm_hi_list)

        self.sknNames = [(f"jnt_skn_{joined_list[i]}") for i in range(len(self.attJntsLs))]
        #(f"jnt_skn_{joined_list[i]}")

        # Build the joints
        #for newJoint in newJointList:
        
        for i in range(len(self.attJntsLs)):  #use this to limit amount of jnts we create in each jnt chain. dont want the toes, just the 4(limbJoints) main bones! 'i' represents each nom in 'limbJoints'
            #newJointName =  newJoint + joined_list[i]
            cmds.joint(n=self.sknNames[i])
            cmds.matchTransform(self.sknNames[i], self.locHi[i])
            cmds.makeIdentity(self.sknNames[i], a=1, t=0, r=1, s=0)
            print(self.sknNames[i])
        Deslect()
        #---------------------------------------------------------------
        cmds.select("jnt_att_neck_*")
        self.attJntsLs = cmds.ls(sl=1, type="joint")
        self.attJntsLs.append("jnt_att_head")
        print("jnt_att_ls", self.attJntsLs)
        Deslect()
        
        rnm_hi_list = []
        for i in range(len(self.attJntsLs)):
            rnm_hi_list.append(self.attJntsLs[i].split('_')[2:])    
                            
        joined_list = ['_'.join(rnm_hi_list[i]) for i in range(len(self.attJntsLs))]

        self.rigNames = [(f"jnt_rig_{joined_list[i]}") for i in range(len(self.attJntsLs))]
        
        for i in range(len(self.attJntsLs)):  #use this to limit amount of jnts we create in each jnt chain. dont want the toes, just the 4(limbJoints) main bones! 'i' represents each nom in 'limbJoints'
            #newJointName =  newJoint + joined_list[i]
            cmds.joint(n=self.rigNames[i])
            cmds.matchTransform(self.rigNames[i], self.locHi[i])
            cmds.makeIdentity(self.rigNames[i], a=1, t=0, r=1, s=0)
            print(self.rigNames[i])
        Deslect()
        
    '''   
    def cr_ctrl(self):
        
        numLS = create_list_from_integer(self.neckAmnt)
        for i in range(self.neckAmnt):
            ctrl_att_neck = "ctrl_att_" + "neck_" + numLS[i]
            cmds.circle( n=ctrl_att_neck, nr=(1, 0, 0), c=(0, 0, 0), sw=360, s=8, ut=0 )
            cmds.matchTransform(ctrl_att_neck, self.jntAtt_match[i])
            cmds.scale(self.ctrl_size,self.ctrl_size,self.ctrl_size, (ctrl_att_neck + '.cv[0:7]'), r=1 )
            override_color_(17)
        
        cmds.select("ctrl_att_*")
        self.ctrlLs= cmds.ls(sl=1, type="transform")

        ctrl_att_head = "ctrl_att_head" 
        cmds.circle( n=ctrl_att_head, nr=(1, 0, 0), c=(0, 0, 0), sw=360, s=8, ut=0 )
        cmds.matchTransform(ctrl_att_head, self.locHead)
        cmds.scale(self.ctrl_size,self.ctrl_size,self.ctrl_size, (ctrl_att_head + '.cv[0:7]'), r=1 )
        override_color_(17)

        self.ctrlLs.append(ctrl_att_head)
        print("look here: ", self.ctrlLs) #['ctrl_att_neck_1', 'ctrl_att_neck_2', 'ctrl_att_head']
        for i in range(self.ctrlAmnt-1): 
            cmds.parent( self.ctrlLs[i+1], self.ctrlLs[i] )
        cmds.select(self.ctrlLs)
        OPM.OpmCleanTool()
    ''' 
    def fix_hierarchy(self):
        '''
        cmds.select("nod_att_neck_*")
        self.nodLs = cmds.ls(sl=1, type="transform")
        self.nodLs.append(self.node_att_name)
        print(self.nodLs)
        print(self.ctrlLs)
        
        #connect ctrls to nodes: 
        for i in range(self.ctrlAmnt):
                cmds.connectAttr( (self.ctrlLs[i] + ".rotate"), (self.nodLs[i] + ".rotate" ))
        '''
        # Constrain nodes to rig_joints, then rig joints to skin!
        for i in range(self.ctrlAmnt):
           cmds.parentConstraint( self.ctrlLs[i], self.rigNames[i], w=1, mo=0 )
           cmds.parentConstraint( self.rigNames[i], self.sknNames[i], w=1, mo=0 )
        
        # Put them into the right place in the rig scene!
        neckLocGrp = cmds.group( n="grp_ctrl_neck", em=1 )
        cmds.parent(neckLocGrp, "grp_ctrl_torso")
        #cmds.parent(self.ctrlLs[0], neckLocGrp)

        cmds.parent(self.rigNames[0], self.sknNames[0], "skeleton")

        # create the custom attrib's on head control
        customAttr.enum_attrib(self.ctrlLs[-1], 'neck_Dvdr', 'NECK_FOLL', 'Neck_Twist_Mult')
        cmds.addAttr(self.ctrlLs[-1], longName='Neck_Bend_Mult', at='double', min=0, max=1, dv=0 )
        cmds.setAttr(self.ctrlLs[-1] + '.Neck_Bend_Mult', e=1, k=1 )
        cmds.setAttr( self.ctrlLs[-1] + '.Neck_Bend_Mult', 0.5 )
        cmds.setAttr( self.ctrlLs[-1] + '.Neck_Twist_Mult', 0.5 )


    def node_connections(self):
        # Connecting coming from ctrl to Neck_02, jnt_att & Negation
        # self.attJntsLs = ['jnt_att_neck_1', 'jnt_att_neck_2', 'jnt_att_head']
        
        cmds.select("jnt_TwistNeg_neck_*")
        self.TwistNeg = cmds.ls(sl=1, type="joint")
        self.TwistNeg.append("jnt_BendNeg_head")
        print(self.TwistNeg)
        Deslect()

        #cmds.setAttr( self.ctrlLs[-1] + ".rotateX", 90 )
        #--------------------------------------------------------------------------------------
        # page 1 - page 2 - Jnt_att_neck_2 & Jnt_TwistNeg_neck_2
        #--------------------------------------------------------------------------------------
        # neck_twist_list = ['jnt_TwistNeg_neck_1', 'jnt_TwistNeg_neck_2', 'jnt_BendNeg_head']
        N_root_AttMd = cmds.shadingNode("multiplyDivide", au=1, n="neck_root" + "_att_MD")
        cmds.connectAttr( (f"{self.ctrlLs[-1]}.rotate{self.twistAxis}"), (f"{N_root_AttMd}.input2{self.twistAxis}"), f=1 )
        N_root_NegMd = cmds.shadingNode("multiplyDivide", au=1, n="neck_root" + "_neg_MD")
        minTws = cmds.shadingNode("unitConversion", au=1, n="neck_twist" + "_minus_UC")
        cmds.setAttr( minTws + ".conversionFactor", -1 )
        
        
        # to UnitConv & Minus & to Mult
        cmds.connectAttr( (self.ctrlLs[-1] + ".Neck_Twist_Mult"), (minTws + ".input"), f=1 )
        cmds.connectAttr( (minTws + ".output"), (f"{N_root_NegMd}.input1{self.twistAxis}"), f=1 )
        cmds.connectAttr( (self.ctrlLs[-1] + ".Neck_Twist_Mult"), (f"{N_root_AttMd}.input1{self.twistAxis}"), f=1 )
        cmds.connectAttr( (self.ctrlLs[-1] + ".rotate" + self.twistAxis), (f"{N_root_NegMd}.input2{self.twistAxis}"), f=1 )
        
        # Connect up to the att jnt!
        cmds.connectAttr( (f"{N_root_AttMd}.output{self.twistAxis}"), (f"{self.attJntsLs[-2]}.rotate{self.twistAxis}"), f=1 )
        
        # Connect to the Neg twist for same jnt
        cmds.connectAttr( (f"{N_root_NegMd}.output{self.twistAxis}"), (f"{self.TwistNeg[-2]}.rotate{self.twistAxis}"), f=1 )
        
        '''
        THIS ALWAYS HAPPENS AT THE BEGINNING FOR THE ROOT JNT!
        '''
        #--------------------------------------------------------------------------------------
        # Connect to next joint in the chain! = Neck_01
        #--------------------------------------------------------------------------------------
        #---------------- Connecting the neck children: HOW IT'S WORKING = 
        # Twist moving down the chain: get value from parent att_Md node, 
        # plug that into 2 new att/Neg Md nodes for the current joint working on!
        # create fucntion that does this, so for the amount of neck joints, call this function that many times to 
        # dissiminate the twisting of the neck!
        # (the next chain always comes from the previous att_md node)
        #---------------- 

        # create 2 more MD nodes that both have the same connection from, 
        # The previous neck_02 'N2AttMd'
        # These joints need to get half of the value from it's parent jnt!
        Divisible_value = 2 # i think this is a constant val(alway dividing by two)
        
        # [neck_01, neck_02, neck_03, neck_04, head] - neck just before head is the neck_root! 
        # Everything before 'neck_04' is a list of joints 
        
        full_neck_list = self.attJntsLs[:-1] # removing head jnt 
        neck_children = full_neck_list[:-1] # removing root neck jnt
        neck_children.reverse() # reverse the order because working from head to bottom of neck 

        full_NEG_list = self.TwistNeg[:-1] # removing head jnt 
        NEG_children = full_NEG_list[:-1] # removing root neck jnt
        NEG_children.reverse()
        
        
        # len(neck_children) = number of neck children to work on
        def rest_of_neck_twists():
            neckOrder = create_list_from_integer(len(neck_children))
            neckOrder.reverse()

            order_list = [self.divisibleList[i] for i in range(len(neck_children))]
            for x in range(len(neck_children)):
                
                N_1_AttMd = cmds.shadingNode("multiplyDivide", au=1, n="neck_" + neckOrder[x] + "_att_MD")
                N_1_NegMd = cmds.shadingNode("multiplyDivide", au=1, n="neck_" + neckOrder[x] + "_Neg_MD")

                # Set the att_Md input2X to positive 'Divisible_value' & neg_Md to negative 'Divisible_value'
                cmds.setAttr( (f"{N_1_AttMd}.input2{self.twistAxis}"), order_list[x])
                cmds.setAttr( (f"{N_1_NegMd}.input2{self.twistAxis}"), -order_list[x] )

                # Set Md operation to Divide 
                cmds.setAttr( N_1_AttMd + ".operation", 2 )
                cmds.setAttr( N_1_NegMd + ".operation", 2 )

                cmds.connectAttr( (f"{N_root_AttMd}.output{self.twistAxis}"), (f"{N_1_AttMd}.input1{self.twistAxis}"), f=1 )
                cmds.connectAttr( (f"{N_root_AttMd}.output{self.twistAxis}"), (f"{N_1_NegMd}.input1{self.twistAxis}"), f=1 )

                # Connect to the att & Neg joint!
                cmds.connectAttr( (f"{N_1_AttMd}.output{self.twistAxis}"), (f"{neck_children[x]}.rotate{self.twistAxis}"), f=1 )
                cmds.connectAttr( (f"{N_1_NegMd}.output{self.twistAxis}"), (f"{NEG_children[x]}.rotate{self.twistAxis}"), f=1 )
        rest_of_neck_twists()
        
        #--------------------------------------------------------------------------------------
        # page 4 - page 5 - Jnt_att_neck_1/neck_2 & Jnt_Bending_head
        #--------------------------------------------------------------------------------------
        # bending axis: self.bendAxis = ['Y', 'Z']
        
        # connect bending axis outputs from 'N_root_AttMd' into bend_ratio_MD
        bend_Ratio = cmds.shadingNode("multiplyDivide", au=1, n="neck_bend_ratio_MD")
        cmds.setAttr( bend_Ratio + ".operation", 2 )
        
        # Start with 'N_root_AttMd' - connect beding axis to it
        for i in range(2):
            cmds.connectAttr( (self.ctrlLs[-1] + ".rotate" + self.bendAxis[i]), 
                             (N_root_AttMd + ".input2" + self.bendAxis[i]), f=1
                            )
            cmds.connectAttr( (self.ctrlLs[-1] + ".Neck_Bend_Mult"), (N_root_AttMd + ".input1" + self.bendAxis[i]))
            cmds.setAttr( bend_Ratio + ".input2" + self.bendAxis[i], Divisible_value )
            # connect root_attMD to bend_ratio
            cmds.connectAttr( (N_root_AttMd + ".output" + self.bendAxis[i]), (bend_Ratio + ".input1" + self.bendAxis[i]))
        
        # connect bend_ratio to all neck joints!   
        # ['jnt_att_neck_1', 'jnt_att_neck_2']
        just_neck_jnts = self.attJntsLs[:self.neckAmnt]
        print("only neck joints:", just_neck_jnts )
        for i in range(self.neckAmnt):
            cmds.connectAttr( (bend_Ratio + ".output" + self.bendAxis[0]), (just_neck_jnts[i] + ".rotate" + self.bendAxis[0]))
            cmds.connectAttr( (bend_Ratio + ".output" + self.bendAxis[1]), (just_neck_jnts[i] + ".rotate" + self.bendAxis[1]))

        # for Bending neg: minus the value from 'N_root_AttMd' & 
        # put into the jnt_bend_Neg with 2 pma(sum) node into the right bending axis for the jnt_bend_neg!
        
        bend_UC = [cmds.shadingNode("unitConversion", au=1, n= self.bendAxis[i] + "axis_bend_min_UC") for i in range(2)]
        Axis_pma = [cmds.shadingNode("plusMinusAverage", au=1, n= self.bendAxis[i] + "axis_neg_pma") for i in range(2)]
        print(bend_UC)
        for i in range(2):
            cmds.setAttr( bend_UC[i] + ".conversionFactor", -1 )
            cmds.connectAttr( (N_root_AttMd + ".output" + self.bendAxis[i]), (bend_UC[i] + ".input"), f=1 )
            cmds.connectAttr( (bend_UC[i] + ".output"), (Axis_pma[i] + ".input1D[0]"), f=1 )
            cmds.connectAttr( (Axis_pma[i] + ".output1D"), (self.TwistNeg[-1] + ".rotate" + self.bendAxis[i]), f=1 )
        '''
        '''
jmvs_Neck_systems()


