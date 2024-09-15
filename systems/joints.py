
import maya.cmds as cmds

def get_joint_list(orientation, skeleton_roots, system):
    jnts_list = []

    for top_skeleton_joint in skeleton_roots:
        # Implement name check for unique naming
        # The name cpncerning the guides list provided, so there are no duplicates!
        #  
        joint_list = joint(orientation, top_skeleton_joint, system)
        jnts_list.append(joint_list)
    
    return jnts_list

def joint(orientation, top_skeleton_joint, system):
    orientation = []
    prefix = "jnt"
    jnt_tag = f"{prefix}_{system}_"
    jnt_names = []
    list_ctrls = []
    list = []

    list = cmds.listrelatives(top_skeleton_joint, ad=1, type="transform")
    
    # If top_skeleton_joint contains "root" append it to the list
    if "root" in top_skeleton_joint:
        list.append(top_skeleton_joint)
    # Do the same for the finger master's
    '''
    elif "proximal" in top_skeleton_joint:
        list.append(top_skeleton_joint)
    '''
    list.reverse()

    # determine the side
    side = cmds.getAttr(f"{top_skeleton_joint}.module_side", asString=1)
    if side == "None":
        side = ""
    
    # Creatre the list of controls for future while
    # Filtering out any controls with a 'cluster' or 'data_', adding rest to list controls
    for x in list:
        if "cluster" in x or "data_" in x:
            pass
        else:
            list_ctrls.append(x)

    # Joint creation: 
    cmds.select(cl=1)
    for locator in list_ctrls:
        # get locator location
        loc = cmds.xform(locator, r=1, ws=1, q=1, t=1)
        # create joint based off the location

    mirror_attribute = cmds.getAttr(f"{top_skeleton_joint}.module_orientation", asString=1)
    if mirror_attribute == "Yes":
        sao_axis = f"{orientation[0]}down"
    else:
        sao_axis = f"{orientation[0]}up"

    # Orient the joint
    cmds.joint(f"{jnt_tag}{list_ctrls[0]}", edit=1, zso=1, oj=orientation, sao=sao_axis, ch=1)

    # Orient endjoint to world
    cmds.joint(f"{jnt_tag}{list_ctrls[-1]}", edit=1, zso=1, oj="none", ch=1)

    cmds.setAttr(f"{jnt_tag}{list_ctrls[0]}.overrideEnabled", 1)
    
    return jnt_names
