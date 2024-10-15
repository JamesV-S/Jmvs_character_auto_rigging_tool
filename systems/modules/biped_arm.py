system = ["clavicle", "shoulder", "elbow", "wrist"]
# XYZ
system_pos_xyz = {'clavicle': [3.970531940460205, 230.650634765625, 2.762230157852173], 
               'shoulder': [25.234529495239258, 225.5797576904297, -12.279715538024902], 
               'elbow': [49.96195602416992, 192.9174346923828, -8.431444168090811], 
               'wrist': [72.36534118652347, 164.23757934570307, 15.064828872680712]}
system_rot_xyz = {'clavicle': [-7.698626118758958, 34.53167209510278, -13.412947865931354], 
               'shoulder': [7.042431639335463, -5.366417614476936, -52.87199475566794], 
               'elbow': [3.4123575630188383, -32.84739113697883, -52.00468157983275], 
               'wrist': [5.910977623767564, -31.08347450391755, -56.62585344811802]}

# YZX
system_pos_yzx = {'clavicle': [3.970531872957107, 230.65063106134636, 2.762230155677427], 
                   'shoulder': [25.234528808345978, 225.57975007147127, -12.27971552775892], 
                   'elbow': [49.96195619301185, 192.9174288786766, -8.431443981071228], 
                   'wrist': [72.36533758489891, 164.23758425486227, 15.064829130333644]}
system_rot_yzx = {'clavicle': [-101.01687892466632, -54.72478122395495, 5.507410321288293e-15], 
                   'shoulder': [-141.5580805724518, -98.65178061226251, -0.9950277459073927], 
                   'elbow': [-98.6018889461081, -123.26924247955515, -41.749524068095575], 
                   'wrist': [-102.45027734434979, -122.01516904948454, -41.245246906475195]}

has_orientation = "yes"

ik_joints = {
    "start_joint": "shoulder",
    "end_joint": "wrist", 
    "pv_joint": "elbow", 
    "world_orientation": False
}

twist_joint= {
    "start": "shoulder",
    "end": "wrist", 
}

# If axis_orientation = a specific axis, use that specified system_pos
side = "_L"
stretch = True
space_swapping = ["shoulder","root","COG","Custom"]
guide_scale = 1
available_rig_types = ["FK", "IK", "IKFK"] # Add ribbon in future!
default_ctrl_shape = {
    "fk_wrist": "circle", 
    "ik_wrist": "cube"
} # Have fk as circle, ik as cube & ribbon as octagon. 

'''
module files do not use defined functions because blueprint guides 
prioritize a visual, modular, and attribute-driven approach that imporoves 
flexibility, ease of use, and automation in the rigging process. This method 
allows me to efficiently create and customize complex rig 
systems without delving into the intricacies of coding functions.
'''