import maya.cmds as cmds
import importlib
import os
from systems.utils import (connect_modules, utils, control_shape) #  reverse_foot, 
importlib.reload(connect_modules)
importlib.reload(utils)
importlib.reload(control_shape)
# importlib.reload(reverse_foot)


scale = 1


class Guides():
    def __init__(self, accessed_module, offset, side, to_connect_to, use_existing_attr, orientation):
        self.module = importlib.import_module(f"systems.modules.{accessed_module}")
        # [if] statement for "self.create_guide" variable {if == "hand"}
        # else:
        self.create_guide = self.guides
    def collect_guides(self):
        pass

    def creation(self, accessed_module, offset, side, guide_connector_list, use_existing_attr, orientation):
        # 1) Setup & initialisation
        # > Defining file paths & configurations > importing guide shape
        GUIDE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                "imports","guide_shape.abc")
        ROOT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                 "imports", "ctrl_root_import.abc")
        guide_list = []
        root_exists = False

        # 2) Determine Side
        if self.module_side == "None":
            side = ""
        else:
            side = self.module_side

        
        # 3) Determine Orientation > I need to do this differently for the hands too!
        if orientation == "xyz":
            pos_dict = self.module.system_pos_xyz
            rot_dict = self.module.system_rot_xyz
        elif orientation == "yzx":
            pos_dict = self.module.system_pos_yzx
            rot_dict = self.module.system_rot_yzx
        else:
            raise ValueError("Invalid orientation specified")
        
        # 4) Create master guide for module
        if "root" in self.module.system:
            master_guide = "root"
        # set the master guides for the fingers on "biped_finger" module 
        elif "biped_phal_proximal" in self.module.system:
            master_guide = "biped_phal_proximal"
        # set the master guides for the fingers on "biped_hand" module
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
            master_guide = control_shape.controlTypes().create_cube(
                f"master_{accessed_module}{side}_#", scale=[5, 5, 5])
        
        # Position the new master guide with the given offset
        pos = pos_dict[self.module.system[0]]
        rot = rot_dict[self.module.system[0]]
        cmds.xform(master_guide, ws=1, t=[pos[0]+offset[0], pos[1]+offset[1], 
                                          pos[2]+offset[2]])
        cmds.xform(master_guide, ws=1, ro=[rot[0], rot[1], rot[2]])
        
        # 5) Guide creation loop
        for x in self.module.system:
            try: 
                if "root" in x: 
                    imported = ROOT_FILE # was: cmds.circle(r=50, nr=[0, 1, 0])
                    root_exists = True
                    guide = cmds.rename(imported, f"{x}{side}")
                else:
                    imported = cmds.file(GUIDE_FILE, i=1, namespace="test", rnn=1)
                    cmds.scale(self.module.guide_scale, self.module.guide_scale, 
                               self.module.guide_scale, imported)
                    guide = cmds.rename(imported[0], f"{x}{side}")
                if "root" in x and root_exists is True:
                    master_guide = guide
                elif "biped_phal_proximal" in self.module.system:
                    master_guide = guide
                else:
                    guide_list.append(guide)
                for shape in imported[1:]:
                    shape = shape.split("|")[-1]
                    cmds.rename(shape, f"{guide}_shape_#")

                # Set the colour of the guide shape!
                utils.colour_custom_guide_shape(GUIDE_FILE)
            except RuntimeError:
                print("Couldn't load guide shape file, using basic shapes instead")
                cmds.spaceLocator(n=x)

            # Use the selected dict'sto set location and rotation
            pos = pos_dict[x]
            rot = rot_dict[x]
            cmds.xform(guide, ws=1, t=[pos[0]+offset[0], pos[1]+offset[1], pos[2]+offset[2]])
            cmds.xform(guide, ws=1, ro=[rot[0], rot[1], rot[2]])
            
            # Add a custom attr to each guide to specify its original type
            cmds.addAttr(guide, ln="original_guide", at="enum", en=x, k=0)

        # 6) Parenting & connecting guides
        
        # Reverse the guides & parent together w/ visual connectors created 
        # between them using the utility function!
        guide_list.reverse()
        ui_guide_list = guide_list
        guide_list.append(master_guide)
        for i in range(len(guide_list)):
            try:
                cmds.parent(guide_list[i], guide_list[i+1])
                guide_connector = utils.guide_curve_connector(guide_list[i], guide_list[i+1])
                guide_connector_list.append(guide_connector)
            except:
                pass # This is the end of the list!
        
        # Guide connectors are grouped under this grp: 
        if "grp_guideConnector_clusters" in cmds.ls("grp_guideConnector_clusters"):
            cmds.parent(guide_connector_list, "grp_guideConnector_clusters")
        else: 
            cmds.group(guide_connector_list, n="guide_connector_list", w=1)
        
        # 7) Add attributes
        
        self.available_rig_modules_type = ":".join(self.module.available_rig_types) 
        # self.module.available_rig_types is the variable found within each module, arm, leg & so on. 
        # In this case it's getting the '["IK", "FK", "IKFK"]' varible for the custom attribiutes!
        
        custom_attribute = self.add_custom_attr()
        # Add ones to the master guide & then proxy to the other guide shapes
        # such as:
        '''If these attributes are simply locked enum attributes I'll use my utils functions'''
        cmds.addAttr(master_guide, ln="is_master", at="enum", en="True", k=0)
        cmds.addAttr(master_guide, ln="base_module", at="enum", en=accessed_module, k=0) # mdl_attr
        cmds.addAttr(master_guide, ln="module_side", at="enum", en=side, k=0)
        cmds.addAttr(master_guide, ln="master_guide", at="enum", en=master_guide, k=0)
        cmds.addAttr(master_guide, ln="orientation", at="enum", en=orientation, k=0)
        
        # Adding the proxy 
        for item in ["is_master", "base_module", "module_side", "master_guide", "orientation"]:
            cmds.addAttr(guide_list[:-1],ln=f"{item}", proxy=f"{guide_list[-1]}.{item}")
            for guide in guide_list[:-1]:
                cmds.setAttr(f"{guide}.{item}",k=0)
        
        # 8) control shape attributes
        # for each guide it adds attributes for control shapes, associated with ik & fk systems. 
        for guide in ui_guide_list:
            if "root" in guide or "COG" in guide or "master" in guide: pass
            else:
                for ikfk in ["ik", "fk"]:
                    control_shape_instance = control_shape.controlShapeList()
                    control_shape_instance.return_filtered_list(type=ikfk, object=guide)
                    control_shape_list = control_shape_instance.return_list()
                    control_shape_en = ":".join(control_shape_list)
                    cmds.addAttr(guide, ln=f"{guide}_{ikfk}_control_shape", 
                                 at="enum", en=control_shape_en, k=1)
        
        # 9) Return UI data
        # Return a dictionary containing master_guide, guide_connector_list & 
        # ui_guide_list for further use in the ui
        ui_dict = {"master_guide":master_guide, 
                   "guide_connector_ls": guide_connector_list, 
                   "ui_guide_list": ui_guide_list
                   }
        return ui_dict
    
    def add_custom_attr(self, system, master_guide, use_existing_attr, accessed_module):
        guide_custom_attributes = {"module_dvdr":["enum", "------------", "MODULE", True],
                            "module_type":["enum", "Base_Module", accessed_module, True],
                            "skeleton_dvdr":["enum", "------------", "SKEL", True], 
                            "mirror_jnts":["enum", "Mirror_Jnts" "No:Yes", False],
                            "twist_jnts":["enum", "Twist_jnts" "No:Yes", False],
                            "twist_amount":["float", "Twist_Amount" "UPDATE", False], 
                            "rig_dvdr":["enum", "------------" "RIG", True], 
                            "rig_type":["enum", "Rig_Type", self.available_rig_modules_type, False],
                            "squash_stretch":["enum", "Squash_&_Stretch" "No:Yes", False]
                            }
        
        # iterates through ^guide_custom_attributes^ & adds attributes to master_guide based on their type.
        def add_new_attr(attr_name, attr_details):
            if attr_details[0] == "enum": # for the enum attributes
                cmds.addAttr(master_guide, k=1, ln=f"{system[-1]}_{attr_name}", nn=attr_details[1], at="enum", en=attr_details[2])
            elif attr_details[0] == "float": # for the float attributes
                if attr_details[1] == "twist_amount":
                    cmds.addAttr(master_guide, k=1, ln=f"{system[-1]}_{attr_name}", 
                                 nn=attr_details[1], at="float", min=0, max=3 )
                else:
                    cmds.addAttr(master_guide, k=1, ln=f"{system[-1]}_{attr_name}", 
                                 nn=attr_details[1], at="float", min=0)
            if attr_details[3] is True: # if attribute marked as locked, it locks the attribute
                cmds.setAttr(f"{master_guide}.{system[-1]}_{attr_name}", l=1)
        
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
