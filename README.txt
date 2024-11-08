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

when build skeleton, and the joints are mirrored the orientation is just like mirroring. 
but if i close and re-open the ui and build the skeleton, the parent joint is 
orientated to it's corresponding guide.
What are the possible reason's for this issue?
- well what's the changing factor? reloading the ui. How the data is retrieved. 
- data when it works: the guide is made & mirrored , that dictionary is just stored and joints are built off it. 
- data when it doesn't work: the guide already exists and the dictionary comes from the data guide. 
> compare the 2 dictionary's joint data before building the joints in the ui.create_joints() and 
in the joints.py file. 

=> if the _R module is in the scene then the mirror guide isn't called, and then the issue happens. 
=> I tested with another _L arm in the scene with mirror set to 'YES', reloaded the ui & run build skeleton & the newly created '_R' worked fine. 
==> Issue arrises when the '_R' already exists and create joints is called!. 
=> I've narrowed down the issue to joints.py

!!!!!!
SOLUTION: > NEED TO EDIT JOINTS.py that checks for '_R' and 
changes the orientation of the parent joint to match the other's orientation!
!!!!!!
-----------------------------
To do:
> 

> the quadleg needs to work with spaceSwap

> after the space-swap and other issues r fixed, move onto the neck system, 
So i can test creating a rig for testing rotomation > Email Malcom  
> acapture movement. question onto Stephen cpncerning creating a head & arm rig for cg replacments.  

- Joints
- System
- constraint to rig joints
- update dictionary

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

