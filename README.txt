Auto batch test >> 

Readme: 

have repo cloned to c\\docs\\maya\\scripts

running the tool from scriptEditor, run this python code:

'''
import importlib
from Jmvs_character_auto_rigging_tool import main

importlib.reload(main)
main.run_ui()

# Delete the scene to start again: 
cmds.select(all=True)
cmds.delete() 

'''



TO DO: > Understand why mirrored joints do not wotk with connect_modules.attatch_joints(). > The mirrored data doesn't contain the master_guide or guides to begin with, so need to mirror the guides too for necessary data. I should see the dictionary for the '_r' too!


- for context this is being used within a class to create joints on blueprint guides for a modular auto rigger within autodesk maya using python 


-----------------------------
[-] Issues to solve:
- By haveing guides already in a scene, 'data_guide' works to store the necessary data, 
and joints are created & stored in modular dictionary's properly.
HOWEVER, when building the system, everything works except the ctrl's are a 
cluster of points only visible thru their cvs!
- Basically the ctrls arnt loading properly. 
They a visible if the guides were created with the same loaded tool
> Figure out this issue. 



-----------------------------
To do:
>> Get ikfkswitch system done then move onto space swap!

> Get all systems, ikfk{DONE}, ikfkswitch, space_swap, squash & stretch added!
- Joints
- System
- constraint to rig joints
- update dictionary

> Edit how the attributes on the mirrored guides work:
- The mirrored attributes shouldn't be linked to the orginal one like a proxy attr.
- The joints created shoudln't acc be mirrored (axis facing opposite dirction), since 
guides are created for the mirrored module, create joints off of them!

> Add button to each section on the ui.
- Switch back & forth between blueprints, rig_joints, systems, polished.

> Add Advanced systems to the rig:
- Head/neck module (change number of neck joints
[either as an option or be able to add guides into the added module]), & head bend system!
- ribbon system (arm twist & what not)
- twist system (New method)
- reverse foot
- Corrective_joints/sliding_joints (be able to load guides for them to position on a rig!)

