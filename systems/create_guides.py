import maya.cmds as cmds
import importlib
import os
from systems.utils import (connect_modules, utils, control_shape) #  reverse_foot, 
importlib.reload(connect_modules)
importlib.reload(utils)
importlib.reload(control_shape)
# importlib.reload(reverse_foot)


scale = 1


class Guides_class():
    def __init__(self, accessed_module, offset, side, to_connect_to, use_existing_attr, orientation, numb_id):
        self.module = importlib.import_module(f"systems.modules.{accessed_module}")
        # Reload the module for any updates!
        importlib.reload(self.module)

        # [if] statement for "self.create_guide" variable {if == "hand"}
        # else:

        self.unique_id = numb_id

        print("If you are seeing this, its is coming from 'create_guides.Guides_class, innit def!'")
        self.create_guide = self.The_guides(accessed_module, offset, side, use_existing_attr, orientation)
    
    def collect_guides(self):
        print("This print is from 'collect_guides() in class'")
        return self.create_guide

    def The_guides(self, accessed_module, offset, side, use_existing_attr, orientation):
        print("This print is from 'The_guides() in class'")
        guide_connector_list = []
        self.system_to_connect = []
        selection = cmds.ls(sl=1)
          
        if not "root_basic" in accessed_module:
            if selection:
                if "master" in selection[0]:
                    cmds.warning("unable to attatch a new module to a master control, please SELECT a guide!")
                elif "master" not in selection[0]:
                    guide = self.creation(accessed_module, offset, side, guide_connector_list, use_existing_attr, orientation)
                    master_guide = guide["master_guide"]
                    guide_connector = connect_modules.attach(master_guide, selection)
                    guide_connector_list.append(guide_connector[1])
                    
                    # Calling ".prep_attach_jnts" is designed to prepare and organize 
                    # joint relationships in the context of creating blueprint guides.
                    self.system_to_connect = connect_modules.prep_attach_jnts(master_guide, selection, need_child=True)
                    guide.update({"system_to_connect": self.system_to_connect})
                    return guide
           
        else:
            print(">> Recognised this module is root_basic!")
            guide = self.creation(accessed_module, offset, side, guide_connector_list, use_existing_attr, orientation)
            guide.update({"system_to_connect": []})
            return guide
        
    def creation(self, accessed_module, offset, side, guide_connector_list, use_existing_attr, orientation):
        
        print("IN CREATION FUNC, THE ORIENTATION ARG IS: ", orientation)
        
        # 1) Setup & initialisation
        # > Defining file paths & configurations > importing guide shape
        GUIDE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                "imports","guide_shape.abc")
        ROOT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                 "imports", "ctrl_root_octagon_import.abc")
       # print("down here")
        #imported = cmds.file(ROOT_FILE, i=1, rnn=1)
        
        guide_list = []
        root_exists = False
        # guide_pref = f"guide_{number_id}"
        
        # 2) Determine Side
        if self.module.side == "None":
            side = ""
        else:
            side = self.module.side

        # Orientation:
        if self.module.has_orientation == "None": # root_basic
            pos_dict = self.module.system_pos
            rot_dict = self.module.system_rot
            print("ORIENTATION IS NONE ###")
        else:
            if orientation == "XYZ":
                print("ORIENTATION IS 'xyz' ###")
                pos_dict = self.module.system_pos_xyz
                rot_dict = self.module.system_rot_xyz
            elif orientation == "YZX":
                print("ORIENTATION IS 'yzx' ###")
                pos_dict = self.module.system_pos_yzx
                rot_dict = self.module.system_rot_yzx

        tmp_list = []
        module_list = cmds.ls("data*")
        for obj in module_list:
            if "Shape" in obj:
                pass
            elif accessed_module in obj:
                tmp_list.append(obj)
            elif accessed_module == "root_basic" and "root" in obj:
                tmp_list.append(obj)
        

        # 4) Create master guide for module by looking in each module's variable's
        if "root" in self.module.system:
            master_guide = "root"
        # set the master guides for the fingers on "biped_finger" module 
        elif "biped_phal_proximal" in self.module.system:
            master_guide = "biped_phal_proximal"
        elif "thumb_phal_proximal" in self.module.system:
            master_guide = "thumb_phal_proximal"
        elif "index_phal_proximal" in self.module.system:
            master_guide = "index_phal_proximal"
        elif "mid_phal_proximal" in self.module.system:
            master_guide = "mid_phal_proximal"
        elif "ring_phal_proximal" in self.module.system:
            master_guide = "ring_phal_proximal"
        elif "pinky_phal_proximal" in self.module.system:
            master_guide = "pinky_phal_proximal"
        else:
            master_guide = control_shape.controlTypes(f"master_{self.unique_id}_{accessed_module}{side}", "octagon")
            master_guide = str(master_guide) # master_guide is not a string, but rather an instance of an object called controlTypes,
            print("hmmmm: ", master_guide)
            cmds.setAttr(f"{master_guide}.overrideEnabled", 1)
            cmds.setAttr(f"{master_guide}.overrideColor", 9)
            cmds.scale(8, 8, 8, master_guide)
            
            # Position the new master guide with the given offset
            pos = pos_dict[self.module.system[0]]
            rot = rot_dict[self.module.system[0]]
            cmds.xform(master_guide, ws=1, t=[pos[0]+offset[0], pos[1]+offset[1], 
                                            pos[2]+offset[2]])
            cmds.xform(master_guide, ws=1, ro=[rot[0], rot[1], rot[2]])
        
        # 5) Guide creation loop
        for x in self.module.system:
          #  try: 
            if "root" in x:
                imported = cmds.file(ROOT_FILE, i=1, rnn=1)
                cmds.scale(self.module.guide_scale, self.module.guide_scale, 
                            self.module.guide_scale, imported)
                print(">>>>>>>>root print in creation()")
                root_exists = True
                
                guide = cmds.rename(imported[0], f"guide_{self.unique_id}_{x}")
                print(f"root guide: {guide}")
                utils.colour_root_control(guide)
            else:
                imported = cmds.file(GUIDE_FILE, i=1, namespace="guide_shape_import", rnn=1)
                cmds.scale(self.module.guide_scale+1, self.module.guide_scale+1, 
                            self.module.guide_scale+1, imported)
                guide = cmds.rename(imported[0], f"guide_{self.unique_id}_{x}{side}")
                utils.colour_guide_custom_shape(guide)
            
            if "root" in x and root_exists is True:
                master_guide = guide
            elif "biped_phal_proximal" in self.module.system:
                master_guide = guide
            else:
                print("print else <<<<<")
                guide_list.append(guide)
            
           
            # Use the selected dict's to set location and rotation
            pos = pos_dict[x]
            rot = rot_dict[x]
            cmds.xform(guide, ws=1, t=[pos[0]+offset[0], pos[1]+offset[1], pos[2]+offset[2]])
            cmds.xform(guide, ws=1, ro=[rot[0], rot[1], rot[2]])
            
            # Add a custom attr to each guide to specify its original type
            cmds.addAttr(guide, ln="original_guide", at="enum", en=x, k=0)

        # 6) Parenting & connecting guides
        guide_list.reverse()
        ui_guide_list = guide_list
        guide_list.append(master_guide)
        #print("1: ", guide_list)
        #print("2: ", len(guide_list))
        print(f"CONNECTING GUIDES create_guides: {guide_list}")
        for i in range(len(guide_list)):
            try:
                cmds.parent(guide_list[i], guide_list[i+1])
                guide_connector = utils.guide_curve_connector(guide_list[i], guide_list[i+1])
                guide_connector_list.append(guide_connector)
            except:
                pass # ignore last element of the list erroring.
        
        # Guide connectors are grouped under this grp: 
        if "grp_guideConnector_clusters" in cmds.ls("grp_guideConnector_clusters"):
            cmds.parent(guide_connector_list, "grp_guideConnector_clusters")
        else: 
            cmds.group(guide_connector_list, n="grp_guideConnector_clusters", w=1)
        cmds.select(cl=1)
        
        #----------------------------------------------------------------------
        # Create  data guide
        if "root" in self.module.system: # or "proximal" in self.module.system:
            data_guide_name = f"data_{master_guide}"
        else:
            print("ERRRRRRRRRRRRRRRRRRRRRRRROOOOOOOR: ", master_guide)
            data_guide_name = master_guide.replace("master_", f"data_")
        cmds.spaceLocator(n=data_guide_name)
        cmds.matchTransform(data_guide_name, master_guide)
        cmds.parent(data_guide_name, master_guide)
        #----------------------------------------------------------------------

        # 7) Add attributes
        self.available_rig_modules_type = ":".join(self.module.available_rig_types) 
        # self.module.available_rig_types is the variable found within each module, arm, leg & so on. 
        # In this case it's getting the '["IK", "FK", "IKFK"]' varible for the custom attribiutes!
        
        custom_attribute = self.add_custom_attr(guide_list, master_guide, use_existing_attr, accessed_module)
        cmds.addAttr(master_guide, ln="is_master", at="enum", en="True", k=0)
        cmds.addAttr(master_guide, ln="base_module", at="enum", en=accessed_module, k=0) # mdl_attr
        cmds.addAttr(master_guide, ln="module_side", at="enum", en=side, k=0)
        cmds.addAttr(master_guide, ln="master_guide", at="enum", en=master_guide, k=0)
        cmds.addAttr(master_guide, ln="module_orientation", at="enum", en=orientation, k=0)
        
        # Adding the proxy 
        for item in ["is_master", "base_module", "module_side", "master_guide", "module_orientation"]:
            cmds.addAttr(guide_list[:-1],ln=f"{item}", proxy=f"{guide_list[-1]}.{item}")
            for guide in guide_list[:-1]:
                cmds.setAttr(f"{guide}.{item}",k=0)
        
        # 8) control shape attributes
        # for each guide it adds attributes for control shapes, associated with ik & fk systems. 
        for guide in ui_guide_list:
            # Ignore the these:
            if "root" in guide or "COG" in guide or "master" in guide: pass
            else:
                for ikfk in ["FK", "IK"]:
                    print("for ikfk in []: ", ikfk)
                    control_shape_instance = control_shape.controlShapeList()
                    control_shape_instance.return_filtered_list(type=ikfk, object=guide)
                    
                    control_shape_list = control_shape_instance.return_list()
                    print("ctrl_shape_list : ", control_shape_list)                    
                    control_shape_en = ":".join(control_shape_list)
                    print("Create_guides <(Line 275)> CONTROL SHAPE INDEX: ", f"{guide[6:]}_{ikfk}_control")
                    cmds.addAttr(guide, ln=f"{guide[5:]}_{ikfk.lower()}_control", 
                                 at="enum", en=control_shape_en, k=1)
        
        # 9) Return UI data
        # Return a dictionary containing master_guide, guide_connector_list & 
        # ui_guide_list for further use in the ui
        ui_dict = {
            "master_guide": master_guide, 
            "guide_connector_list": guide_connector_list,
            "ui_guide_list": ui_guide_list, 
            "data_guide": data_guide_name,
            "guide_number": self.unique_id
        }
        return ui_dict
        
    def add_custom_attr(self, system, master_guide, use_existing_attr, accessed_module):
        guide_custom_attributes = {"module_dvdr":["enum", "------------", "MODULE", True],
                            "module_type":["enum", "Base Module", accessed_module, True],
                            "skeleton_dvdr":["enum", "------------", "SKEL", True], 
                            "mirror_jnts":["enum", "Mirror Jnts", "No:Yes", False],
                            "twist_jnts":["enum", "Twist jnts", "No:Yes", False],
                            "twist_amount":["float", "Twist Amount", "UPDATE", False], 
                            "rig_dvdr":["enum", "------------", "RIG", True], 
                            "rig_type":["enum", "Rig Type", self.available_rig_modules_type, False],
                            "squash_stretch":["enum", "Squash & Stretch", "No:Yes", False]
                            }
        
        # iterates through ^guide_custom_attributes^ & adds attributes to master_guide based on their type.
        def add_new_attr(attr_name, attr_details):
            
            print(f"Attrib details made: {attr_details[2]}")

            if attr_details[0] == "enum": # for the enum attributes
                cmds.addAttr(master_guide, k=1, ln=f"{system[-1]}_{attr_name}", nn=attr_details[1], at="enum", en=attr_details[2])
            elif attr_details[0] == "float": # for the float attributes
                if attr_details[1] == "twist_amount":
                    cmds.addAttr(master_guide, k=1, ln=f"{system[-1]}_{attr_name}", 
                                 nn=attr_details[1], at="float", min=0, max=3 )
                else:
                    cmds.addAttr(master_guide, k=1, ln=f"{system[-1]}_{attr_name}", 
                                 nn=attr_details[1], at="float", min=0)
            if attr_details[3] == True: # if attribute marked as locked, it locks the attribute
                print(f"Attrib LOCK made: {attr_details[3]}")
                cmds.setAttr(f"{master_guide}.{system[-1]}_{attr_name}", l=1, 
                             keyable=False, channelBox=True)
        
        # Manage the adition of proxy attributes based on existing attribute's.
        def add_proxy(list, skip_attr, proxy_item, add_missing):
            if add_missing: # If this is True add attributesfor items in skip_attr. 
                for item in skip_attr:
                    cmds.addAttr(list, ln=f"{master_guide}_{item}", proxy=f"{proxy_item}.{proxy_item}_{item}")
            else: # Otherwise add atttributes for al items in custom_attr dictionary (that r not in skip_attr)
                for item in guide_custom_attributes:
                    if item not in skip_attr:
                        cmds.addAttr(list, ln=f"{master_guide}_{item}", proxy=f"{proxy_item}.{proxy_item}_{item}")

        if use_existing_attr:
            # Initialise the "skip_attr" with ["rig_type"] to specify which attr of the dict to skip
            skip_attr = ["rig_type"]
            # Add proxy attrib's for the current system. (so this can work on all different modules)
            add_proxy(system, skip_attr, proxy_item=use_existing_attr[0], add_missing=False)
            for attr in skip_attr:
                # Call add_new_attr func for skipped attrib's
                add_new_attr(attr, guide_custom_attributes[attr])

            # Call the add_proxy func again for the parent system (excluding the last item) 
            add_proxy(system[:-1], skip_attr, proxy_item=system[-1], add_missing=True)

        else:
            for attr_name, attr_details in guide_custom_attributes.items():
                add_new_attr(attr_name, attr_details)
            add_proxy(system[:-1], skip_attr=[], proxy_item=system[-1], add_missing=False)

'''
numbers_unfiltered = []
for data_guide in tmp_list:
    if cmds.attributeQuery("guide_number", node=data_guide, exists=True):
        numbers_unfiltered.append(cmds.getAttr(f"{data_guide}.guide_number"))
    else:
        cmds.warning(
            f"guide_number attr doesn't exist on this node '{data_guide}',guide seup might not work as sexpected to."
                        )
'''
# Increment the counter
# self.unique_id_counter += 1
#print("Create_guides, number id:::: ", type(number_unique))
#number_unique += 1 
# number_id = str(number_unique) 
'''
if numbers_unfiltered:
    numbers_unfiltered.sort()
    number_id = numbers_unfiltered[-1]+1
            '''

'''
for shape in imported[1:]:
    shape = shape.split("|")[-1]
    cmds.rename(shape, f"{guide}_shape_#")
    '''
   
#except RuntimeError:
    #   print("Couldn't load guide shape file, using basic shapes instead")
    #  cmds.spaceLocator(n=x)
'''
if "root" in x: # Ignore the orientation!
    pos = root_pos_dict[x]
    rot = root_rot_dict[x]
'''