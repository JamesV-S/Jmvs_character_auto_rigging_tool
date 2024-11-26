
import maya.cmds as cmds
from systems.utils import OPM, utils
import importlib

importlib.reload(OPM)
importlib.reload(utils)

class connecting_sys_to_connect():
    def __init__(self, master_guide, sys_to_connect, ctrl_root, side):
        print(f"CSTOC: MDL = {master_guide}")
        print(f"CSTOC: sys_to_connect = {sys_to_connect}")
        self.mdl = master_guide
        self.ctrl_root = ctrl_root
        self.side = side
        self.jnt_follow = sys_to_connect[1].replace('guide', 'jnt_rig')

        self.fk_ctrl_follower = sys_to_connect[0].replace('guide', 'ctrl_fk')
        
        print( f"jnt follow: {self.jnt_follow}, fk_ctrl: {self.fk_ctrl_follower}" )
        self.group()
        self.create_nodes()
        self.connect_nodes()


    def group(self):
        if cmds.objExists(f"grp_Foll{self.mdl[6:-2]}{self.jnt_follow.replace('jnt_rig', '')}{self.side}"):
            self.grp = f"grp_Foll{self.mdl[6:-2]}{self.jnt_follow.replace('jnt_rig', '')}{self.side}"
        else:
            self.grp = cmds.group(n=f"grp_Foll{self.mdl[6:-2]}{self.jnt_follow.replace('jnt_rig', '')}{self.side}", em=1)
            cmds.parent(self.grp, 'ctrl_root')
            cmds.matchTransform(self.grp, self.fk_ctrl_follower, pos=1, rot=1, scl=0)
            cmds.parentConstraint(self.jnt_follow, self.grp, n=f"pCons_{self.grp}", mo=1)
    

    def create_nodes(self):
        # multmatrix 
        # connect grp to matrix[0] & root[inverse] to matrix[1]
        # cnnect matrixSum to fk_ctrl OPM
        self.MM_grp_node = f"MM_{self.mdl[6:-2]}{self.jnt_follow.replace('jnt_rig', '')}{self.side}"
        utils.cr_node_if_not_exists(
            util_type=1, node_type="multMatrix", 
            node_name=self.MM_grp_node
            )
        

    def connect_nodes(self):
        utils.connect_attr(f"{self.grp}.worldMatrix[0]", f"{self.MM_grp_node}.matrixIn[0]")
        utils.connect_attr(f"{self.ctrl_root}.worldInverseMatrix[0]", f"{self.MM_grp_node}.matrixIn[1]")
        utils.connect_attr(f"{self.MM_grp_node}.matrixSum", f"{self.fk_ctrl_follower}.offsetParentMatrix")


        
