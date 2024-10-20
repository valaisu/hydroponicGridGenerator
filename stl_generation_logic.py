import bpy
from functions import *
# TODO: Code some kind of GUI
# TODO: Add fail-proofing
# TODO: Add margins

from constants import *

def get_max_bevel(arm_loc, corner_loc):
    return corner_loc - arm_loc


def ask_container_size():
    print(" Input the container dimensions in cm")
    x = float(input("X: "))
    y = float(input("Y: "))
    return x, y


def calc_grid_dim_limits(x, y):
    x_max = round(x/MIN_PLATFORM_SIZE - 0.49999)
    y_max = round(y/MIN_PLATFORM_SIZE - 0.49999)
    x_min = round(x/MAX_PLATFORM_SIZE + 0.50000)
    y_min = round(y/MAX_PLATFORM_SIZE + 0.50000)
    print(f" Possible X counts: {x_min} - {x_max}, corresponding to platform sizes of {(x/x_max):.2f} - {(x/x_min):.2f} cm")
    print(f" Possible Y counts: {y_min} - {y_max}, corresponding to platform sizes of {(y/y_max):.2f} - {(y/y_min):.2f} cm")
    print(" Please choose the desired dimensions")
    x_amount = int(input("X amount: "))
    y_amount = int(input("Y amount: "))
    x_size = x/x_amount
    y_size = y/y_amount
    return x_size, y_size, x_amount, y_amount


def edit_platforms(x_size, y_size, x_amount, y_amount, height, bevel_width, bevel_count, margin, scale):

    # calc amounts
    corners = 2 # 2 unique corners
    middles = x_amount*y_amount - 4 # everything except corners are middles

    x_move_corners = (x_size - BASE_PLATFORM_SIZE) / 2
    y_move_corners = (y_size - BASE_PLATFORM_SIZE) / 2

    bpy.ops.wm.open_mainfile(filepath=PLATFORM_PATH)

    # move corners
    move_instruction_multipliers = (x_move_corners-margin, y_move_corners-margin, 1)
    for name in PLATFORM_CORNER_VERT_GROUPS:
        instr = tuple(a*b for a, b in zip(move_instruction_multipliers, MOVE_INSTRUCTIONS_CORNER[name]))
        move_vertices(PLATFORM_NAME, [name], instr)
    # move sides
    for name in PLATFORM_EDGE_VERT_GROUPS:
        instr = tuple(a*b for a, b in zip(move_instruction_multipliers, MOVE_INSTRUCTIONS_EDGE[name]))
        move_vertices(PLATFORM_NAME, [name], instr)
    
    # move arms
    x_corner_loc = CORNER_BASE_LOC + x_move_corners
    y_corner_loc = CORNER_BASE_LOC + y_move_corners
    arm_loc_x = (2 * ARM_MIN_LOC + 1 * x_corner_loc) / 3
    arm_loc_y = (2 * ARM_MIN_LOC + 1 * y_corner_loc) / 3

    arm_move = (arm_loc_x - ARM_BASE_LOC, arm_loc_y - ARM_BASE_LOC, 0)
    for name in PLATFORM_ARM_VERT_GROUPS:
        instr = tuple(a*b for a, b in zip(arm_move, MOVE_INSTRUCTIONS_ARM[name]))
        move_vertices(PLATFORM_NAME, [name], instr)

    # edge height
    move_vertices(PLATFORM_NAME, [PLATFORM_EDGE_VERT_GROUP], (0, 0, height - EDGE_BASE_HEIGHT))

    # scale
    scale_all(scale)

    # save base piece
    bpy.ops.wm.save_as_mainfile(filepath=f"output/platform_middle_{middles}x.blend")
    export(f"output/platform_middle_{middles}x.stl")

    # the file is still open
    # NOTE: diagonally opposite corners are identical
    # NOTE: the model has been scaled, but the bevel uses LOCAL SCALE
    # LU/RD corner:
    bevel_vertex_group_edges(PLATFORM_NAME, ["RU"], bevel_width, bevel_count)  # 
    bpy.ops.wm.save_as_mainfile(filepath=f"output/platform_corner_LU_RD_{corners}x.blend")
    export(f"output/platform_corner_LU_RD_{corners}x.stl")

    # LD/RU corner:
    mirror(PLATFORM_NAME, [True, False, False])  # mirror along x
    bpy.ops.wm.save_as_mainfile(filepath=f"output/platform_corner_LD_RU_{corners}x.blend")
    export(f"output/platform_corner_LD_RU_{corners}x.stl")
    return arm_loc_x, arm_loc_y


