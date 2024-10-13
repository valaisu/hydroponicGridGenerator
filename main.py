import bpy
from functions import *
# TODO: Code some kind of GUI
# TODO: Add fail-proofing
# TODO: Add margins

BASE_PLATFORM_SIZE = 12
ARM_BASE_LOC = 5
ARM_MIN_LOC = 3.5
CORNER_BASE_LOC = 6
EDGE_BASE_HEIGHT = 1

CONNECTOR_BASE_START = 1
CONNECTOR_BASE_MID = 2
CONNECTOR_BASE_END = 3


MIN_PLATFORM_SIZE = 12
MAX_PLATFORM_SIZE = 20

PLATFORM_NAME = "platform"
PLATFORM_PATH = "models_4.0/ModularPlatform.blend"
SUPPORT_PATH = "models_4.0/Supports.blend"
SAVE_TO = "output/platform_ready.blend"


PLATFORM_CORNER_VERT_GROUPS = ["RU", "LU", "RD", "LD"]
PLATFORM_ARM_VERT_GROUPS = ["RUarm", "LUarm", "RDarm", "LDarm"]
PLATFORM_EDGE_VERT_GROUP = "Edges"
MOVE_INSTRUCTIONS_CORNER = {"RU" : (1, 1, 0), "LU" : (-1, 1, 0), "RD" : (1, -1, 0), "LD" : (-1, -1, 0)}
MOVE_INSTRUCTIONS_ARM = {"RUarm" : (1, 1, 0), "LUarm" : (-1, 1, 0), "RDarm" : (1, -1, 0), "LDarm" : (-1, -1, 0)}

CONNECTOR_VERT_GROUPS = ["FemaleHead", "MaleHead", "FlatHead"]
CONNECTOR_OBJECT = ["ConnectorFemale", "ConnectorMale", "ConnectorFlat"]


def get_max_boolean(arm_loc, corner_loc):
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


def edit_platforms(x_size, y_size, height):

    x_move_corners = (x_size - BASE_PLATFORM_SIZE) / 2
    y_move_corners = (y_size - BASE_PLATFORM_SIZE) / 2

    bpy.ops.wm.open_mainfile(filepath=PLATFORM_PATH)

    # move corners
    move_instruction_multipliers = (x_move_corners, y_move_corners, 1)
    for name in PLATFORM_CORNER_VERT_GROUPS:
        instr = tuple(a*b for a, b in zip(move_instruction_multipliers, MOVE_INSTRUCTIONS_CORNER[name]))
        move_vertices(PLATFORM_NAME, [name], instr)

    # move arms
    corner_loc_x = CORNER_BASE_LOC + x_move_corners
    corner_loc_y = CORNER_BASE_LOC + y_move_corners
    arm_loc_x = (2 * ARM_MIN_LOC + 1 * corner_loc_x) / 3
    arm_loc_y = (2 * ARM_MIN_LOC + 1 * corner_loc_y) / 3

    arm_move = (arm_loc_x - ARM_BASE_LOC, arm_loc_y - ARM_BASE_LOC, 0)
    for name in PLATFORM_ARM_VERT_GROUPS:
        instr = tuple(a*b for a, b in zip(arm_move, MOVE_INSTRUCTIONS_ARM[name]))
        move_vertices(PLATFORM_NAME, [name], instr)

    # edge height
    move_vertices(PLATFORM_NAME, [PLATFORM_EDGE_VERT_GROUP], (0, 0, height - EDGE_BASE_HEIGHT))

    # save base piece
    bpy.ops.wm.save_as_mainfile(filepath=SAVE_TO)

    # Generate corners (use mirrors?)
    # Note: diagonally opposite corners are identical


    return arm_loc_x, arm_loc_y


