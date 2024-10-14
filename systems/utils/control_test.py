import maya.cmds as cmds



class controlTypes():
    def __init__(self, name, ctrl_type):
        self.ctrl_name = name
        #module = f"self.create_{ctrl_type}()"
        #eval(module)
        
        #self.ctrl_curve = None
        #method = getattr(self, f"create_{ctrl_type}", None)
        #if callable(method):
        #    self.ctrl_curve = method()
        
        
        if ctrl_type == "cube":
            print("------IMAGINE MAKING CUBE FROM TYPE!------")
            self.create_cube()
        elif ctrl_type == "circle":
            print("------IMAGINE MAKING circle FROM TYPE!------")
            self.create_circle()
        elif ctrl_type == "octagon":
            print("------IMAGINE MAKING octagon FROM TYPE!------")
            self.create_octagon()
        elif ctrl_type == "locator":
            print("------IMAGINE MAKING locator FROM TYPE!------")
            self.create_locator()
        
        
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
        return str(self.ctrl_name)
    
control = controlTypes("sunny", "cube")
print(control)