import maya.cmds as cmds


class cstm_attr():
    def __init__(self, system, master_guide, use_existing_attr, accessed_module, rig_type):
        self.add_custom_attr(system, master_guide, use_existing_attr, accessed_module, rig_type)
    
    
    def add_custom_attr(self, system, master_guide, use_existing_attr, accessed_module, rig_type):
            guide_custom_attributes = {"module_dvdr":["enum", "------------", "MODULE", True],
                                "module_type":["enum", "Base Module", accessed_module, True],
                                "skeleton_dvdr":["enum", "------------", "SKEL", True], 
                                "mirror_jnts":["enum", "Mirror Jnts", "No:Yes", False],
                                "twist_jnts":["enum", "Twist jnts", "No:Yes", False],
                                "twist_amount":["float", "Twist Amount", "UPDATE", False], 
                                "rig_dvdr":["enum", "------------", "RIG", True], 
                                "rig_type":["enum", "Rig Type", rig_type, False],
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