def edit_supports(arm_loc_x, arm_loc_y, corner_loc_x, corner_loc_y):

    x_dist_between = arm_loc_x
    x_dist_to_edge = corner_loc_x - arm_loc_x
    y_dist_to_edge = corner_loc_y - arm_loc_y

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
    create_support(middle, [y_dist_to_edge, arm_loc_x, arm_loc_y, x_dist_to_edge], "output/support_mid_LU.blend")  # LU
    create_support(middle, [y_dist_to_edge, x_dist_to_edge, arm_loc_y, arm_loc_x], "output/support_mid_RU.blend")  # RU
    create_support(middle, [arm_loc_y, arm_loc_x, y_dist_to_edge, x_dist_to_edge], "output/support_mid_LD.blend")  # LD
    create_support(middle, [arm_loc_y, x_dist_to_edge, y_dist_to_edge, arm_loc_x], "output/support_mid_RD.blend")  # RD
    
    # edges
    create_support(edge_U, [y_dist_to_edge, arm_loc_x, arm_loc_y, x_dist_to_edge], "output/support_edge_U1.blend")
    create_support(edge_U, [y_dist_to_edge, x_dist_to_edge, arm_loc_y, arm_loc_x], "output/support_edge_U2.blend")
    
    create_support(edge_R, [y_dist_to_edge, x_dist_to_edge, arm_loc_y, arm_loc_x], "output/support_edge_R1.blend")
    create_support(edge_R, [arm_loc_y, x_dist_to_edge, y_dist_to_edge, arm_loc_x], "output/support_edge_R2.blend")
    
    create_support(edge_D, [arm_loc_y, arm_loc_x, y_dist_to_edge, x_dist_to_edge], "output/support_edge_D1.blend")
    create_support(edge_D, [arm_loc_y, x_dist_to_edge, y_dist_to_edge, arm_loc_x], "output/support_edge_D2.blend")
    
    create_support(edge_L, [y_dist_to_edge, arm_loc_x, arm_loc_y, x_dist_to_edge], "output/support_edge_L1.blend")
    create_support(edge_L, [arm_loc_y, arm_loc_x, y_dist_to_edge, x_dist_to_edge], "output/support_edge_L2.blend")
    
    # corners
    create_support(corner_LU, [y_dist_to_edge, arm_loc_x, arm_loc_y, x_dist_to_edge], "output/support_mid_LU.blend")  # LU
    create_support(corner_RU, [y_dist_to_edge, x_dist_to_edge, arm_loc_y, arm_loc_x], "output/support_mid_RU.blend")  # RU
    create_support(corner_LD, [arm_loc_y, arm_loc_x, y_dist_to_edge, x_dist_to_edge], "output/support_mid_LD.blend")  # LD
    create_support(corner_RD, [arm_loc_y, x_dist_to_edge, y_dist_to_edge, arm_loc_x], "output/support_mid_RD.blend")  # RD


def create_support(parts: list[str], lengths: list[float], save_file):
    # parts, lengths = [up, right, down, left]
    #                         ConnectorFemale
    part_names = {"Female" : "ConnectorFemale", "Male" : "ConnectorMale", "Flat" : "ConnectorFlat"}
    
    bpy.ops.wm.open_mainfile(filepath=SUPPORT_PATH)

    for i, p in enumerate(parts):
        # duplicate correct part
        # select
        obj = duplicate_and_select(part_names[p])
        
        # stretch correct amount
        name = obj.name
        move_vertices(name, ["Head"], [0, lengths[i] - CONNECTOR_BASE_END, 0])
        
        # rotate 
        rotate(name, -90 * i, "Z")

    # remove base parts
    delete("ConnectorFemale")
    delete("ConnectorMale")
    delete("ConnectorFlat")
   
    # save
    bpy.ops.wm.save_as_mainfile(filepath=save_file)



def main():

    x, y = ask_container_size()
    x_size, y_size, x_amount, y_amount = calc_grid_dim_limits(x, y)
    height = float(input(" Desired edge height: "))
    print(f" Creating platforms of size {x_size:.2f}cm *{y_size:.2f}cm \n Amount to be printed: {x_amount} * {y_amount} = {x_amount*y_amount}")
    arm_loc_x, arm_loc_y =  edit_platforms(x_size, y_size, height)
    #edit_platforms(15, 15)
    corner_loc_x = x_size/2
    corner_loc_y = y_size/2
    edit_supports(arm_loc_x, arm_loc_y, corner_loc_x, corner_loc_y)
    return 0


if __name__ == "__main__":
    main()




