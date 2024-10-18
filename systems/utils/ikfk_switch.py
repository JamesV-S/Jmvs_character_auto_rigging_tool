
import importlib
import maya.cmds as cmds

from systems.utils import (utils)
importlib.reload(utils)

# for each module it'll be good to have an 'arrow' ctrl for ikfk_switch

def cr_ikfk_switch_sys(rig_joints, mdl_switch_ctrl, fk_ctrls, ik_ctrls, fk_joint_list, ik_joint_list, master_guide):
    collected_ctrls = fk_ctrls + ik_ctrls
    switch_Attr = 'ik_fk_Switch'
    
    # Add attr to 'mdl_switch_ctrl' & proxy it
    utils.add_locked_attrib(ctrl=mdl_switch_ctrl, en=["IKFK"])
    utils.add_float_attrib(ctrl=mdl_switch_ctrl, flt=[switch_Attr], 
                           val=[0 ,1], limited=True)
    # utils.add_locked_attrib(ctrl=fk_ctrls, en=["IKFK"])
    for ctrl in range(len(collected_ctrls)):
        utils.add_locked_attrib(ctrl=collected_ctrls[ctrl], en=["IKFK"])
        utils.proxy_attr_list(mdl_switch_ctrl, collected_ctrls[ctrl], switch_Attr)
    
    # create reverse node
    rev_node = f"REV_ik{master_guide[6:]}"
    yh = utils.cr_node_if_not_exists(util_type=1, node_type="reverse", 
        node_name=rev_node, set_attrs=None
        )
    
    # Connections for ctrls:
    utils.connect_attr(f"{mdl_switch_ctrl}.{switch_Attr}", f"{rev_node}.inputX")
    
    # output x for '_L'
    if '_L' in mdl_switch_ctrl or '_R' in mdl_switch_ctrl:
        if mdl_switch_ctrl[-2:] == '_L':
            side = 1
        else: 
            side = 0

    axis_val = 'X'
    if side == True: # left side
        axis_val = 'X'
    else:
        axis_val = 'Y'
    
    print("AXIS VALUE IS ",  axis_val)
    for ctrl in collected_ctrls:
        if 'ctrl_fk' in ctrl:
            utils.connect_attr(f"{mdl_switch_ctrl}.{switch_Attr}", f"{ctrl}.visibility")
        elif 'ctrl_ik' in ctrl or 'ctrl_pv' in ctrl:      
            utils.connect_attr(f"{rev_node}.output{axis_val}", f"{ctrl}.visibility")
        
    
    # create joint connections:
    for x in range(len(rig_joints)):
        rig_jnt_Pcons = cmds.listRelatives(rig_joints[x], c=1, type="parentConstraint")
        if "jnt_fk" in fk_joint_list[x]:
            utils.connect_attr(f"{mdl_switch_ctrl}.{switch_Attr}", f"{rig_jnt_Pcons[0]}.{fk_joint_list[x]}W0")
        else:
            cmds.warning(f"{fk_joint_list[x]} doesn't contain jnt_fk joints!")
        if "jnt_ik" in ik_joint_list[x]:
            utils.connect_attr(f"{rev_node}.output{axis_val}", f"{rig_jnt_Pcons[0]}.{ik_joint_list[x]}W1")
          
        else:
            cmds.warning(f"{ik_joint_list[x]} doesn't contain jnt_ik joints!")
    
    ikfk_switch_dict = {
        "ikfk_switch_name": switch_Attr, 
        "reverse_node": rev_node
    }

    return ikfk_switch_dict