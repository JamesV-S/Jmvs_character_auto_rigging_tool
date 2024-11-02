
system = ["bipedPhalProximal", "bipedPhalMiddle", "bipedPhalDistal", "bipedPhalDEnd"]
system_pos_xyz = {'bipedPhalProximal': [80.61004637463462, 151.7215423583185, 24.099996037467385], 
                  'bipedPhalMiddle': [84.45979996338392, 145.8773481500665, 28.318845156262494], 
                  'bipedPhalDistal': [87.13240797932576, 141.82014294780598, 31.24768974670393], 
                  'bipedPhalDEnd': [89.18559525612636, 138.70326159035977, 33.49772656951928]}

system_rot_xyz = {'bipedPhalProximal': [5.910977623767589, -31.083474503917564, -56.62585344811804], 
                  'bipedPhalMiddle': [5.910977623767589, -31.083474503917564, -56.62585344811804], 
                  'bipedPhalDistal': [5.910977623767589, -31.08347450391755, -56.62585344811804], 
                  'bipedPhalDEnd': [5.910977623767589, -31.08347450391755, -56.62585344811804]}



system_pos_yzx =  {'bipedPhalProximal': [80.19394606756256, 152.35320359361023, 23.644002910328396], 
                   'bipedPhalMiddle': [82.61541856572182, 145.66173207304433, 26.96767490588119], 
                   'bipedPhalDistal': [84.14606245539908, 141.4319669182922, 29.06861069398193], 
                   'bipedPhalDEnd': [85.21207493612852, 138.48615929058138, 30.53180130705048]}


system_rot_yzx = {'bipedPhalProximal': [50.95891725101831, -56.98582204849474, 153.9365525662274], 
                  'bipedPhalMiddle': [50.95891725101831, -56.98582204849474, 153.9365525662274], 
                  'bipedPhalDistal': [50.95891725101831, -56.98582204849474, 153.9365525662274], 
                  'bipedPhalDEnd': [50.95891725101831, -56.98582204849474, 153.9365525662274]}



#Trans dictionary:  {'bipedPhalProximal': [80.61004637463462, 151.7215423583185, 24.099996037467385], 'bipedPhalMiddle': [84.45979996338392, 145.8773481500665, 28.318845156262494], 'bipedPhalDistal': [87.13240797932576, 141.82014294780598, 31.24768974670393], 'bipedPhalDEnd': [89.18559525612636, 138.70326159035977, 33.49772656951928]}
#Rots dictionary:  {'bipedPhalProximal': [5.910977623767589, -31.083474503917564, -56.62585344811804], 'bipedPhalMiddle': [5.910977623767589, -31.083474503917564, -56.62585344811804], 'bipedPhalDistal': [5.910977623767589, -31.08347450391755, -56.62585344811804], 'bipedPhalDEnd': [5.910977623767589, -31.08347450391755, -56.62585344811804]}


# You are able to change the number of fingers you want. But not the number of 
# phalanges because it's a biped finger. 

has_orientation = "yes"

# For the seperate modules i would like to have the option for them to spawn 

ik_joints = {
    "start_joint": "bipedPhalProximal",
    "end_joint": "bipedPhalDistal", 
    "pv_joint": "bipedPhalMiddle", 
    "world_orientation": False, 
    "last_joint": "bipedPhalDEnd"
}

# somewhere in space with a locator that loads in from selecting checkbox on my ui
# number_of_fingers = [] # This the option to add as many pibed fingers you want
side = "_L"
stretch = True
guide_scale = 0.15
available_rig_types = ["FK", "IK", "IKFK"]
default_ctrl_shape = {
    "fk_wrist": "circle", 
    "ik_wrist": "cube"
}

space_swapping = [["world", "COG", "wrist", "custom"], ["world", "bipedPhalDEnd"], ["world", "bipedPhalProximal"], ["world", "wirst"]]




# {'bipedPhal_proximal': [23.0, -25.00000000000005, -70.00000000000003], 'bipedPhalMiddle': [23.00000000000001, -25.000000000000057, -70.00000000000003], 'bipedPhalDistal': [23.00000000000001, -25.000000000000057, -70.00000000000003], 'bipedPhalDEnd': [23.00000000000001, -25.000000000000057, -70.00000000000003]}
# {'bipedPhal_proximal': [80.1939468383789, 152.35321044921875, 23.64400291442871], 'bipedPhalMiddle': [82.63496348169618, 145.6465723411917, 26.97206641207716], 'bipedPhalDistal': [84.16667564616189, 141.43822775621817, 29.06039110966503], 'bipedPhalDEnd': [85.23322557829721, 138.50790590095545, 30.514517162953766]}