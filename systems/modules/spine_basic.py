system = ["spine_1", "spine_2", "spine_3", "spine_4", "spine_5"]
# XYZ
system_pos_xyz = {'spine_1': [0.0, 150.0, 0.0], 
                  'spine_2': [-1.0302985026792348e-14, 165.3182830810547, 2.138536453247061], 
                  'spine_3': [-2.3043808310802754e-14, 185.50926208496094, 2.8292100429534632], 
                  'spine_4': [-3.3364796818449844e-14, 204.27308654785156, -0.3802546262741595], 
                  'spine_5': [-5.1020985278054485e-14, 237.46397399902344, -8.25034904479989]}
system_rot_xyz = {'spine_1': [0.0, -7.947513469078512, 90.00000000000001], 
                  'spine_2': [-1.9890093469260345e-16, -1.959155005957633, 90.00000000000001], 
                  'spine_3': [0.0, 9.706246313394262, 90.00000000000001], 
                  'spine_4': [-8.171859705486283e-16, 13.339396285991443, 90.0], 
                  'spine_5': [-7.814945266275812e-14, -9.271752801444176, 89.99999999999991]}

# YZX
system_pos_yzx = {'spine_1': [0.0, 149.99999999999997, 0.0], 
                  'spine_2': [0.0, 165.31828684331416, 2.1385364623483873], 
                  'spine_3': [0.0, 185.50925602661235, 2.829210091525154], 
                  'spine_4': [0.0, 204.27308987171685, -0.3802546321712157], 
                  'spine_5': [0.0, 237.46397213105308, -8.250348923732691]}
system_rot_yzx = {'spine_1': [7.667038985618099, 0.0, 0.0], 
                  'spine_2': [1.880673240761548, 0.0, 0.0], 
                  'spine_3': [-9.496334372767544, 0.0, 0.0], 
                  'spine_4': [-13.212290179161894, 0.0, 0.0], 
                  'spine_5': [9.331941466846782, 0.0, 0.0]}

''' Because how I'm writing it in the create_guides.py I won't need this:
axis_orientation = "xyz"
if axis_orientation == "xyz":
    system_pos = system_pos_xyz
    system_rot = system_rot_xyz
    print[f"xyz orientation"]
if axis_orientation == "yzx":
    system_pos = system_pos_yzx
    system_rot = system_rot_yzx
    print[f"yzx orientation"]
'''

has_orientation = "yes"

ik_joints = {
    "start_joint": "spine_1",
    "end_joint": "spine_5",
    "pv_joint": None,
    "world_orientation": True
}
side = "None"
space_swap = []
guide_scale = 1
available_rig_types = ["FK", "IK", "IKFK"]
default_ctrl_shape = {
    "fk_wrist": "circle",
    "ik_wrist": "cube"
}