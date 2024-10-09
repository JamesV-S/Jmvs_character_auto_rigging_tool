import maya.cmds as cmds 


def add_float_attrib(ctrl, flt, val, limited):
    MinVal = val[0]
    MaxVal = val[1]
    
    for target in [ctrl]:
        for attr in flt:
            if not cmds.attributeQuery(attr, node=target, exists=True):
                if limited:                            
                    cmds.addAttr(target, longName=attr, at='double', dv=MinVal, 
                                min= MinVal, max = MaxVal)
                    cmds.setAttr(f"{target}.{attr}", e=1, k=1 )
                else:
                    cmds.addAttr(target, longName=attr, at='double', dv=0, 
                                )
                    cmds.setAttr(f"{target}.{attr}", e=1, k=1 )
            else:
                print(f"Attribute {attr} already exists on {target}")

def add_locked_attrib(ctrl, en):
    dividerNN = "------------" 
    atrrType = "enum"
    
    for attr in en:
        # Generate the long name for the attribute
        ln = f"{attr.lower()}_dvdr"

        #check if the attribute already exists
        if not cmds.attributeQuery(ln, node=ctrl, exists=True):
            try:
                # add the attributes
                cmds.addAttr(ctrl, longName=ln, niceName=dividerNN, 
                            attributeType=atrrType, enumName=attr, k=True
                            )
                
                cmds.setAttr(f"{ctrl}.{ln}", lock=True, keyable=False, 
                            channelBox=True
                            )
                print(f"Added locked attr {attr} on {ctrl}")
            except Exception as e:
                print(f"Failed to add locked attr {attr} on {ctrl}: {e}")
        else:
            print(f"Attribute {attr} already exists on {ctrl}")

def add_multile_enum_attribute(ctrl, enum_long_name, enum_name_options):
    # ctrl = cmds.ls(sl=1, type="transform")
    if not cmds.attributeQuery(enum_long_name, node=ctrl, exists=True):
        try:
            cmds.addAttr(longName=enum_long_name, at="enum", enumName=enum_name_options)
            cmds.setAttr(f"{ctrl}.{enum_long_name}", e=1, k=1)
        except Exception as e:
            print(f"Failed to add multiple_choice enum attr {enum_long_name} on {ctrl}: {e}" )
    else: 
        print(f"Attribute {enum_long_name} a;ready exists on {ctrl}")

def get_selection_trans_rots_dictionary():
    selection = cmds.ls(sl=1, type="transform")
    
    translation_pos = {}
    rotation_pos = {}
    
    for sel in selection:
        trans_ls = cmds.getAttr(f"{sel}.translate")[0]
        rot_ls = cmds.getAttr(f"{sel}.rotate")[0]
        
        translation_pos[sel] = trans_ls
        rotation_pos[sel] = rot_ls
        
    print("Trans dictionary: ", translation_pos)
    print("Rots dictionary: ", rotation_pos)
    
    return translation_pos, rotation_pos
   
# get_selection_trans_rots_dictionary()

system_pos = {"spine_1": [0,150,0],"spine_2": [0, 165, 3.771372431203975],"spine_3": [0, 185, 6.626589870023061],"spine_4": [0, 204, 5.4509520093959845],"spine_5": [0.0, 231.0, 0.0150903206755304]}
system_rot = {"spine_1": [13.832579598094327, 0, 0],"spine_2":[8.04621385323777, 0, 0],"spine_3":[-3.330793760291316, 0, 0],"spine_4":[-11.225661138926666, 0, 0],"spine_5":[0,0,0]}

def set_transformations(translation_dict, rotation_dict):
    for obj in translation_dict:
        # check if object exists in scene
        if not cmds.objExists(obj):
            print(f"Object: '{obj}' doesn't exist in the scene")
            continue

        current_trans = cmds.getAttr(f"{obj}.translate")[0]
        current_rot = cmds.getAttr(f"{obj}.rotate")[0]

        # check if the object is alreadyu at the specified positions
        if current_trans == translation_dict[obj] and current_rot == rotation_dict[obj]:
            print(f"Object: '{obj}' is already in the specified position")
            continue

        # Set the trans & rot values
        cmds.setAttr(f"{obj}.translate", *translation_dict[obj])
        cmds.setAttr(f"{obj}.rotate", *rotation_dict[obj])
        print(f"Set the trans & rot values for '{obj}' ")

