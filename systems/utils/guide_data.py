
import maya.cmds as cmds
# Define the type of each attribute that can be stored. 
dict_var_types = {
                "module": "string",
                "master_guide": "string",
                "guide_list": "list",
                "guide_scale": "float",
                "joints": "list",
                "side": "string",
                "connectors": "list",
                "system_to_connect": "list",
                "ik_ctrl_list": "list",
                "fk_ctrl_list": "list",
                "ik_joint_list": "list",
                "fk_joint_list": "list",
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
    
def setup(temp_dict, data_guide):
    for key in temp_dict.keys():
        if key == "guide_number":
            # Add float type attr to data_guide
            cmds.addAttr(data_guide, ln=key, at="float", k=1)
            # The initial value of this attr is set using 'temp_dict[key]'(value of key)
            cmds.setAttr(f"{data_guide}.{key}", temp_dict[key]) 
        
        elif isinstance(temp_dict[key], str):
            # If value of the key is a 'string', an enum attr is added to data_guide. 
            cmds.addAttr(data_guide, ln=key, at="enum", en=temp_dict[key], k=1)
            '''try replace "enum" with "string"'''
        
        elif isinstance(temp_dict[key], list):
            # if valueis a list, checks if list is empty. 
            if len(temp_dict[key]) == 0: 
                enum_list = "empty"
            else:
                # if not, the list is joined into a single string with elements 
                # after colon(:)
                enum_list = ":".join(temp_dict[key])
            # An enum attr is added with the values, as a way to store list data in Maya.
            cmds.addAttr(data_guide, ln=key, at="enum", en=enum_list, k=1)
        
        # if float or int, a float attr is added & value is set.
        elif isinstance(temp_dict[key], float):
            cmds.addAttr(data_guide, ln=key, at="float",k=1)
            cmds.setAttr(f"{data_guide}.{key}", temp_dict[key])
        
        elif isinstance(temp_dict[key], int):
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
    pass
    
    '''
    elif dict_var_types[attr] == "list":
        value_list = cmds.attributeQuery(attr, node=guide, le=1)
        if value_list:
            value = value_list[0].split(":")
            if value == ["empty"]:
                value = []
    '''

