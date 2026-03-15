import bpy
import math
import os

scene = bpy.context.scene
output_dir = scene.render.filepath

# 5 directions
directions = {
    "N": 0,
    "NE": 45,
    "E": 90,
    "SE": 135,
    "S": 180,
}

# Parts inside armature
parts = [
    "Body",
    "Foot",
    "Head",
    "LeftHand",
    "RightHand",
]

frame_count = scene.frame_end - scene.frame_start + 1

obj = bpy.context.active_object
if obj is None:
    raise Exception("Select the Armature object")

original_rotation = obj.rotation_euler.copy()

# Store visibility state
original_visibility = {}
for p in parts:
    part_obj = bpy.data.objects.get(p)
    if part_obj:
        original_visibility[p] = part_obj.hide_render

frame_global = 1

for part in parts:

    part_obj = bpy.data.objects.get(part)
    if part_obj is None:
        print(f"{part} not found, skipping")
        continue

    # Hide all parts
    for p in parts:
        o = bpy.data.objects.get(p)
        if o:
            o.hide_render = True

    # Show only current part
    part_obj.hide_render = False

    for dir_name, angle in directions.items():

        obj.rotation_euler[2] = math.radians(angle)

        for frame in range(scene.frame_start, scene.frame_end + 1):

            scene.frame_set(frame)

            filename = f"{part}_{dir_name}_{frame_global:04d}.png"
            scene.render.filepath = os.path.join(output_dir, filename)

            bpy.ops.render.render(write_still=True)

            frame_global += 1

# restore rotation
obj.rotation_euler = original_rotation

# restore visibility
for p, vis in original_visibility.items():
    obj = bpy.data.objects.get(p)
    if obj:
        obj.hide_render = vis

scene.render.filepath = output_dir
