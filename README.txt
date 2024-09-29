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
WIP. 
import maya.cmds as cmds

def reposition_guide_shape():
    pass
    # unparent the selected guide, so it's child doesn't move!
    # unparent the child too
    
    '''A lot easier if i just use grps!'''
    # sl child > sl selected > aim constraint, depending on orientation setting(write a way to check!)
    # > aim constraint so selected always looks at child. 
    # > put the selected into a grp orientation set to world & only move in the
    
    # Possibilty of using a live plane plane & grp that points at the child so the orientation only moves in one 

