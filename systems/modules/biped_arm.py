system = ["clavicle", "shoulder", "elbow", "wrist"]
# XYZ
system_pos_xyz = {'clavicle': [3.9705319404602006, 230.650634765625, 2.762230157852166], 
               'shoulder': [25.234529495239258, 225.57975769042972, -12.279715538024915], 
               'elbow': [49.96195602416994, 192.91743469238278, -8.43144416809082], 
               'wrist': [72.36534118652347, 164.23757934570304, 15.064828872680739]}
system_rot_xyz = {'clavicle': [-7.698626118758961, 34.531672095102785, -13.412947865931349], 
               'shoulder': [7.042431639335459, -5.366417614476926, -52.87199475566795], 
               'elbow': [3.4123575630188263, -32.847391136978814, -52.004681579832734], 
               'wrist': [3.4123575630188263, -32.847391136978814, -52.004681579832734]}

# YZX
system_pos_yzx = {'clavicle': [3.970531940460202, 230.65063476562497, 2.762230157852178], 
               'shoulder': [25.234529495239247, 225.5797576904297, -12.279715538024897], 
               'elbow': [49.96195602416995, 192.9174346923828, -8.431444168090792], 
               'wrist': [72.3653420762656, 164.2375841027702, 15.064833830859115]}
system_rot_yzx = {'clavicle': [-101.01687892466634, -54.72478122395497, 0.0], 
                  'shoulder': [38.44191942754821, -81.34821938773749, 179.00497225409262], 
                  'elbow': [84.72265733457102, -56.99499092973047, 134.2807120402011], 
                  'wrist': [84.72265733457102, -56.99499092973047, 134.2807120402011]}

has_orientation = "yes"

ik_joints = {
    "start_joint": "shoulder",
    "end_joint": "wrist", 
    "pv_joint": "elbow",
    "top_joint": "clavicle", 
    "world_orientation": False
}

# If axis_orientation = a specific axis, use that specified system_pos
side = "_L"
stretch = True

guide_scale = 1
available_rig_types = ["FK", "IK", "IKFK"] # Add ribbon in future!
space_swapping = [["world", "COG", "shoulder", "custom"], ["world", "wrist"], ["world", "clavicle"], ["world", "spine"]]