# set_transformations(system_pos, system_rot)

def guide_curve_connector(first_jnt, second_jnt):
    fst_point_loc = cmds.xform(first_jnt ,q=1, ws=1, rp=1)
    scnd_point_loc =  cmds.xform(second_jnt ,q=1, ws=1, rp=1)

    curve_name = f"crv_{first_jnt}"
    cmds.curve(d=1, p=[fst_point_loc, scnd_point_loc], n=curve_name)

    cluster_1 = cmds.cluster(f"{curve_name}.cv[0]", n=f"cluster_crv_{first_jnt}_cv0")
    cluster_2 = cmds.cluster(f" {curve_name}.cv[1]", n=f"cluster_crv_{second_jnt}_cv0")

    cmds.parent(cluster_1, first_jnt)
    cmds.parent(cluster_2, second_jnt)
    print("Going to hid clusters & template the connector")
    
    for x in cmds.ls(typ="cluster"):
        cmds.hide(f"{x}Handle")
        cmds.setAttr(f"{x}Handle.hiddenInOutliner", True)
            
    cmds.setAttr(f"{curve_name}.template", 1)
    cmds.select(cl=1)

    return curve_name

def find_substring_in_life(string, substrings):
    for substring in substrings:
        if substring in string:
            return substring
        
def colour_guide_custom_shape(custom_crv):
    # Firstly, from the 'custom_crv' select all shapes in it & set their overrideEnabled!
    shape_list = cmds.listRelatives(custom_crv, shapes=1)
    for shape in shape_list:
        cmds.setAttr(f"{shape}.overrideEnabled", 1)
        
    # Create lists for shapes with specific patterns in their names!
    yellow_shape = [shape for shape in shape_list if custom_crv in shape]
    for shape in yellow_shape:
        cmds.setAttr(f"{shape}.overrideColor", 22) # 17

    red_shape = [shape for shape in shape_list if "X" in shape]
    for shape in red_shape:
        cmds.setAttr(f"{shape}.overrideColor", 13)

    green_shape = [shape for shape in shape_list if "Y" in shape]
    for shape in green_shape:
        cmds.setAttr(f"{shape}.overrideColor", 14)

    blue_shape = [shape for shape in shape_list if "Z" in shape]
    for shape in blue_shape:
        cmds.setAttr(f"{shape}.overrideColor", 6)

    black_shape = [shape for shape in shape_list if "guidePivot" in shape]
    for shape in black_shape:
        cmds.setAttr(f"{shape}.overrideColor", 1)

# colour_custom_shape("crv_custom_guide")

def colour_COG_control(custom_crv):
    
    # Firstly, from the 'custom_crv' select all shapes in it & set their overrideEnabled!
    shape_list = cmds.listRelatives(custom_crv, shapes=1)
    for shape in shape_list:
        cmds.setAttr(f"{shape}.overrideEnabled", 1)
        cmds.setAttr(f"{shape}.overrideColor", 18)
        
    # Create lists for shapes with specific patterns in their names!
    grey_shape = [shape for shape in shape_list if "kite" in shape]
    for shape in grey_shape:
        cmds.setAttr(f"{shape}.overrideColor", 3)
# colour_COG_control("ctrl_COG")

def colour_root_control(custom_crv):
    
    # Firstly, from the 'custom_crv' select all shapes in it & set their overrideEnabled!
    shape_list = cmds.listRelatives(custom_crv, shapes=1)
    for shape in shape_list:
        cmds.setAttr(f"{shape}.overrideEnabled", 1)
        cmds.setAttr(f"{shape}.overrideColor", 17)
        
    # Create lists for shapes with specific patterns in their names!
    white_shape = [shape for shape in shape_list if "white" in shape]
    for shape in white_shape:
        cmds.setAttr(f"{shape}.overrideColor", 16)
# colour_root_control("ctrl_root")

