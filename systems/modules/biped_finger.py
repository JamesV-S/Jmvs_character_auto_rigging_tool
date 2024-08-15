
system = ["fing_phal_proximal_0", "biped_phal_middle_0", "biped_phal_distal_0", "biped_phal_distalEnd_0"]
system_pos_xyz = {'biped_phal_proximal_0': (80.1939468383789, 152.35321044921875, 23.64400291442871), 
              'biped_phal_middle_0': (82.63496348169618, 145.6465723411917, 26.97206641207716), 
              'biped_phal_distal_0': (84.16667564616189, 141.43822775621817, 29.06039110966503), 
              'biped_phal_distalEnd_0': (85.23322557829721, 138.50790590095545, 30.514517162953766)}
system_rot_xyz = {'biped_phal_proximal_0': (23.0, -25.00000000000005, -70.00000000000003), 
              'biped_phal_middle_0': (23.00000000000001, -25.000000000000057, -70.00000000000003), 
              'biped_phal_distal_0': (23.00000000000001, -25.000000000000057, -70.00000000000003), 
              'biped_phal_distalEnd_0': (23.00000000000001, -25.000000000000057, -70.00000000000003)}

system_pos_yzx =  {'biped_phal_proximal_0': (80.19394606756256, 152.35320359361023, 23.644002910328396), 
                   'biped_phal_middle_0': (82.61541856572182, 145.66173207304433, 26.96767490588119), 
                   'biped_phal_distal_0': (84.14606245539908, 141.4319669182922, 29.06861069398193), 
                   'biped_phal_distalEnd_0': (85.21207493612852, 138.48615929058138, 30.53180130705048)}


system_rot_yzx = {'biped_phal_proximal_0': (50.95891725101831, -56.98582204849474, 153.9365525662274), 
                  'biped_phal_middle_0': (50.95891725101831, -56.98582204849474, 153.9365525662274), 
                  'biped_phal_distal_0': (50.95891725101831, -56.98582204849474, 153.9365525662274), 
                  'biped_phal_distalEnd_0': (50.95891725101831, -56.98582204849474, 153.9365525662274)}


# You are able to change the number of fingers you want. But not the number of 
# phalanges because it's a biped finger. 

axis_orientation = "xyz"
if axis_orientation == "xyz":
    system_pos = system_pos_xyz
    system_rot = system_rot_xyz
    print[f"xyz orientation"]

if axis_orientation == "yzx":
    system_pos = system_pos_yzx
    system_rot = system_rot_yzx
    print[f"yzx orientation"]

# For the seperate modules i would like to have the option for them to spawn 
# somewhere in space with a locator that loads in from selecting someting on my ui
number_of_finger = [] # This the option to add as many pibed fingers you want
side = "_l"
available_rig_types = ["FK", "IK", "IKFK"]