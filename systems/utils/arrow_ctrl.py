
import importlib
import maya.cmds as cmds
import sys
import os

from systems.utils import (OPM)
importlib.reload

def cr_arrow_control(module_name, master_guide, side):
    print(f"module name: {module_name}, master guide name: {master_guide}, side: {side}")
    
    module = module_name # 'biped_leg' / for name
    # master_guide = 'master_0_biped_leg_R' / for position / for amount
    # side = '_R' / for name/ for amount
    # orientation = 'xyz'/ for amount
    
    amount = 50

    # if 'spine' in module_name:
    '''
    COG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                            "..", "imports","cog_ctrl_import.abc")
    print(f"arw_control import path: {COG_FILE}")
    imported = cmds.file(COG_FILE, i=1, namespace="imp_cog", rnn=1)
    cmds.scale(1, 1, 1, imported)
    mdl_switch_ctrl = cmds.rename(imported[0], f"ctrl_cog")
    # position the cog ctrl to the guide_0_COG!
    cog_pos = "guide_0_COG" # cmds.listRelatives(master_guide, c=1, type="transform")[0]
    cmds.matchTransform(mdl_switch_ctrl, cog_pos,  pos=1, rot=0, scl=0)
    pos = 0,0,0
    '''
    # else:
    # import & rename the arrow control
    ARW_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                            "..", "imports","arrow_ctrl_import.abc")
    print(f"arw_control import path: {ARW_FILE}")
    imported = cmds.file(ARW_FILE, i=1, namespace="imp_arrow", rnn=1)
    cmds.scale(1, 1, 1, imported)
    mdl_switch_ctrl = cmds.rename(imported[0], f"ctrl_arw_{master_guide[7:]}")
    # middle_guide = cmds.listRelatives(master_guide, )
    listrelatives_item = cmds.listRelatives(master_guide, ad=1, type="transform")
    match_pos = [obj for obj in listrelatives_item if 'cluster_crv' not in obj and 'handle' not in obj and 'data' not in obj][1]
    cmds.matchTransform(mdl_switch_ctrl, match_pos, pos=1, rot=0, scl=0)

    if side == '_L':
        pos = amount,0,0
    else:
        pos = -amount,0,0

    cmds.setAttr(f"{mdl_switch_ctrl}.overrideEnabled", 1)
    cmds.setAttr(f"{mdl_switch_ctrl}.overrideColor", 18)
    cmds.move(*pos, mdl_switch_ctrl, r=1, os=1, wd=1)
    OPM.OpmCleanTool(mdl_switch_ctrl)

    return mdl_switch_ctrl

