# These functions have been tested to work in blenders scripting 
# tab, on version 4.2.2 . This does not necessarily mean they work 
# outside of Blender, although achieving that is my goal. 

import bpy



def move_vertices(object_name: str, vertex_group_names: list[str], move_vector: tuple[int, int, int]):

    # Example usage:
    # move_vertices("Cube", ["Group2", "Group"], (0, 0.5, 0))

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

    # this is what console prints out when I move using "g"-command
    bpy.ops.transform.translate(value=move_vector, orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)

    
    bpy.ops.object.mode_set( mode = 'OBJECT' )
    object.select_set(False)


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