def edit_supports(arm_loc_x, arm_loc_y, x_corner_loc, y_corner_loc, edge_lift, margin, x_amount, y_amount, scale):

    # Calculate how many of each piece needed
    corners = 2                             # two unique corners
    L_R_edges = y_amount-1                  # two unique edges
    D_U_edges = x_amount-1                  # two unique
    middles = (x_amount-1) * (y_amount-1)   # four uniques middles

    x_dist_between = arm_loc_x
    x_arm_edge_dist = x_corner_loc - arm_loc_x
    y_arm_edge_dist = y_corner_loc - arm_loc_y

    # The types of parts, clockwise, starting from 12 o clock
    # So 12 and 3 o clock are always female, and 6 and 9 are always male
    middle = ["Female", "Female", "Male", "Male"]

    edge_U = ["Flat", "Female", "Male", "Male"]
    edge_R = ["Female", "Flat", "Male", "Male"]
    edge_D = ["Female", "Female", "Flat", "Male"]
    edge_L = ["Female", "Female", "Male", "Flat"]

    corner_LU = ["Flat", "Female", "Male", "Flat"]
    corner_RU = ["Flat", "Flat", "Male", "Male"]
    corner_LD = ["Female", "Female", "Flat", "Flat"]
    corner_RD = ["Female", "Flat", "Flat", "Male"]

    # Up to 16 unique pieces are needed
    #  
    # create the middle pieces
    if (middles):
        create_support(middle, [y_arm_edge_dist, arm_loc_x, arm_loc_y, x_arm_edge_dist], edge_lift, margin, scale, f"output/support_mid_LU_{middles}x.blend")  # LU
        create_support(middle, [y_arm_edge_dist, x_arm_edge_dist, arm_loc_y, arm_loc_x], edge_lift, margin, scale, f"output/support_mid_RU_{middles}x.blend")  # RU
        create_support(middle, [arm_loc_y, arm_loc_x, y_arm_edge_dist, x_arm_edge_dist], edge_lift, margin, scale, f"output/support_mid_LD_{middles}x.blend")  # LD
        create_support(middle, [arm_loc_y, x_arm_edge_dist, y_arm_edge_dist, arm_loc_x], edge_lift, margin, scale, f"output/support_mid_RD_{middles}x.blend")  # RD
    
    # edges
    if L_R_edges:
        create_support(edge_L, [y_arm_edge_dist, arm_loc_x, arm_loc_y, x_arm_edge_dist], edge_lift, margin, scale, f"output/support_edge_L1_{L_R_edges}x.blend")
        create_support(edge_L, [arm_loc_y, arm_loc_x, y_arm_edge_dist, x_arm_edge_dist], edge_lift, margin, scale, f"output/support_edge_L2_{L_R_edges}x.blend")
        create_support(edge_R, [y_arm_edge_dist, x_arm_edge_dist, arm_loc_y, arm_loc_x], edge_lift, margin, scale, f"output/support_edge_R1_{L_R_edges}x.blend")
        create_support(edge_R, [arm_loc_y, x_arm_edge_dist, y_arm_edge_dist, arm_loc_x], edge_lift, margin, scale, f"output/support_edge_R2_{L_R_edges}x.blend")
    if D_U_edges:
        create_support(edge_D, [arm_loc_y, arm_loc_x, y_arm_edge_dist, x_arm_edge_dist], edge_lift, margin, scale, f"output/support_edge_D1_{D_U_edges}x.blend")
        create_support(edge_D, [arm_loc_y, x_arm_edge_dist, y_arm_edge_dist, arm_loc_x], edge_lift, margin, scale, f"output/support_edge_D2_{D_U_edges}x.blend")
        create_support(edge_U, [y_arm_edge_dist, x_arm_edge_dist, arm_loc_y, arm_loc_x], edge_lift, margin, scale, f"output/support_edge_U2_{D_U_edges}x.blend")
        create_support(edge_U, [y_arm_edge_dist, arm_loc_x, arm_loc_y, x_arm_edge_dist], edge_lift, margin, scale, f"output/support_edge_U1_{D_U_edges}x.blend")
    
    # corners, always exist
    create_support(corner_LU, [y_arm_edge_dist, arm_loc_x, arm_loc_y, x_arm_edge_dist], edge_lift, margin, scale, f"output/support_corner_LU_{corners}x.blend")  # LU
    create_support(corner_RU, [y_arm_edge_dist, x_arm_edge_dist, arm_loc_y, arm_loc_x], edge_lift, margin, scale, f"output/support_corner_RU_{corners}x.blend")  # RU
    create_support(corner_LD, [arm_loc_y, arm_loc_x, y_arm_edge_dist, x_arm_edge_dist], edge_lift, margin, scale, f"output/support_corner_LD_{corners}x.blend")  # LD
    create_support(corner_RD, [arm_loc_y, x_arm_edge_dist, y_arm_edge_dist, arm_loc_x], edge_lift, margin, scale, f"output/support_corner_RD_{corners}x.blend")  # RD

    # test prints, always exist
    create_test_prints(x_corner_loc, y_corner_loc, edge_lift, margin, x_amount, y_amount, scale) #TODO: fix amounts


