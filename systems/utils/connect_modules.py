import maya.cmds as cmds
from systems.utils import utils
import importlib
importlib.reload(utils)

modules_to_connect = {}
jnts_to_parent = []

def attach(master_guide, selection):
    guide_connector_list = utils.guide_curve_connector(master_guide, selection[0])

    if "grp_guideConnector_clusters" in cmds.ls("grp_guideConnector_clusters"):
        cmds.parent(guide_connector_list, "grp_guideConnector_clusters")
    else:
        cmds.group(guide_connector_list, n="grp_guideConnector_clusters", w=1)

    temp_grp = [master_guide]
    modules_to_connect.update({f"{master_guide}_2_{selection[0]}": temp_grp})

    return [modules_to_connect, guide_connector_list]

def prep_attach_jnts(child_jnt, parent_jnt, need_child):
    if need_child:
        child_jnt = cmds.listRelatives(child_jnt, c=1, type="transform")[0]

    temp_grp = [f"jnt_rig_{child_jnt}", f"jnt_rig_{parent_jnt[0]}"]
    jnts_to_parent.append(temp_grp)

    return [child_jnt, parent_jnt[0]]

def attach_jnts(system_to_be_made, system):
    # 'system_to_be_made' is a dict containing info abt rigging sytems, 
    # including which jnts need to be connected. 
    # 'system' is the prefix of th joint system like rig_ or skn_
    
    # this list below contains the vals 
    to_parent = [key["systems_to_connect"] for key in system_to_be_made.values() if key["systems_to_connect"]]
    for x in to_parent:
        cmds.parent(f"jnt_{system}_{x[0]}", f"jnt_{system}_{x[1]}")

def connect_to_ikfk_switch(p_object, constraint): 
    # Concerning the ik reverse of ikfk switch
    for x in p_object:
        attr_exists = cmds.attributeQuery("ikfk_switch_name", node=x, exists=1)
        if attr_exists:
            ikfk_switch_name = cmds.getAttr(f"{x}.ikfk_switch_name", asString=1)
            try:
                reverse_node = cmds.createNode("reverse", n=f"REV_{ikfk_switch_name}_#")
                cmds.connectAttr(f"{x}.{ikfk_switch_name}", f"{reverse_node}.input1X")
                cmds.connectAttr(f"{reverse_node}.outputX", f"{constraint[0]}.{x}W0")
            except:
                pass
            try:
                cmds.connectAttr(f"{x}.{ikfk_switch_name}", f"{constraint[0]}.{x}W1")
            except:
                pass