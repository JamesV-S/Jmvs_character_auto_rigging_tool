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

-----------------------------
To do:
=> Add make joints follow rig properly. > found in old autolimb! > check autospine differencen too!
=> Head/neck module (change number of neck joints
[either as an option or be able to add guides into the added module]), & head bend system!
> the quadleg needs to work with spaceSwap

> after the space-swap and other issues r fixed, move onto the neck system, 
So i can test creating a rig for testing rotomation > Email Malcom  
> capture movement. question onto Stephen cpncerning creating a head & arm rig for cg replacments.  

> Get stretch to work on mirrored side!

> Add button to each section on the ui.
- Switch back & forth between blueprints, rig_joints, systems, polished.

> Add Advanced systems to the rig:
- Head/neck module (change number of neck joints
[either as an option or be able to add guides into the added module]), & head bend system!
- ribbon system (arm twist & what not)
- twist system (New method)
- reverse foot
- Corrective_joints/sliding_joints (be able to load guides for them to position on a rig!)

