import maya.cmds as cmds

def collect_jnt_hi(root_joints, system_name):
    jnt_collect = []
    print(f"Root joints: {root_joints}")
    
    for root_joint in root_joints:
        joints = create_joints_from_hierarchy(root_joint, system_name)
        jnt_collect.append(joints)
    
    return jnt_collect

def create_joints_from_hierarchy(root_joint, system_name):
    prefix = "jnt"
    joint_prefix = f"{prefix}_{system_name}_"
    jnt_nms = []
    guide_list = []
    all_descendants = []

    print(f"Processing root joint: {root_joint}")

    # Retrieve all descendants of the root joint
    all_descendants = cmds.listRelatives(root_joint, ad=True, type="transform") or []
    print(f"Descendants: {all_descendants}")

    # Add root joint to the list if it includes "root"
    if "root" in root_joint:
        all_descendants.append(root_joint)
    all_descendants.reverse()

    # Determine the side attribute from the guide
    side_indicator = cmds.getAttr(f"{root_joint}.module_side", asString=True)
    side_indicator = "" if side_indicator == "None" else side_indicator

    if side_indicator == "_R":
        print("Processing right side joints")

    # Filter out unwanted controls
    for item in all_descendants:
        if "cluster" not in item and "data_" not in item:
            guide_list.append(item)
    
    print(f"Filtered guides: {guide_list}")
    guide_names = [name.replace('guide_', '') for name in guide_list]

    cmds.select(clear=True)

    for guide in guide_list:
        position = cmds.xform(guide, q=True, ws=True, t=True)
        jnt_nm = cmds.joint(n=f"{joint_prefix}{guide[6:]}", p=position)
        cmds.matchTransform(jnt_nm, guide)
        cmds.makeIdentity(jnt_nm, apply=True, rotate=True)
        jnt_nms.append(jnt_nm)

    # make end jnt match orientation.
    cmds.joint(f"{joint_prefix}{guide_names[-1]}", edit=True, zso=True, oj="none", ch=True)

    cmds.setAttr(f"{joint_prefix}{guide_names[0]}.overrideEnabled", 1)

    return jnt_nms