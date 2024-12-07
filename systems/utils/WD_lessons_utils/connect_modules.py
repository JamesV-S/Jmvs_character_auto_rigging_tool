import maya.cmds as cmds
from systems.utils import utils
import importlib
importlib.reload(utils)

modules_to_connect = {}
jnts_to_parent = []



def attach(master_guide, selection):
    print(f"{master_guide} << master guide arg")
    print(f"{selection} << master selection")
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
    # including which jnts need to be connected: 'systems_to_connect': ['guide_clavicle_l', 'guide_COG'],
    # 'system' is the prefix of th joint system like rig_ or skn_
    for key in system_to_be_made.values():
        print(f"Structure of each key:{key}") # Check the structure of each key.

    # this list below contains the vals 
    to_parent = [key["systems_to_connect"] for key in system_to_be_made.values() if key["systems_to_connect"]]
    print(f"List of sublists to parent >>: {to_parent}")
    # [['guide_clavicle_l', 'guide_COG'], ['guide_COG']]
    # [['guide_spine_1', 'guide_COG'], ['guide_clavicle_l', 'guide_spine_4'], ['guide_spine_4']]
    
    # Parenting the systems_to_connect aka 'to_parent'
    for x in to_parent:
        if len(x) > 1: # Ignore any sublists with only 1 item in it
            first_element = x[0].replace('guide_', '')
            second_element = x[1].replace('guide_', '')
            print(f"Double Sublist: jnt_{system}_{first_element}"," AND ", f"jnt_{system}_{second_element}")
            cmds.parent(f"jnt_{system}_{first_element}", f"jnt_{system}_{second_element}")
        else: 
            first_element = x[0].replace('guide_', '')
            print(f"Single Sublist: jnt_{system}_{first_element}")


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