import maya.cmds as cmds

def collect_jnt_hi(root_joints, system_name):
    print(f"Root joints: {root_joints}")
    return [cr_jnts(root_joint, system_name) for root_joint in root_joints]

def cr_jnts(root_joint, system_name):
    prefix = "jnt"
    joint_prefix = f"{prefix}_{system_name}_"
    print(f"Processing root joint: {root_joint}")

    # make list w/ all transform type descendants of var
    all_descendants = cmds.listRelatives(root_joint, ad=True, type="transform") or []
    if "root" in root_joint:
        all_descendants.append(root_joint)
    all_descendants.reverse()
    print(f"Descendants: {all_descendants}")

    # Determine the side attribute
    side = cmds.getAttr(f"{root_joint}.module_side", asString=True) or ""
    side = "" if side == "None" else side

    if side == "_R":
        print("Processing right side joints")

    # Filter guides
    guide_list = [item for item in all_descendants if "cluster" not in item and "data_" not in item]
    print(f"Filtered guides: {guide_list}")

    # Create joints
    cmds.select(clear=True)
    jnt_nms = []
    for guide in guide_list:
        position = cmds.xform(guide, r=1, q=1, ws=1, t=1)
        jnt_nm = cmds.joint(n=f"{joint_prefix}{guide[6:]}", p=position)
        cmds.matchTransform(jnt_nm, guide)
        cmds.makeIdentity(jnt_nm, a=1, t=0, r=1, s=1)
        cmds.makeIdentity(jnt_nm, a=1, t=0, )
        jnt_nms.append(jnt_nm)

    # Match orientation for the end joint
    if guide_list:
        cmds.joint(f"{joint_prefix}{guide_list[-1][6:]}", edit=True, zso=True, oj="none", ch=True)
        cmds.setAttr(f"{joint_prefix}{guide_list[0][6:]}.overrideEnabled", 1)

    return jnt_nms