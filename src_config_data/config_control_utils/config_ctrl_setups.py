
import configparser
import maya.cmds as cmds
import os

def import_ini_file():
    config = configparser.ConfigParser()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ini_list = ['ctrl_settings.ini']
    # create the .ini fole path then read
    for ini in ini_list:
        config_file = os.path.join(current_dir, '..', 'config', ini)
        config.read(config_file)
    print(config.sections())
    return config.sections()

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def create_control_shape(ctrl_name, ctrl_type):
    shape_creators = {
        'circle': create_circle,
        'cube': create_cube,
        'octagon': create_octagon,
        'locator': create_locator
    }
    create_fn = shape_creators.get(ctrl_type)
    
    if create_fn:
        return create_fn(ctrl_name)
    else:
        raise ValueError(f"Unknown control type: {ctrl_type}")

def create_circle(ctrl_name):
    ctrl_curve = cmds.circle(n=ctrl_name, r=1, nr=(1, 0, 0))[0]
    return ctrl_curve

def create_cube(ctrl_name):
    ctrl_curve = cmds.curve(
        n=ctrl_name, d=1,
        p=[(0,0,0), (1,0,0), (1,0,1), (0,0,1), (0,0,0), (0,1,0),
           (1,1,0), (1,0,0), (1,1,0), (1,1,1), (1,0,1), (1,1,1),
           (0,1,1), (0,0,1), (0,1,1), (0,1,0)]
    )
    cmds.CenterPivot()
    cmds.xform(ctrl_curve, t=(-.5, -.5, -.5))
    cmds.makeIdentity(a=1, t=1, r=1, s=0, n=0, pn=1)
    return ctrl_curve

def create_octagon(ctrl_name):
    ctrl_curve = cmds.curve(
        n=ctrl_name, d=1,
        p=[(0.287207, 0, 0.676617), (0.677828, 0, 0.275354),
           (0.677828, 0, -0.287207), (0.275354, 0, -0.677828),
           (-0.287207, 0, -0.676617), (-0.680282, 0, -0.275354),
           (-0.675373, 0, 0.287207), (-0.275354, 0, 0.677828),
           (0.287207, 0, 0.676617)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8]
    )
    return ctrl_curve

def create_locator(ctrl_name):
    ctrl_curve = cmds.spaceLocator(n=ctrl_name)
    return ctrl_curve

def set_control_size(ctrl, scale):
    cmds.xform(ctrl, s=[10 * scale[0], 10 * scale[1], 10 * scale[2]])
    cmds.select(ctrl)
    cmds.makeIdentity(a=1, t=1, r=1, s=1)
    cmds.delete(ctrl, ch=1)

def create_and_configure_control(config_file, ctrl_name):
    config = read_config(config_file)
    
    scale = config.getfloat('ControlSettings', 'scale')
    scale_vector = [scale, scale, scale]

    control_type = config.get('ControlShapes', ctrl_name)

    ctrl_curve = create_control_shape(ctrl_name, control_type)
    set_control_size(ctrl_curve, scale_vector)
    
    return ctrl_curve