system = ["hip", "knee", "ankle", "ball", "toe"]
# XYZ
system_pos_xyz = {'hip': [16.036325454711914, 147.7965545654297, 0.051486290991306305], 
                   'knee': [20.133201599121104, 82.05242919921866, -0.4505884051322898], 
                   'ankle': [24.197132110595703, 12.625909805297809, -3.493209123611452], 
                   'ball': [24.084232330322262, -1.2434497875801753e-14, 17.988098144531257], 
                   'toe': [24.084232330322276, -1.1379786002407858e-14, 29.18881988525391]}
system_rot_xyz = {'hip': [-0.206856730062026, 0.4367008200374581, -86.43419733389054], 
                   'knee': [-0.20685673006202596, 0.43670082003745814, -86.43419733389054], 
                   'ankle': [0.5942622188475634, -59.55357811140123, -90.0], 
                   'ball': [-89.85408725528224, -89.99999999999997, 0.0], 
                   'toe': [-89.85408725528225, -89.99999999999997, 0.0]}

# YZX
system_pos_yzx = {'hip': [16.036325454711914, 147.7965545654297, 0.051486290991306305], 
                   'knee': [20.133201367026416, 82.0524305014815, -0.45058841430001517], 
                   'ankle': [24.197132110595714, 12.625909805297862, -3.4932091236114484], 
                   'ball': [24.084232330322276, 8.881784197001252e-15, 17.988098144531243], 
                   'toe': [24.084232330322276, -6.835402147862271e-15, 29.188819885253892]}
system_rot_yzx = {'hip': [-0.43670082003745525, 0.0, -176.43419733389047], 
                   'knee': [-2.5051019515754724, 0.0035324430433216728, -176.434], 
                   'ankle': [59.55357811140115, 0.0, 180.0], 
                   'ball': [89.99999999999993, 1.8636062586700292e-16, -180.0], 
                   'toe': [89.99999999999996, -1.2424041724466862e-17, -180.0]}

has_orientation = "yes"

ik_joints = {
    "start_joint": "hip",
    "end_joint": "ankle",
    "pv_joint": "knee",
    "world_orientation": True
}

twist_joint= {
    "start": "hip",
    "end": "ankle"
}

side = "_L"
stretch = True
space_swapping = ["hip","root","COG","Custom"]
guide_scale = 1
available_rig_types = ["FK", "IK", "IKFK"] # Add ribbon in future!
reverse_foot = True
rev_locators = {  # items foot_ctrl, ankle, ball, toe must be the same
    "foot_ctrl": system[2],
    "ankle": system[2],
    "ball": system[3],
    "toe": system[4],
    "heel": "heel",
    "bank_in": "bank_in",
    "bank_out": "bank_out",
}
default_ctrl_shape = {
    "fk_ball": "circle", 
    "ik_ball": "cube"
} # Have fk as circle, ik as cube & ribbon as octogan. 