
import maya.cmds as cmds
# Define the type of each attribute that can be stored. 
dict_var_types = {
                "module": "string",
                "master_guide": "string",
                "guide_list": "list",
                "guide_scale": "float",
                "joints": "list",
                "side": "string",
                "guide_connectors": "list",
                "systems_to_connect": "list",
                "ik_ctrl_list": "list",
                "fk_ctrl_list": "list",
                "ik_joint_list": "list",
                "fk_joint_list": "list",
                "space_swap": "list",
                "mdl_switch_ctrl_list": "list",
                "guide_number": "float"
            }

#------------------
# Setup() function:
    # Adds attributes to a a given locator(data_guide),
    # based on the types defined in temp_dict.
    # Handles different data types: strings, lists, floats, integers.
    # Sets certain attributes to be locked & hidden from the channel box.

# Each key in the dict represents a attribute name, & 
# its corresponding value determines the the attribute type and initial value.

def flatten_list_of_lists(nested_list):
    flattened = []
    for sublist in nested_list:
        if isinstance(sublist, list):
            flattened.extend(sublist)
    return ":".join(flattened) if flattened else "empty"


def setup(temp_dict, data_guide):
    
    for key in temp_dict.keys():
        
        # print(f"Alpha keys: {key}")

        if key == "guide_number":
            print(f"A guide_number> Adding attribute to: {data_guide}, attribute name: {key}")
            # Add float type attr to data_guide
            cmds.addAttr(data_guide, ln=key, at="float", k=1)
            # The initial value of this attr is set using 'temp_dict[key]'(value of key)
            print("line 40, in setup", f"{data_guide}.{key}", "//", temp_dict[key])
            cmds.setAttr(f"{data_guide}.{key}", float(temp_dict[key])) 
        
        elif isinstance(temp_dict[key], str):
            #print(f"B str> Adding attribute to: {data_guide}, attribute name: {key}")
            # If value of the key is a 'string', an enum attr is added to data_guide. 
            cmds.addAttr(data_guide, ln=key, at="enum", en=temp_dict[key], k=1)
            '''try replace "enum" with "string"'''
        
        elif isinstance(temp_dict[key], list): 
            if key == "space_swap":
                # Handle the space_swap attribute specifically 
                if isinstance(temp_dict[key], list) and all(isinstance(i, list) for i in temp_dict[key]):
                    flattened_value = flatten_list_of_lists(temp_dict[key])
                    print(f"----------- GD SETUP flattend_value of spaceSwap == {flattened_value}")
                    cmds.addAttr(data_guide, ln=key, at="enum", en=flattened_value, k=1)
                else:
                    # handle unexpected format
                    print(f"Warning: sapce_swap is not a list of lists for {data_guide}")
            else:
                if len(temp_dict[key]) == 0: 
                    enum_list = "empty"
                else:
                    enum_list = ":".join(temp_dict[key])
                # An enum attr is added with the values, as a way to store list data in Maya.
                cmds.addAttr(data_guide, ln=key, at="enum", en=enum_list, k=1)
        
        # if float or int, a float attr is added & value is set.
        elif isinstance(temp_dict[key], float):
            #print(f"D float> Adding attribute to: {data_guide}, attribute name: {key}")
            cmds.addAttr(data_guide, ln=key, at="float",k=1)
            print(f"GUIDE DATA isinstance>FLOAT: : : : : : : : :{data_guide}.{key}, {temp_dict[key]}")
            cmds.setAttr(f"{data_guide}.{key}", temp_dict[key])
        
        elif isinstance(temp_dict[key], int):
           print(f"E int> Adding attribute to: {data_guide}, attribute name: {key}")
           if not cmds.objExists(data_guide):
                raise RuntimeError(f"{data_guide} does not exist in the scene.")
           #print()
           cmds.addAttr(data_guide, ln=key, at="float",k=1)
           cmds.setAttr(f"{data_guide}.{key}", temp_dict[key])
        
        # Lock & hide the standard transform attrs in channel box. 
        for attr in ["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"]:
            cmds.setAttr(f"{data_guide}.{attr}", cb=0, k=0, l=1)

#---------------------
# init_data() function:
    # searches the scene for existing guides with a locator with a 
    # specific naming convention (data_*).
    # Retrieves & stores attribute values in a dictionary for each guide found. 

# Potential fixes:
    # Make sure list types are correctly interpreted and split using attribute values


def init_data():
    return_dict = {}
    data_guides = cmds.ls("data_*", type="transform")
    print(f"Data Guides found in scene: {data_guides}")
    for guide in data_guides:
        temp_dict = {}
        attr_list = cmds.listAttr(guide, r=1, k=1)
        for attr in attr_list:
            if dict_var_types[attr] == "guide_number":
                pass
            elif dict_var_types[attr] == "list":
                value_list = cmds.attributeQuery(attr, node=guide, le=1)
                if value_list:
                    value = value_list[0].split(":")
                    if value == ["empty"]:
                        value = []
            elif dict_var_types[attr] == 'string':
                value = cmds.getAttr(F"{guide}.{attr}", asString=1)
            elif dict_var_types[attr] == 'float' or dict_var_types[attr] == "long":
                value = cmds.getAttr(F"{guide}.{attr}")
            

            '''elif isinstance(value, list) and value[0] == "empty": 
                value = []'''
            temp_dict[attr] = value
        return_dict[guide] = temp_dict
    return return_dict
            

