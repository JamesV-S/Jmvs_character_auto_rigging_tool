import maya.cmds as cmds 
import importlib
# module imports----------------------------------------------------------
import BQ_Almb_removePref_mdl as rmv_pref
import BQ_Almb_addPref_mdl as add_pref
import OPM
# Reload the modules
importlib.reload(rmv_pref)
importlib.reload(add_pref)
importlib.reload(OPM)



def ctrl_root_support(mult_node, rt_obj):
    # Connect rt_obj(world[0]) to MultMatrix,
    # Connect root_ctrl(inverse[0]) to MultMatrix
    cmds.connectAttr( (rt_obj + ".worldMatrix[0]"), 
                     (mult_node + ".matrixIn[0]" ), f=1
                    )
    cmds.connectAttr( ( "ctrl_root.worldInverseMatrix[0]"),
                     (mult_node + ".matrixIn[1]"), f=1
                    )
    cmds.select(cl=1)

def Deslect():
    cmds.select(cl=1)

axis_ls = ['X', 'Y', 'Z']

# Do you want to select soemthing first before running script?
# Check the selection is valid
selCheck = cmds.ls(sl=1, type="transform")

# Error check to make sure a joint is selected
if not selCheck:
    cmds.error("Please select the tail root joint!.")
else:
    tail_root_jnt = cmds.ls(sl=1, type="transform")[0]
#tail_root_jnt = "jnt_att_tail_01"

tailFolder = cmds.group( n=("grp_sys_tail"), em=1 )
cmds.parent( tailFolder, "rig_systems" )
Deslect()


def tail_rt_follow_spine():
    # Create a locator to act as the arm's rootPosition 
    cmds.spaceLocator( n='loc_tail_rtPosition')
    #LegORArm + '_root_position' + whichSide
    LOClimbRoot = 'loc_tail_rtPosition'
    #cmds.setAttr(LOClimbRoot)
    
    IKwspc = cmds.group( n=("tail_IK_Wspace"), em=1 )
    FKwspc = cmds.group( n=("tail_FK_Wspace"), em=1 )

    def rt_locator():
        '''
        for i in range(len(axis_ls)):
            cmds.setAttr( (LOClimbRoot + ".localScale" + axis_ls[i] ), 8 )
        '''
        cmds.matchTransform( LOClimbRoot, tail_root_jnt )
        tailLocGrp = "grp_ctrl_tail"
        cmds.parent( LOClimbRoot, tailLocGrp )
        OPM.OpmCleanTool()
        Deslect()
        # Set colour of Locator
        cmds.setAttr((LOClimbRoot + ".overrideEnabled"), 1)
        cmds.setAttr((LOClimbRoot + ".overrideColor"), 17)
        Deslect()
    rt_locator()
    
    #----------------------------
    # Store limb_rootposition with a grpNode//This soesn't do shit yet, 
    # but it might be usefuol for HEAD_ORIENT down the line.
    cmds.group(n=( "tail_root_Wspace" ), em=1) 
    tailRtWspc = "tail_root_Wspace" 
    
    OPM.OpmCleanTool()
    
    def connecting_to_tail_jnt(): 

        # Connect loc_limb_position to jnt_att_tail_01!!!
        cmds.connectAttr( (LOClimbRoot + ".worldMatrix[0]"), 
                        (tail_root_jnt + ".offsetParentMatrix"), 
                        f=1 
                        )
        cmds.connectAttr( (LOClimbRoot + ".worldMatrix[0]"), 
                        (tailRtWspc + ".offsetParentMatrix"),
                        f=1
                        ) # Use for Head Orient?

    connecting_to_tail_jnt()
    
    def fixing_limb_root_Vals():
        #axis_ls = ['X', 'Y', 'Z']
        for i in range(len(axis_ls)):
            cmds.setAttr( tail_root_jnt + ".translate" + axis_ls[i], 0 )
            cmds.setAttr( tail_root_jnt + ".jointOrient" + axis_ls[i], 0 )
    fixing_limb_root_Vals()

    #---------------------------------------------------------------------------------
    # MAKE ARM/LEG FOLLOW THE SPINE!
    # follow how to do this method from page 5 of ur 'rigging in maya fklimbs notes'!
    
    def limb_fol_spine_sys(ctrl_IK_parent, ctrl_FK_parent,):
        
        # Put ik/fk_jnts & wspace_grp into limbGrp
        cmds.parent(tail_root_jnt, tailRtWspc, tailFolder)
                    
        # Match transforms&rotations of both grps to limbrootPosition
        cmds.matchTransform( IKwspc, FKwspc, LOClimbRoot )
        
        # Parent correct ik/fkwspac_grp to SPINE_ik/fk_ctrl
        
        cmds.parent( IKwspc, ctrl_IK_parent )
        cmds.parent( FKwspc, ctrl_FK_parent )
                        
        #cmds.select( IKwspc, FKwspc )
        OPM.OpmCleanTool()
        Deslect()
    limb_fol_spine_sys('ctrl_ikctrl_pelvis_0', 'ctrl_fk_pelvis_0')
    

    def Spine_ikfk_blnd_support(): #//// NODES before locator!
            # We want limb to blend betweenthses two shoulder grps, 
            # when animator blends between ik&fk , limb moves to correct spine.
            #'LOClimbRoot' will work as the 'arm_root_ctrl'
            
            cmds.shadingNode( "blendMatrix", au=1, n=("spine_ikfk_blend") )
            spine_blend = "spine_ikfk_blend"
           
            #connect COG ikfkSWITCH attrib to blend envolope
            cmds.connectAttr( "ctrl_COG.ik_fk_Switch",
                             (spine_blend + ".envelope" ),f=1
                             )
            
            # Connect blend node to locator leg/arm root positon
            cmds.connectAttr( (spine_blend + ".outputMatrix" ),
                            (LOClimbRoot + ".offsetParentMatrix" ),
                            f=1 
                            )
        
            # Correct the doubletransform issue when move root_ctrl
            multMtxIK = cmds.shadingNode( "multMatrix", au=1,
                                        n=(("tail_root_ik_multMtx"))
                                        )
            multMtxFK = cmds.shadingNode( "multMatrix", au=1,
                                        n=(("tail_root_fk_multMtx"))
                                        )
            
            #ik wspace to ik multMTX (+ctrl_root)
            cmds.connectAttr( (IKwspc + ".worldMatrix[0]" ), 
                             (multMtxIK + ".matrixIn[0]" ), f=1
                            )
            cmds.connectAttr( ("ctrl_root.worldInverseMatrix[0]"),
                              (multMtxIK + ".matrixIn[1]" ), f=1
                            )
            
            #fk wspace to fk multMTX (+ctrl_root)
            cmds.connectAttr( (FKwspc + ".worldMatrix[0]" ),
                             (multMtxFK + ".matrixIn[0]" ), f=1
                            )
            cmds.connectAttr( ("ctrl_root.worldInverseMatrix[0]"),
                             (multMtxFK + ".matrixIn[1]" ), f=1
                            )
            
            # Connect ik/fk multMTX to ikfkblend
            cmds.connectAttr( (multMtxIK + ".matrixSum" ),
                             (spine_blend + ".inputMatrix" ), f=1
                            )
            cmds.connectAttr( (multMtxFK + ".matrixSum" ),
                             (spine_blend + ".target[0].targetMatrix" ), f=1
                            )
                   
    Spine_ikfk_blnd_support()
tail_rt_follow_spine()


