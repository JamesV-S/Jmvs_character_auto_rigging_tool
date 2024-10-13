import importlib
import maya.cmds as cmds

class controlShapeList():
    def __init__(self):
        # predefined list of controls
        self.ctrl_shape_list = ["circle", "cube", "octagon", "locator"]

    def return_filtered_list(self, type, object):
        
        print("CALLING 'return_filtered_list(type, object)'")
        
        # arg 'type' is string reping the type of control shape 
        # arg 'object' is string reping name of obj whose attrribs r to be queried
        
        # get the base_module attr from obj & import corresponding module. 
        module = cmds.getAttr(f"{object}.base_module", asString=1)
        module_path = importlib.import_module(module)
        importlib.reload(module_path)

        # get the orginal guide attr from obj
        base_guide = cmds.getAttr(f"{object}.original_guide", asString=1)

        # if key exists & value is in the initial control shape list, move this ctrl 
        # to the start of the list to give priority
        try:
            try:
                if module_path.default_ctrl_shape[f"{type}_{base_guide}"]:
                    default_ctrl_shape = module_path.default_ctrl_shape[f"{type}_{base_guide}"]
                    if default_ctrl_shape in self.ctrl_shape_list:
                        self.ctrl_shape_list.remove(default_ctrl_shape)
                        self.ctrl_shape_list.insert(0, default_ctrl_shape)
            except AttributeError: 
                print("catches if module doesnt have default_ctrl_shape dict")
                pass
        except KeyError:
            print("catches the guide isn't in the default_ctrl_shape dict ")
            pass

    def return_list(self):
        return self.ctrl_shape_list
    

class controlTypes():
    def __init__(self, name, ctrl_type):
        self.ctrl_name = name
        #module = f"self.create_{ctrl_type}()"
        #eval(module)
        
        self.ctrl_curve = None
        method = getattr(self, f"create_{ctrl_type}", None)
        if callable(method):
            self.ctrl_curve = method()
        
        '''
        if ctrl_type == "cube":
            print("------IMAGINE MAKING CUBE FROM TYPE!------")
            # self.create_cube()
            '''
       
        
    def create_circle(self):
        self.ctrl_curve = cmds.circle(n=self.ctrl_name, r=1, nr=(1, 0, 0))[0]
        return self.ctrl_name
        
    def create_cube(self):
        self.ctrl_curve = cmds.curve(n=self.ctrl_name, d=1, 
                                   p=[(0,0,0), (1,0,0), (1,0,1),
                                      (0,0,1), (0,0,0), (0,1,0),
                                      (1,1,0), (1,0,0), (1,1,0),
                                      (1,1,1), (1,0,1), (1,1,1),
                                      (0,1,1), (0,0,1), (0,1,1), (0,1,0)])
        cmds.CenterPivot()
        cmds.xform(self.ctrl_curve, t=(-.5, -.5, -.5))
        cmds.makeIdentity(a=1 ,t=1, r=1, s=0, n=0, pn=1)
        return self.ctrl_name
    
    def create_octagon(self):
        self.ctrl_curve = cmds.curve(n=self.ctrl_name, d=1, 
                                p=[(0.287207, 0, 0.676617),
                                    (0.677828, 0, 0.275354),
                                    (0.677828, 0, -0.287207),
                                    (0.275354, 0, -0.677828),
                                    (-0.287207, 0, -0.676617),
                                    (-0.680282, 0, -0.275354),
                                    (-0.675373, 0, 0.287207),
                                    (-0.275354, 0, 0.677828),
                                    (0.287207, 0, 0.676617)
                                    ], k=[0, 1, 2, 3, 4, 5, 6, 7, 8])
    
        return self.ctrl_name

    def create_locator(self):
        self.ctrl_curve = cmds.spaceLocator(n=self.ctrl_name)
        return self.ctrl_name
    
    def return_ctrl(self):
        return self.ctrl_name
    
    '''
    def __str__(self):
        print("ctrl_shape typ shi: ", self.ctrl_curve)
        return self.ctrl_curve
    '''


class Controls():
    def __init__(self, scale, guide, ctrl_name, rig_type):
       
        self.ctrl_name =  ctrl_name

        # scale is converted into a list 3 so can be used in commands properly
        self.scale = scale
        if type(self.scale) is int or type(self.scale) is float:
            self.scale = [self.scale, self.scale, self.scale]
        
        
        # put this line into a variable so every ctrl in the list has it's control type gotten!
        control_type = cmds.getAttr(f"guide{guide}.{guide}_{rig_type}_control", asString=1)
        
        # Get a list of possible control shapes
        ctrl_shape_instance = controlShapeList()
        ctrl_list = ctrl_shape_instance.return_list()
        if control_type in ctrl_list:
            # If the retrieved control shape type is in the list, 
            # it creates the control using ControlTypes and assigns it to self.ctrl.
            control_module = controlTypes(self.ctrl_name, control_type) 
            self.ctrl = control_module.return_ctrl()
            # Call methods to set the control's size and name.
            self.set_control_size()
            self.set_name()
        
    # Methods:
    def set_control_size(self):
        cmds.xform(self.ctrl, s=[10*self.scale[0], 10*self.scale[1], 10*self.scale[2]])
        cmds.select(self.ctrl)
        cmds.makeIdentity(a=1, t=1, r=1, s=1)
        cmds.delete(self.ctrl, ch=1)

    def set_name(self):
        cmds.rename(self.ctrl, self.ctrl_name)

    def return_ctrl(self):
        return self.ctrl_name
        

        