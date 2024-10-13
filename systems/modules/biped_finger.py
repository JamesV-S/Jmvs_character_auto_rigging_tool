
system = ["bipedPhalProximal", "bipedPhalMiddle", "bipedPhalDistal", "bipedPhalDistalEnd"]
system_pos_xyz = {'bipedPhal_proximal': (80.1939468383789, 152.35321044921875, 23.64400291442871), 
              'bipedPhalMiddle': (82.63496348169618, 145.6465723411917, 26.97206641207716), 
              'bipedPhalDistal': (84.16667564616189, 141.43822775621817, 29.06039110966503), 
              'bipedPhalDistalEnd': (85.23322557829721, 138.50790590095545, 30.514517162953766)}
system_rot_xyz = {'bipedPhal_proximal': (23.0, -25.00000000000005, -70.00000000000003), 
              'bipedPhalMiddle': (23.00000000000001, -25.000000000000057, -70.00000000000003), 
              'bipedPhalDistal': (23.00000000000001, -25.000000000000057, -70.00000000000003), 
              'bipedPhalDistalEnd': (23.00000000000001, -25.000000000000057, -70.00000000000003)}

system_pos_yzx =  {'bipedPhal_proximal': (80.19394606756256, 152.35320359361023, 23.644002910328396), 
                   'bipedPhalMiddle': (82.61541856572182, 145.66173207304433, 26.96767490588119), 
                   'bipedPhalDistal': (84.14606245539908, 141.4319669182922, 29.06861069398193), 
                   'bipedPhalDistalEnd': (85.21207493612852, 138.48615929058138, 30.53180130705048)}


system_rot_yzx = {'bipedPhal_proximal': (50.95891725101831, -56.98582204849474, 153.9365525662274), 
                  'bipedPhalMiddle': (50.95891725101831, -56.98582204849474, 153.9365525662274), 
                  'bipedPhalDistal': (50.95891725101831, -56.98582204849474, 153.9365525662274), 
                  'bipedPhalDistalEnd': (50.95891725101831, -56.98582204849474, 153.9365525662274)}


# You are able to change the number of fingers you want. But not the number of 
# phalanges because it's a biped finger. 

has_orientation = "yes"

# For the seperate modules i would like to have the option for them to spawn 

ik_joints = {
    "start_joint": "bipedPhalProximal",
    "end_joint": "bipedPhalDistalEnd", 
    "pv_joint": "bipedPhalMiddle", 
    "world_orientation": False
}

# somewhere in space with a locator that loads in from selecting checkbox on my ui
number_of_fingers = [] # This the option to add as many pibed fingers you want
side = "_L"
available_rig_types = ["FK", "IK", "IKFK"]