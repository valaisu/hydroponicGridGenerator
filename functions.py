# These functions have been tested to work in blenders scripting 
# tab, on version 4.2.2 . This does not necessarily mean they work 
# outside of Blender, although achieving that is my goal. 

import bpy


def bevel_vertex_group_edges(object_name: str, vertex_group_names: list[str], offset: float, segments: int = 1):

    # Example call:
    # bevel_vertex_group_edges("Cube", ["Group2", "Group"], 1, 3)

    # Select object
    object = bpy.data.objects[object_name]
    object.select_set(True)
    bpy.context.view_layer.objects.active = object # sometimes needed

    o = bpy.context.object  # "retrieves currently active object"

    bpy.ops.object.mode_set( mode = 'EDIT' )
    bpy.ops.mesh.select_all( action = 'DESELECT' )  # deselect vertices

    for group_name in vertex_group_names:
        o.vertex_groups.active = o.vertex_groups.get(group_name)
        bpy.ops.object.vertex_group_select()
        print(group_name)
    
    bpy.ops.mesh.bevel(
        offset = offset,
        segments = segments,
        affect = 'EDGES',
    )    
    
    bpy.ops.object.mode_set( mode = 'OBJECT' )
    object.select_set(False)

