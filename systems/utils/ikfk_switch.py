
import importlib
import maya.cmds as cmds
from systems.utils import utils

importlib.reload(utils)

def setup_ikfk_switch(skel_jnts, switch_ctrl, fk_ctrls, ik_ctrls, fk_jnt_names, ik_jnt_names, guide_id):
    #need tthe fk ctrls and fk ctrls together
    controls = fk_ctrls + ik_ctrls
    switch_attribute = 'IKFK_Switch'
    
    # Add switch attribute to the switch_ctrl and proxy it
    utils.add_locked_attrib(ctrl=switch_ctrl, en=["IKFK"])
    utils.add_float_attrib(ctrl=switch_ctrl, flt=[switch_attribute], val=[0, 1], limited=True)
    for control in controls:
        utils.add_locked_attrib(ctrl=control, en=["IKFK"])
        utils.proxy_attr_list(switch_ctrl, control, switch_attribute)
    
    # cr a rev node
    reverse_node_name = f"ReverseNode_{guide_id[6:]}"
    utils.cr_node_if_not_exists(util_type=1, node_type="reverse", node_name=reverse_node_name)
    # con the switch control to the reverse node
    utils.connect_attr(f"{switch_ctrl}.{switch_attribute}", f"{reverse_node_name}.inputX")
    
    # whats th side and axiss for control visbility
    side_indicator = 1 if '_L' in switch_ctrl else 0
    axis = 'X' if side_indicator else 'Y'
    
    for control in controls:
        if 'ctrl_fk' in control:
            utils.connect_attr(f"{switch_ctrl}.{switch_attribute}", f"{control}.visibility")
        elif 'ctrl_ik' in control or 'ctrl_pv' in control:
            utils.connect_attr(f"{reverse_node_name}.outputX", f"{control}.visibility")
    
    # rig jnts:
    for i, joint in enumerate(skel_jnts):
        constraints = cmds.listRelatives(joint, c=1, type="parentConstraint")
        
        if "jnt_fk" in fk_jnt_names[i]:
            utils.connect_attr(f"{switch_ctrl}.{switch_attribute}", f"{constraints[0]}.{fk_jnt_names[i]}W0")
        else:
            print(f"'setup_ikfk_swtch' {fk_jnt_names[i]} doesn't work for conn")
        
        if "jnt_ik" in ik_jnt_names[i]:
            utils.connect_attr(f"{reverse_node_name}.outputX", f"{constraints[0]}.{ik_jnt_names[i]}W1")
        else:
            print(f"'setup_ikfk_swtch' {ik_jnt_names[i]} doesn't work for conn")
    
    # switch dict
    return {
        "ikfk_switch_attribute": switch_attribute,
        "reverse_node": reverse_node_name
    }