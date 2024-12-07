import maya.cmds as cmds
import importlib
from JmvsShelf_Rigging.scripts.other import rig_scene_grp
importlib.reload(rig_scene_grp)

'''
cmds.select("hdl_ik_*_wrist_*", tgl=1)
cmds.select("grp_ik_jnts_*", tgl=1)
cmds.select("grp_fk_jnts_*", tgl=1)
cmds.select("jnt_dvr_*", tgl=1)
cmds.select("master_*", tgl=1)
cmds.select("guide_0_root", tgl=1)
cmds.select("grp_guideConnector_clusters", tgl=1)
cmds.select(cl=1)
'''
try:
    cmds.parent("grp_ik_ctrls_*", "grp_fk_ctrls_*", "ctrl_mdl_*", "ctrl_root")
except Warning:
    pass

cmds.select(cl=1)
cmds.select("ctrl_*_*_*_R")
blue_selection = cmds.ls(selection=True, type="transform")
def override_color_blu(selection):
    sel = selection# cmds.ls(selection=True)
    shape = cmds.listRelatives(sel, shapes = True )
    for node in shape:
        cmds. setAttr (node + ".overrideEnabled" ,True)
        cmds. setAttr (node + ".overrideColor" , 6)
    cmds.select(cl=1)
override_color_blu(blue_selection)

cmds.select("ctrl_*_*_*_L") # ctrl_ik_0_quadHip_L
red_selection = cmds.ls(selection=True, type="transform")
def override_color_red(selection):
    sel = selection# cmds.ls(selection=True)
    shape = cmds.listRelatives(sel, shapes = True )
    for node in shape:
        print(f"red_node: ")
        cmds. setAttr (node + ".overrideEnabled" ,True)
        cmds. setAttr (node + ".overrideColor" , 13)
    cmds.select(cl=1)
override_color_red(red_selection)

cmds.select("ctrl_*_*_spine_*")
yell_selection = cmds.ls(selection=True, type="transform")
def override_color_yellow(selection):
    sel = selection# cmds.ls(selection=True)
    shape = cmds.listRelatives(sel, shapes = True )
    for node in shape:
        cmds. setAttr (node + ".overrideEnabled" ,True)
        cmds. setAttr (node + ".overrideColor" , 17)
    cmds.select(cl=1)
override_color_yellow(yell_selection)

cmds.select("ctrl_mdl_*")
black_selection = cmds.ls(selection=True, type="transform")
def override_color_black(selection):
    sel = selection# cmds.ls(selection=True)
    shape = cmds.listRelatives(sel, shapes = True )
    for node in shape:
        cmds. setAttr (node + ".overrideEnabled" ,True)
        cmds. setAttr (node + ".overrideColor" , 1)
    cmds.select(cl=1)
override_color_black(black_selection)


if not cmds.objExists("DO_NOT_TOUCH"):
    rig_scene_grp.parent_hi_groups()
    cmds.delete("grp_ctrl_*")
    cmds.select(cl=1)
    cmds.parent("grp_ik_jnts_*", "grp_fk_jnts_*", "hdl_ik_*_wrist_*", "jnt_dvr_*_quadHip_*", "rig_systems")
    cmds.parent("ctrl_root", "controls")
    gd_grp = cmds.group(n="guides",em=1)
    cmds.parent(gd_grp, "rig_buffer")
    cmds.parent("guide_0_root", "master_*", "grp_guideConnector_clusters", gd_grp)
    cmds.parent("jnt_rig_0_root", "skeleton")

    cmds.hide("rig_systems", "guides", "misc", )