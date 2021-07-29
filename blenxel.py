import bpy
import math
import random

# source object workflow
# set source object
sourceName = bpy.context.object.name
source = bpy.data.objects[sourceName]

bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})
bpy.context.object.name = sourceName + "_Voxelized"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
bpy.ops.object.convert(target='MESH')

# hide the source
source.hide_render = True
source.hide_viewport = True

# target object workflow
# set target object
targetName = bpy.context.object.name
target = bpy.data.objects[targetName]

# turn target into block
bpy.ops.object.modifier_add(type='REMESH')
bpy.context.object.modifiers["Remesh"].mode = 'BLOCKS'
bpy.context.object.modifiers["Remesh"].octree_depth = 5
bpy.context.object.modifiers["Remesh"].use_remove_disconnected = False
bpy.ops.object.modifier_apply(modifier="Remesh")

# transfer UV's to target
bpy.ops.object.modifier_add(type='DATA_TRANSFER')
bpy.context.object.modifiers["DataTransfer"].use_loop_data = True
bpy.context.object.modifiers["DataTransfer"].data_types_loops = {'UV'}
bpy.context.object.modifiers["DataTransfer"].loop_mapping = 'POLYINTERP_NEAREST'
bpy.context.object.modifiers["DataTransfer"].object = source
bpy.ops.object.datalayout_transfer(modifier="DataTransfer")
bpy.ops.object.modifier_apply(modifier="DataTransfer")

# reduce faces to single color
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_mode(type='FACE')
bpy.context.area.ui_type = 'UV'
bpy.context.scene.tool_settings.use_uv_select_sync = False
bpy.context.space_data.uv_editor.sticky_select_mode = 'DISABLED'
bpy.context.scene.tool_settings.uv_select_mode = 'FACE'
bpy.context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'
bpy.ops.mesh.select_all(action='DESELECT')

# the latest version change the random percent to ratio(float)
count = 0
while count < 1:
    bpy.ops.mesh.select_random(ratio=round(count,2), seed = random.randint(1,100))
    bpy.ops.uv.select_all(action='SELECT')
    bpy.ops.transform.resize(value=(0.001, 0.001, 0.001))
    bpy.ops.mesh.hide(unselected=False)
    count+= 0.1
    
# return to previous context
bpy.context.area.ui_type = 'VIEW_3D'
bpy.ops.mesh.reveal()
bpy.ops.object.editmode_toggle()

