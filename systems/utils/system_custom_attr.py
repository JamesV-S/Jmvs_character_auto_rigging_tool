import maya.cmds as cmds

class buildCustomAttr:
    def __init__(self, system, master_guide, use_existing_attr, accessed_module, rig_type):
        # gather the args and apply to self.var to share globally. 
        self.system = system
        self.master_guide = master_guide
        self.use_existing_attr = use_existing_attr
        self.accessed_module = accessed_module
        self.rig_type = rig_type

        # cstm attrbts for each module
        self.guide_cstm_attrs = {
            "module_dvdr": ["enum", "------------", "MODULE", True],
            "module_type": ["enum", "Base Module", accessed_module, True],
            "skeleton_dvdr": ["enum", "------------", "SKEL", True], 
            "mirror_jnts": ["enum", "Mirror Jnts", "No:Yes", False],
            "rig_dvdr": ["enum", "------------", "RIG", True], 
            "rig_type": ["enum", "Rig Type", rig_type, False],
            "squash_stretch": ["enum", "Squash & Stretch", "No:Yes", False]
        }
        self.run_custom_attr()

    def run_custom_attr(self):
        if self.use_existing_attr:
            self.existing_attr()
        else:
            self.add_all_attrs()
            # proxy attributess
            self.cr_proxy_attrs(self.system[:-1], [], self.system[-1], False)

    def add_all_attrs(self):
        for attr_name, attr_details in self.guide_cstm_attrs.items():
            self.create_attr(attr_name, attr_details)

    def create_attr(self, attr_name, attr_details):
        attr_type, nice_name, enum_options, is_locked = attr_details
        attr_full_name = f"{self.system[-1]}_{attr_name}"

        print(f"Attrib details made: {enum_options}")

        if attr_type == "enum":
            cmds.addAttr(self.master_guide, k=True, ln=attr_full_name, 
                         nn=nice_name, at="enum", en=enum_options)
        elif attr_type == "float":
            self.cr_proxy_attrs(attr_name, attr_full_name, nice_name)

        if is_locked:
            print(f"Attrib LOCK made: {is_locked}")
            cmds.setAttr(f"{self.master_guide}.{attr_full_name}", l=True, 
                         keyable=False, channelBox=True)

    def cr_proxy_attrs(self, attr_name, attr_full_name, nice_name):
        if attr_name == "twist_amount":
            cmds.addAttr(self.master_guide, k=True, ln=attr_full_name, 
                         nn=nice_name, at="float", min=0, max=3)
        else:
            cmds.addAttr(self.master_guide, k=True, ln=attr_full_name, 
                         nn=nice_name, at="float", min=0)

    def existing_attr(self):
        ignore_attr = ["rig_type"]
        self.cr_proxy_attrs(self.system, ignore_attr, 
                                self.use_existing_attr[0], False)

        for attr in ignore_attr:
            self.create_attr(attr, self.guide_cstm_attrs[attr])

        self.cr_proxy_attrs(self.system[:-1], ignore_attr, 
                                self.system[-1], True)

    def cr_proxy_attrs(self, system_list, ignore_attr, proxy_item, add_missing):
        target_list = ignore_attr if add_missing else self.guide_cstm_attrs.keys()
        
        for item in target_list:
            if item not in ignore_attr:
                cmds.addAttr(system_list, ln=f"{self.master_guide}_{item}", 
                             proxy=f"{proxy_item}.{proxy_item}_{item}")