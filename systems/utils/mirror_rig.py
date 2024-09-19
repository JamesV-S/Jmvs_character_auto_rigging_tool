import maya.cmds as cmds

class mirror_data():
    def __init__(self, systems_to_be_made):
        self.data_to_be_checked = systems_to_be_made
        self.mirror_data()
    
    def mirror_joints(self):
        # self.key is the key from the provided dict containing data on the module! 
        cmds.select(self.key["joints"][0])
        joint_list = cmds.mirrorJoint(mirrorYZ=1, mirrorBehavior=1, searchReplace=('_l', '_r'))
        return joint_list
    
    def get_mirrored_side(self):
        if self.key["side"] == "_l":
            self.side = "_r"
            self.simple_side = "_r_"
        elif self.key["side"] == "_r":
            self.side = "_l"
            self.simple_side = "_l_"
        else:
            self.side = ""

    def get_mirrored_system_to_connect(self):
        systems_to_connect = self.key["systems_to_connect"]
        mirrored_systems_to_connect = [item.replace(f"{self.key['side']}_", self.simple_side) if f"{self.key['side']}_" in item else item for item in systems_to_connect]
        return mirrored_systems_to_connect
    
    def mirror_data(self):
        temp_systems_to_be_made = {}
        # For loop to iterate through the keys in 'self.data_to_be_made'
        for key in self.data_to_be_checked.values():
            self.locator_list = []
            # Gather mirror_jnts attrib on each guide!
            mirror_attr_name = f"{key['master_guide']}.{key['master_guide']}_mirror_jnts"
            mirror_attribute = cmds.getAttr(mirror_attr_name, asString=1 )
            print(f"mirror attributes: {mirror_attribute} found on '{mirror_attr_name}'")

            if mirror_attribute == "Yes": # Yes mirror joint
                # Call the other functions
                self.key = key
                print(f"key is this:  {self.key}")
                self.joint_list = self.mirror_joints()
                self.get_mirrored_side()
                self.mirrored_system_to_connect = self.get_mirrored_system_to_connect()
                # self.create_mirrored_guides()
                self.master_guide = [] # self.create_mirrored_master_guide()
                # self.copy_mirrored_attrs()

                # create temp dict to store same module data as 'add_module() from ui.py'
                temp_dictionary = {
                    "module": key["module"], 
                    "master_guide": self.master_guide,
                    "guide_list": self.locator_list,
                    "scale": key["scale"],
                    "joints": self.joint_list,
                    "side": self.side,
                    "guide_connectors": [],
                    "systems_to_connect": self.mirrored_system_to_connect,
                    "ik_ctrl_list": [],
                    "fk_ctrl_list": [],
                    "ik_joint_list": [],
                    "fk_joint_list": []
                }

                # Assign the temp dict to 'temp_systems_to_be_made' w 'self.master_guide'
                # as the key!
                temp_systems_to_be_made[self.master_guide] = temp_dictionary
        
        # Update the 'data_to_be_made' dict with this new data
        self.data_to_be_checked.update(temp_systems_to_be_made)

    def get_mirror_data(self):
        return self.data_to_be_checked




