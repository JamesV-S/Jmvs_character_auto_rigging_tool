
import maya.cmds as cmds

def get_joint_list(skeleton_roots, system):
    jnts_list = []
    print(f"JOINTS, skeleton_roots == {skeleton_roots}")
    for top_skeleton_joint in skeleton_roots:
        # Implement name check for unique naming
        # The name concerning the guides list provided, so there are no duplicates! 
        joint_list = joint(top_skeleton_joint, system)
        jnts_list.append(joint_list)
    
    return jnts_list

def joint(top_skeleton_joint, system):
    prefix = "jnt"
    jnt_tag = f"{prefix}_{system}_"
    jnt_names = []
    list_ctrls = []
    list = []
    print(f"JOINTS, top_top_skeleton_joint == {top_skeleton_joint}")
    # make list w/ all transform type descendants of var
    print(f"systems>joints.py(joint) the list is: {list}")
    list = cmds.listRelatives(top_skeleton_joint, ad=1, type="transform")
    

    # If top_skeleton_joint contains "root" append it to the list
    if "root" in top_skeleton_joint:
        list.append(top_skeleton_joint)
    # Do the same for the finger master's
    '''
    elif "proximal" in top_skeleton_joint:
        list.append(top_skeleton_joint)
    '''
    list.reverse()

    # determine the side from attr on guide!
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
    
    name_list_ctrls = [guide_name.replace('guide_', '') for guide_name in list_ctrls]
    #print(f"LIST OF CONTRLSSS >>>> {list_ctrls}")

    # ['guide_root', 'guide_COG']
   

    # Joint creation: 
    cmds.select(cl=1)
    for locator in list_ctrls:
        # get locator location
        loc = cmds.xform(locator, r=1, ws=1, q=1, t=1)
        #print(f"guides xform's: {loc}")
        # create joint based off the location
        jnt_name = cmds.joint(n=f"{jnt_tag}{locator[6:]}",) # remove 'guide' from name!
        cmds.matchTransform(jnt_name, locator)
        cmds.makeIdentity(jnt_name, a=1, t=0, r=1, s=1)
        cmds.makeIdentity(jnt_name, a=1, t=0, )
        #makeIdentity -apply true -t 0 -r 0 -s 1 -n 0 -pn 1
        jnt_names.append(jnt_name)
    
    # I'm matching the joint's to the guides instead ofg orientaing them!
    '''
    mirror_attribute = cmds.getAttr(f"{top_skeleton_joint}.module_orientation", asString=1)
    print(f"ZZZZZZZZZZZZZZZZZZZ what's the name {top_skeleton_joint}.module_orientation")
    print(f"ORI Attr is >> {mirror_attribute}") 
    
    # if mirroring it:
    if mirror_attribute == "XYZ": # used to be 'Yes'
        sao_axis = f"{orientation}down" # xdown
    else:
        sao_axis = f"{orientation}up" # xup

    # Orient the joint
    # Y tf orient the joint if it's matching the guides??
    cmds.joint(f"{jnt_tag}{list_ctrls[0]}", edit=1, zso=1, oj=orientation, sao=sao_axis, ch=1)
    '''

    # Orient endjoint to world
    cmds.joint(f"{jnt_tag}{name_list_ctrls[-1]}", edit=1, zso=1, oj="none", ch=1)

    cmds.setAttr(f"{jnt_tag}{name_list_ctrls[0]}.overrideEnabled", 1)
    
    return jnt_names