def create_support(parts: list[str], lengths: list[float], edge_lift, margin, scale, save_file):
    # parts, lengths = list[up, right, down, left]
    part_names = {"Female" : "ConnectorFemale", "Male" : "ConnectorMale", "Flat" : "ConnectorFlat"}
    
    bpy.ops.wm.open_mainfile(filepath=SUPPORT_PATH)

    for i, p in enumerate(parts):
        # duplicate correct part
        # select
        obj = duplicate_and_select(part_names[p])
        
        # stretch correct amount
        name = obj.name
        m = margin if p != "Flat" else 0  # no margins on flat edges
        move_vertices(name, ["Head"], [0, lengths[i] - CONNECTOR_BASE_END - m, 0])
        # apply edge lift
        if p == "Flat" and edge_lift:
            if lengths[i] - CONNECTOR_BASE_MID - edge_lift < -1:
                print("   This is potentially bad")
            move_vertices(name, ["Middle"], [0, lengths[i] - CONNECTOR_BASE_MID - edge_lift, 0])  # move middle edge_lift-distance away from edge
            move_vertices(name, ["Head"], [0, 0, edge_lift])  # and thus the edge lift has a 45 deg angle, which is stable to print
        
        # rotate 
        rotate(name, -90 * i, "Z")

    # remove base parts
    delete("ConnectorFemale")
    delete("ConnectorMale")
    delete("ConnectorFlat")
   
    # scale
    scale_all(scale)

    # save
    bpy.ops.wm.save_as_mainfile(filepath=save_file)
    export(save_file[:-6] + ".stl")




def create_test_prints(x_corner_loc, y_corner_loc, edge_lift, margin, x_amount, y_amount, scale):

    create_test_support(True, [False, True], x_corner_loc, edge_lift, margin, scale, "output/test_x_edge_end_1x.blend")
    create_test_support(True, [False, False], x_corner_loc, edge_lift, margin, scale, f"output/test_x_mid_{x_amount}x.blend")
    create_test_support(True, [True, False], x_corner_loc, edge_lift, margin, scale, "output/test_x_edge_start_1x.blend")
    
    create_test_support(False, [False, False], y_corner_loc, edge_lift, margin, scale, f"output/test_y_mid_{y_amount}x.blend")
    create_test_support(False, [True, False], y_corner_loc, edge_lift, margin, scale, "output/test_y_edge_start_1x.blend")
    create_test_support(False, [False, True], y_corner_loc, edge_lift, margin, scale, "output/test_y_edge_end_1x.blend")
    


