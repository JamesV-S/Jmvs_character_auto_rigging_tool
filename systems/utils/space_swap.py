
import maya.cmds as cmds
import importlib
import re
import maya.api.OpenMaya as om

from systems.utils import (utils, OPM)

importlib.reload(utils)
importlib.reload(OPM)

class cr_spaceSwapping():
    def __init__(self, key, ctrl_cog, ctrl_root):
        self.key = key
        self.ctrl_cog = ctrl_cog
        self.ctrl_root = ctrl_root
        
        self.space_list_names = self.key["space_swap"]
        print(f"---------- SPACE: space_list_names is: {self.space_list_names}")
        self.master_space_name = self.space_list_names[0]
        self.pv_space_names = self.space_list_names[1]
        self.start_space_names = self.space_list_names[2]

        if 'arm' in self.key['module']:
            print("------------ SPACE system has found 'arm' name in the module")
            print(f"SPACE/ TOP SPACE NAME: {self.space_list_names[3]}")
            self.top_space_name = self.space_list_names[3]
        else:
            print("SPACE system has NOT found 'arm' name in the module")

        
        #     self.top_space_names = self.space_list_names[3]
        
        # print(f"master; {self.master_space_name}, pv; {self.pv_space_names}, top; {self.start_space_names}")

        # self.guide_list = self.key["guide_list"]
        self.ik_ctrl_list = self.key["ik_ctrl_list"]
        
        rig_type = cmds.getAttr(f"{self.key['master_guide']}.{self.key['master_guide']}_rig_type", asString=1)
        if rig_type == "IKFK" or rig_type == "IK":
            # self.space_space_locators = self.create_locators() # swappos locators!
            loc_master_list = self.create_locators(self.master_space_name) # ['swappos_world_biped_arm_0_L', 
            # 'swappos_COG_biped_arm_0_L', 'swappos_shoulder_biped_arm_0_L', 'swappos_custom_biped_arm_0_L']

            print(f"loc_master_list is : {loc_master_list}")
            loc_pv_list = self.create_locators(self.pv_space_names)
            loc_start_list = self.create_locators(self.start_space_names)
            if 'arm' in self.key['module']:
                loc_top_list = self.create_locators(self.top_space_name)
            
            if 'quad' in self.key['module']:
                self.master_space_ctrl = [item for item in self.ik_ctrl_list if 'quadWrist' in item or 'quadAnkle' in item][0]
                self.start_ctrl = [item for item in self.ik_ctrl_list if 'quadShoulder' in item or 'quadHip' in item][0]
            else:
                self.master_space_ctrl = [item for item in self.ik_ctrl_list if 'wrist' in item or 'ankle' in item][0]
                self.start_ctrl = [item for item in self.ik_ctrl_list if 'shoulder' in item or 'hip' in item][0]
            print( f"333333333333333333 SPACE self.master_space_ctrl is = {self.master_space_ctrl}")
            print( f"333333333333333333 SPACE self.start_ctrl is = {self.start_ctrl}")
            self.pv_ctrl = [item for item in self.ik_ctrl_list if 'pv' in item][0]
            
            if 'arm' in self.key['module']:
                self.top_ctrl = [item for item in self.ik_ctrl_list if 'clavicle' in item or 'scapula' in item][0]

            
            
            # Add attr to controls
            self.add_attr(self.master_space_ctrl, self.master_space_name)
            self.add_attr(self.pv_ctrl, self.pv_space_names)
            self.add_attr(self.start_ctrl, self.start_space_names)
            if 'arm' in self.key['module']:
                self.add_attr(self.top_ctrl, self.top_space_name)
            
            self.match_and_parent_to_ctrl(loc_master_list, self.master_space_ctrl)
            self.match_and_parent_to_ctrl(loc_pv_list, self.pv_ctrl)
            self.match_and_parent_to_ctrl(loc_start_list, self.start_ctrl)

            if 'arm' in self.key['module']:
                self.match_and_parent_to_ctrl(loc_top_list, self.top_ctrl)

            self.cr_nodes_and_connect(ctrl=self.master_space_ctrl, locator_ls=loc_master_list)
            self.cr_nodes_and_connect(ctrl=self.pv_ctrl , locator_ls=loc_pv_list)
            self.cr_nodes_and_connect(ctrl=self.start_ctrl , locator_ls=loc_start_list)
            
            if 'arm' in self.key['module']:
                self.cr_nodes_and_connect(ctrl=self.top_ctrl, locator_ls=loc_top_list)

    def create_locators(self, space_loc_names):
        self.custom_loc_name_id = f"{self.key['module']}_{int(self.key['guide_number'])}{self.key['side']}"
        print(f"swappos names: {self.custom_loc_name_id}")
        created_loc_list = []
        print(f"loc names: {space_loc_names}")
        for item in space_loc_names:
            locator_name = f"swappos_{item}_{self.custom_loc_name_id}"
            if not cmds.objExists(locator_name):
                created_loc_list.append(cmds.spaceLocator(n=locator_name)[0])
        return created_loc_list
                

    def add_attr(self, ctrl, space_names):
        # for obj in ctrl: 
        utils.add_locked_attrib(ctrl, ["SPACE"])
        enum_name_options = [':'.join(space_names)][0]
        print(f"space_names for this control: {enum_name_options}")
        #utils.add_multile_enum_attribute(ctrl, ["Follow"], enum_name_options)
        utils.custom_enum_attr(ctrl, "Follow", enum_name_options)


    # from the created locator list parent to location. 
    # Locators are matched to the same control, like pv or master_ctrl, 
    # then parented to dpaceswap like root, cog...
    def match_and_parent_to_ctrl(self, locator_ls, ctrl):
        for loc in locator_ls:
            cmds.setAttr(f"{loc}.overrideEnabled", 1)
            cmds.setAttr(f"{loc}.overrideColor", 14)
            print(f"match : {loc} to {ctrl}")
            cmds.matchTransform(loc, ctrl)
            
            if "COG" in loc:
                print(f"found COG in locator list > {loc}")
                cmds.parent(loc, self.ctrl_cog)
            elif "world" in loc or "custom" in loc:
                print(f"found world in loc list > {loc}")
                try: cmds.parent(loc, self.ctrl_root)
                except: pass
            elif "spine" in loc: 
                temp_spine_grp = cmds.group(loc, n=f"tmp_swappos_TOPLOC_{self.custom_loc_name_id}")
                cmds.parent(temp_spine_grp, self.ctrl_root)
                
                # Find out if there are any spine joints in the scene!
                spine_jnt_nm_pattern = re.compile(r"jnt_rig_\d+_spine_\d+")
                all_obj = cmds.ls()
                spine_jnts = [obj for obj in all_obj if spine_jnt_nm_pattern.match(obj)]
                print(spine_jnts)
                if spine_jnts:
                    # figure out which spine_joints are closest to the locator!
                    '''
                    def get_position(obj_name):
                        return om.MVector(cmds.xform(obj_name, query=True, 
                                                     worldSpace=True, translation=True))
                    
                    def find_closest_joint(locator, joints):
                        locator_pos = get_position(locator)
                        return min(joints, key=lambda joint: (locator_pos - get_position(joint)).length())
                    
                    closest_joint = find_closest_joint(loc, spine_jnts)
                    print(f"The closest joint to {loc} is {closest_joint}")
                    '''
                    
                    spine_joint = self.key['systems_to_connect'][-1].replace('guide_', 'jnt_rig_')
                    print("systems to connect: ", spine_joint) # 'systems_to_connect': ['guide_0_clavicle_L', 'guide_0_spine_4']
                    
                    cmds.parentConstraint(spine_joint, loc, mo=1)
                    cmds.select(cl=1)

                else:
                    # No spine for the locator to foolow
                    pass
                    print("did NOT IDNETIFY that this module has a spine module!")
                    # if the spine module doesn't exist, create temp grp for the start_locator to parent to,
                    # otherwise find the closest spine(connect to spine) joint & constrain the locator to it, 
                    
            else:
                # parent remianing locators to the write places
                id = loc.split('_')[1]
                print(f"id: {id}")
                print(f"ctrl_ik_{int(self.key['guide_number'])}_{id}{self.key['side']}")
                ik_ctrl = f"ctrl_ik_{int(self.key['guide_number'])}_{id}{self.key['side']}"
                cmds.parent(loc, ik_ctrl)
            OPM.OpmCleanTool(loc)
        

    def get_loc(self):
        pass

    # space with 2 options needs mmx & blendmatrix only.
    # space with 4 options needs extra 4 condition nodes total,
    # 3 for each other option & the last to tie it together. 
    def cr_nodes_and_connect(self, ctrl, locator_ls):
        print(f"Creat nodes, the locator is: {locator_ls}")
        print(f"Creat nodes, the ctrl is: {ctrl}")
        self.mmx_node_ls = []
        self.bmx_node = []
        self.cond_node_ls = []
        temp_set_attr_cond_list = []
        for loc in locator_ls:
            if "world" in loc: 
                pass
                #print(f"found the world in the name: {loc}")
            else:
                #print(f"didn't find the world in the name: {loc}")
                mmx_node = f"MMXspace_{loc}"
                utils.cr_node_if_not_exists(1, "multMatrix", mmx_node)
                self.mmx_node_ls.append(mmx_node)

        bmx_node = f"BMXspace_{ctrl}"
        utils.cr_node_if_not_exists(0, "blendMatrix", bmx_node)
        # self.bmx_node.append(bmx_node)
        print(f"blend matrix: {bmx_node}")

        # the length of 'locator_ls' is less than 3 or greater than 2 make condition nodes: 
        if len(locator_ls) > 2:
            cond_master_node_name = f"CONDspace_master{ctrl}"
            utils.cr_node_if_not_exists(1, "condition", cond_master_node_name, 
                                        {"colorIfFalseR":0, "colorIfFalseG":0, 
                                         "colorIfFalseB":0, "operation":2 })
            num_ls = [1, 2, 3]
            for loc in locator_ls:
                if "world" in loc: pass
                else:  
                    cond_node_name = f"CONDspace_{loc}"
                    utils.cr_node_if_not_exists(1, "condition", cond_node_name, 
                                                {"colorIfTrueR":1, "colorIfFalseR":0})
                    self.cond_node_ls.append(cond_node_name)
                    temp_set_attr_cond_list.append(cond_node_name)
            for x in range(len(num_ls)):
                cmds.setAttr( f"{temp_set_attr_cond_list[x]}.secondTerm", num_ls[x])
            self.cond_node_ls.append(cond_master_node_name)
            print(f"condition list: {self.cond_node_ls}")
        else:
            # connect follow from pv vtrl to weight in blemd
            utils.connect_attr(f"{ctrl}.Follow", f"{bmx_node}.target[0].weight")
            print("no need for condition nodes")
        
        # Create connections
        print(f"CONNECT_NODES: {locator_ls}") # CONNECT_NODES: ['swappos_wrist_biped_arm_0_L']
        new_locator_ls = [item for item in locator_ls if 'world' not in item]# ignore the world name        
        print(f"new_locator_ls : {new_locator_ls}")
        
        #set the blendmatrix inputmatrix to the location of the 
        
        # connectAttr -f guide_0_wrist_L.worldMatrix[0] BMXspace_ctrl_ik_0_wrist_L.inputMatrix;
        utils.connect_attr(f"{ctrl}.worldMatrix[0]", f"{bmx_node}.inputMatrix")
        
        # disconnectAttr guide_0_wrist_L.worldMatrix[0] BMXspace_ctrl_ik_0_wrist_L.inputMatrix;
        cmds.disconnectAttr(f"{ctrl}.worldMatrix[0]", f"{bmx_node}.inputMatrix")

        element_cond_list = self.cond_node_ls[:-1]
        for x in range(len(new_locator_ls)):
            utils.connect_attr(f"{new_locator_ls[x]}.worldMatrix[0]", f"{self.mmx_node_ls[x]}.matrixIn[0]")
            utils.connect_attr(f"{self.ctrl_root}.worldInverseMatrix[0]", f"{self.mmx_node_ls[x]}.matrixIn[1]")
            utils.connect_attr(f"{self.mmx_node_ls[x]}.matrixSum", f"{bmx_node}.target[{x}].targetMatrix")

        if len(locator_ls) > 2: # do condition bullshit
            rgb_list = ["R", "G", "B"]
            for x in range(len(num_ls)):
                utils.connect_attr(f"{ctrl}.Follow", f"{cond_master_node_name}.firstTerm")
                utils.connect_attr(f"{ctrl}.Follow", f"{element_cond_list[x]}.firstTerm")
                utils.connect_attr(f"{element_cond_list[x]}.outColorR", f"{cond_master_node_name}.colorIfTrue{rgb_list[x]}") 
                utils.connect_attr(f"{cond_master_node_name}.outColor{rgb_list[x]}", f"{bmx_node}.target[{x}].useMatrix")
            pass
            
        for x in range(len(new_locator_ls)):
            utils.connect_attr(f"{bmx_node}.outputMatrix", f"{ctrl}.offsetParentMatrix")

