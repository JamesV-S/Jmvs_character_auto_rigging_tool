system = ["neck_1", "neck_2", "neck_3"]
# XYZ
system_pos_xyz = {'neck_1': [0.0, 240, 0.0], 
                  'neck_2': [0.0, 250, 0.0], 
                  'neck_3': [0.0, 260, 0.0]}

system_rot_xyz = {'neck_1': [0.0, 0.0, 90.0], 
                  'neck_2': [0.0, 0.0, 90.0], 
                  'neck_3': [0.0, 0.0, 90.0]}

# YZX
system_pos_yzx = {'neck_1': [0.0, 240, 0.0], 
                  'neck_2': [0.0, 250, 0.0], 
                  'neck_3': [0.0, 260, 0.0]}

system_rot_yzx = {'neck_1': [0.0, 0.0, 0.0], 
                  'neck_2': [0.0, 0.0, 0.0], 
                  'neck_3': [0.0, 0.0, 0.0]}

# Have a module that has name of guides: 'system' each with their own

has_orientation = "yes"

ik_joints = {
    "start_joint": system[0],
    "end_joint": system[-1], 
    "pv_joint": None,
    "top_joint": system[0], 
    "world_orientation": False
}

twist_joint = "None"

# If axis_orientation = a specific axis, use that specified system_pos
side = "None"
stretch = False

guide_scale = 0.5
available_rig_types = ["FK", "IK", "IKFK"] # Add ribbon in future!
default_ctrl_shape = {
    f"fk_{system[-1]}": "circle", 
    f"ik_{system[-1]}": "cube"
} # Have fk as circle, ik as cube & ribbon as octagon. 


# Need to split it up: Clav, PV, master[wrist]
# space_swapping = [["world", "COG", "shoulder", "custom"], ["world", "wrist"], ["world", "James"]]
space_swapping = []