Readme: 

have repo cloned to c\\docs\\maya\\scripts

running the tool from scriptEditor, run this python code:

'''
import importlib
from Jmvs_character_auto_rigging_tool import main

importlib.reload(main)
main.run_ui()
'''


- for context this is being used within a class to create blueprint guides for a modular auto rigger within autodesk maya using python 


> attributes on ctrl guides: 
- Dividers need to be locked & unKeyable!
- Attributes, especially on the dividers are not working correctly!


-----------------------------
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

