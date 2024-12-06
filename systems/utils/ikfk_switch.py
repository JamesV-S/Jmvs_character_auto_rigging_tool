
import importlib
import maya.cmds as cmds
from systems.utils import utils

importlib.reload(utils)

def setup_ikfk_switch(skeleton_joints, switch_control, fk_controls, ik_controls, fk_joint_names, ik_joint_names, guide_id):
    #need tthe fk ctrls and fk ctrls together
    controls = fk_controls + ik_controls
    switch_attribute = 'IKFK_Switch'
    
    # Add switch attribute to the switch_control and proxy it
    utils.add_locked_attrib(ctrl=switch_control, en=["IKFK"])
    utils.add_float_attrib(ctrl=switch_control, flt=[switch_attribute], val=[0, 1], limited=True)
    for control in controls:
        utils.add_locked_attrib(ctrl=control, en=["IKFK"])
        utils.proxy_attr_list(switch_control, control, switch_attribute)
    
    # cr a rev node
    reverse_node_name = f"ReverseNode_{guide_id[6:]}"
    utils.cr_node_if_not_exists(util_type=1, node_type="reverse", node_name=reverse_node_name)
    # con the switch control to the reverse node
    utils.connect_attr(f"{switch_control}.{switch_attribute}", f"{reverse_node_name}.inputX")
    
    # whats th side and axiss for control visbility
    side_indicator = 1 if '_L' in switch_control else 0
    axis = 'X' if side_indicator else 'Y'
    
    for control in controls:
        if 'ctrl_fk' in control:
            utils.connect_attr(f"{switch_control}.{switch_attribute}", f"{control}.visibility")
        elif 'ctrl_ik' in control or 'ctrl_pv' in control:
            utils.connect_attr(f"{reverse_node_name}.outputX", f"{control}.visibility")
    
    # rig jnts:
    for i, joint in enumerate(skeleton_joints):
        constraints = cmds.listRelatives(joint, c=1, type="parentConstraint")
        
        if "jnt_fk" in fk_joint_names[i]:
            utils.connect_attr(f"{switch_control}.{switch_attribute}", f"{constraints[0]}.{fk_joint_names[i]}W0")
        else:
            cmds.warning(f"FK joint {fk_joint_names[i]} is not valid for connection!")
        
        if "jnt_ik" in ik_joint_names[i]:
            utils.connect_attr(f"{reverse_node_name}.outputX", f"{constraints[0]}.{ik_joint_names[i]}W1")
        else:
            cmds.warning(f"IK joint {ik_joint_names[i]} is not valid for connection!")
    
    # switch dict
    return {
        "ikfk_switch_attribute": switch_attribute,
        "reverse_node": reverse_node_name
    }