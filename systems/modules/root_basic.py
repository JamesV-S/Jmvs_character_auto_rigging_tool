system = ["root", "COG"]
system_pos = {"root": [0,0,0], "root": [0,150,0]}
system_rot = {"root": [0,0,0], "root": [0,0,0]}
side = "None"
space_swapping = []
guide_scale = 1
available_rig_types = ["FK"]

'''1. **Guide Shapes:**
    - Visual markers placed in the 3D scene representing joint positions and 
    orientations.

2. **Attributes:**
    - Custom attributes on guide shapes provide additional information 
    (e.g., joint positions, rotations, control shapes, IK/FK settings).

3. **Reading and Rigging Process:**
    - The rigging tool reads guide shapes and their attributes to:
        - Place joints accurately.
        - Create control objects with specified shapes.
        - Set up IK/FK system based on the provided information.

Blueprint guides streamline the rigging process by providing a clear, visual, 
and attribute-driven reference for setting up complex rig system.'''