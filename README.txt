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