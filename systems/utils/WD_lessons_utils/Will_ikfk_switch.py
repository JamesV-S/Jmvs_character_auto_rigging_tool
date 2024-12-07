
import importlib
import maya.cmds as cmds

from systems.utils import (utils)
importlib.reload(utils)

# for each module it'll be good to have an 'arrow' ctrl for ikfk_switch

def cr_ikfk_switch_sys(mdl_switch_ctrl, fk_ctrls, ik_ctrls, fk_joint_list, ik_joint_list, master_guide):
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
    
    utils.cr_node_if_not_exists(util_type=1, node_type="reverse", 
                                node_name=rev_node, set_attrs=None)
    
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