def create_test_support(dir_is_x: bool, flat: tuple[bool, bool], size, edge_lift, margin, scale, save_file):
    # dir: x or y
    move = (1,0,0) if dir_is_x else (0,1,0)
    path = TEST_PATH_X if dir_is_x else TEST_PATH_Y
    bpy.ops.wm.open_mainfile(filepath=path)
    
    multiplier = size - TEST_CONNECTOR_SIZE  - 2 * margin  # times 2, because two moves are made with one action here
    multiplier_vec = (multiplier, multiplier, 0)
    instr = tuple(a*b for a, b in zip(move, multiplier_vec))
    #print(f" {instr}, {size}")

    # flat: is one of the ends flat
    if flat[0] or flat[1]:
        deleted = "ConnectorStart" if flat[0] else "ConnectorEnd"
        this = "ConnectorEnd" if flat[0] else "ConnectorStart"
        #print(" ", this, deleted)
        delete(deleted)
        delete("ConnectorMid")
        # correct size
        move_vertices(this, ["End"], instr)
        # edge lifts
        middle_move = (-1 + edge_lift)
        multiplier_vec = (middle_move, middle_move, 0)
        instr_el = tuple(a*b for a, b in zip(move, multiplier_vec))
        move_vertices(this, ["Mid"], instr_el)
        move_vertices(this, ["Start"], (0, 0, edge_lift))

    else:
        delete("ConnectorStart")
        delete("ConnectorEnd")
        move_vertices("ConnectorMid", ["End"], instr)
        
    # scale
    scale_all(scale)

    # save
    bpy.ops.wm.save_as_mainfile(filepath=save_file)
    export(save_file[:-6] + ".stl")


def generate(x_size, y_size, edge_height, bevel_width, bevel_count, margin, x_amount, y_amount, edge_lift, scale):
    arm_loc_x, arm_loc_y = edit_platforms(x_size, y_size, x_amount, y_amount, edge_height, bevel_width, bevel_count, margin, scale)
    x_corner_loc = x_size/2
    y_corner_loc = y_size/2
    edit_supports(arm_loc_x, arm_loc_y, x_corner_loc, y_corner_loc, edge_lift, margin, x_amount, y_amount, scale)
    pass


'''
def main():

    #x, y = ask_container_size()
    #x_size, y_size, x_amount, y_amount = calc_grid_dim_limits(x, y)
    #edge_height = float(input(" Desired edge height: "))
    #bevel_width = float(input(" Desired bevel height: "))
    #edge_lift = float(input(" Desired edge lift: "))
    #bevel_count = int(input(" Desired bevel count: "))
    #margin = float(input(" Margin per part "))  # TODO: I don't actually know what is a good margin
    #scale = float(input(" Final scaling factor "))
    x_size, y_size, edge_height, bevel_width, bevel_count, margin, x_amount, y_amount, edge_lift, scale = 17.5, 20.0, 2, 1, 10, 0.01, 4, 2, 1.5, 10.0
    generate(x_size, y_size, edge_height, bevel_width, bevel_count, margin, x_amount, y_amount, edge_lift, scale)

    #print(f" Creating platforms of size {x_size:.2f}cm *{y_size:.2f}cm \n Amount to be printed: {x_amount} * {y_amount} = {x_amount*y_amount}")
    #arm_loc_x, arm_loc_y = edit_platforms(x_size, y_size, x_amount, y_amount, edge_height, bevel_width, bevel_count, margin, scale)
    #x_corner_loc = x_size/2
    #y_corner_loc = y_size/2
    #edit_supports(arm_loc_x, arm_loc_y, x_corner_loc, y_corner_loc, edge_lift, margin, x_amount, y_amount, scale)
    return 0


main()

'''


