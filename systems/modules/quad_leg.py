system = ["quadHip", "quadKnee", "quadCalf", "quadAnkle"]

system_pos_xyz = {'quadHip': [22.620569466817653, 144.1399044329108, -0.3245277273685474], 
                  'quadKnee': [22.584449316155787, 83.12080210962229, 1.399156957455773], 
                  'quadCalf': [22.56734558086405, 54.22683143805715, -34.46527139681592], 
                  'quadAnkle': [22.54233003259439, 11.96714338110995, -31.719538725507462]}

system_rot_xyz = {'quadHip': [0.0, -1.6180766381813425, -90.03391613228942], 
                  'quadKnee': [0.0, 51.1435387994787, -90.03391613228945], 
                  'quadCalf': [0.0, -3.717444687739824, -90.03391613228942], 
                  'quadAnkle': [0.0, -3.717444687739824, -90.03391613228942]}

system_pos_yzx = {'quadHip': [9.016059875488281, 51.326595306396484, -24.138771057128906], 
                  'quadKnee': [0.012862205505374646, 21.736881718613237, -0.0001346988280275241], 
                  'quadCalf': [0.006090164189521019, 16.39988340706282, 9.110254524102857e-07], 
                  'quadAnkle': [0.008908271789573874, 15.079927171793372, -4.049635384006933e-05]}

system_rot_yzx = {'quadHip': [1.6184322628454946, 0.0, -180.0], 
                  'quadKnee': [-52.7619786368714, 0.0, 0.0], 
                  'quadCalf': [54.861151572516995, 0.0, 0.0], 
                  'quadAnkle': [0.0, 0.0, 0.0]}


has_orientation = "yes"

ik_joints = {
    "start_joint": "quadHip",
    "end_joint": "quadAnkle", 
    "pv_joint": "quadKnee",
    "world_orientation": True,
    "calf_joint": "quadCalf"    
}

# If axis_orientation = a specific axis, use that specified system_pos
side = "_L"
stretch = True

guide_scale = 1
available_rig_types = ["FK", "IK", "IKFK"] # Add ribbon in future!

 # Need to split it up: Clav, PV, master[wrist]
space_swapping = [["world", "COG", "quadHip", "custom"], ["world", "quadAnkle"], ["world", "spine"]]