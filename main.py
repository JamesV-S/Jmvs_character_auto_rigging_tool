
import importlib
import sys
import os
'''
import maya.cmds as cmds
script_path = cmds.file(query=True, sceneName=True)
__file__ = script_path
'''
# Add the scripts('main.py') directory to sys.path and MAYA_SCRIPT_PATH
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)
os.environ['MAYA_SCRIPT_PATH'] = script_dir + os.pathsep + os.environ.get('MAYA_SCRIPT_PATH', '')
# Get the current scriptpath
# Retrieve Existing MAYA_SCRIPT_PATH: 'os.environ.get('MAYA_SCRIPT_PATH', '')'
# Concatenate Paths: 'os.pathsep' is the separator for the operating system
# Update enviroment Variable: updated path assigned back to 'os.environ['MAYA_SCRIPT_PATH']'
# modifying the environment variable for the duration of the script's execution 
# (and any subprocesses it spawns)

# import the ui & run it
import ui
importlib.reload(ui)

def run_ui():
    ui.main()
    print("main is run")
run_ui()
