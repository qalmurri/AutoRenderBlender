import bpy
import math
import os

scene = bpy.context.scene
output_dir = scene.render.filepath

# 5 directions
directions = {
    "N": -270,
    "NE": -225,
    "E": -180,
    "SE": -135,
    "S": -90,
}

# Parts inside armature
parts = [
    "Body",
    "Foot",
    "Head",
    "LeftHand",
    "RightHand",
    "LeftTool",
    "RightTool",
    "Bag",
]

armature = bpy.context.active_object
if armature is None:
    raise Exception("Select the Armature object")

if armature.animation_data is None:
    armature.animation_data_create()

anim_data = armature.animation_data

original_rotation = armature.rotation_euler.copy()

# Store visibility state
original_visibility = {}
for p in parts:
    part_obj = bpy.data.objects.get(p)
    if part_obj:
        original_visibility[p] = part_obj.hide_render

# 🔥 LOOP SEMUA ACTION
for action in bpy.data.actions:

    print(f"Rendering action: {action.name}")

    anim_data.action = action

    # Gunakan frame range dari action
    frame_start = int(action.frame_range[0])
    frame_end = int(action.frame_range[1])

    # Reset frame
    scene.frame_set(frame_start)

    frame_global = 1

    for part in parts:

        part_obj = bpy.data.objects.get(part)
        if part_obj is None:
            print(f"{part} not found, skipping")
            continue

        # Hide semua part
        for p in parts:
            o = bpy.data.objects.get(p)
            if o:
                o.hide_render = True

        # Show hanya part ini
        part_obj.hide_render = False

        for dir_name, angle in directions.items():

            armature.rotation_euler[2] = math.radians(angle)

            for frame in range(frame_start, frame_end + 1):

                scene.frame_set(frame)

                # filename = f"{action.name}_{part}_{dir_name}_{frame_global:04d}.png"
                filename = f"{action.name}_{part}_{frame_global:04d}.png"
                scene.render.filepath = os.path.join(output_dir, filename)

                bpy.ops.render.render(write_still=True)

                frame_global += 1

# restore rotation
armature.rotation_euler = original_rotation

# restore visibility
for p, vis in original_visibility.items():
    part_obj = bpy.data.objects.get(p)
    if part_obj:
        part_obj.hide_render = vis

scene.render.filepath = output_dir

print("✅ Render selesai tanpa merusak animasi lain.")
