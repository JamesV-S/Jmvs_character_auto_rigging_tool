
import maya.cmds as cmds
import importlib
import os

from systems import jnts
from systems.utils import utils, control_shape, guide_data, system_custom_attr
importlib.reload(jnts)
importlib.reload(utils)
importlib.reload(control_shape)
importlib.reload(guide_data)
importlib.reload(system_custom_attr)

class MirroredSys:
    def __init__(self, systems_config):
        self.orig_data = systems_config
        print("Doing Mirrored System...")
        self.calc_mirroring()

    def determine_opposite_side(self):
        current_side = self.current_item["side"]
        self.opposite_side = "_R" if current_side == "_L" else "_L" if current_side == "_R" else ""

    def generate_mirror_guides(self):
        guide_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "imports", "guide_shape.abc")
        print(f"Guide Shape File Path: {guide_file_path}")
        mirror_guides = []

        for guide in self.current_item["guide_list"]:
            position = cmds.xform(guide, q=True, ws=True, t=True)
            rotation = cmds.xform(guide, q=True, ws=True, ro=True)

            if "master" in guide:
                guide_name = f"master_{guide[7:-2]}{self.opposite_side}"
                new_guide = control_shape.controlTypes(guide_name, [5, 5, 5]).create_octagon()
                cmds.setAttr(f"{guide_name}.overrideEnabled", 1)
                cmds.setAttr(f"{guide_name}.overrideColor", 9)
                cmds.scale(8, 8, 8, guide_name)
                cmds.makeIdentity(guide_name, apply=True, scale=True)
            else:
                guide_name = f"{guide[:-2]}{self.opposite_side}"
                imported_guide_file = cmds.file(guide_file_path, i=True, namespace="guide_shape_import", rnn=True)
                cmds.scale(self.module.guide_scale + 0.5, self.module.guide_scale + 0.5, self.module.guide_scale + 0.5, imported_guide_file)
                new_guide = cmds.rename(imported_guide_file[0], guide_name)
                cmds.makeIdentity(guide_name, apply=True, scale=True)
                utils.colour_guide_custom_shape(guide_name)

            cmds.xform(new_guide, t=position, ro=rotation)
            mirror_guides.append(new_guide)
            cmds.addAttr(mirror_guides, ln="original_guide", at="enum", en=guide[8:-2], k=False)

        print(f"Mirrored Guides Created: {mirror_guides}")

    def calc_mirroring(self):
        for item in self.orig_data.values():
            self.current_item = item
            self.determine_opposite_side()
            self.generate_mirror_guides()

    def get_mirror_results(self):
        return self.orig_data