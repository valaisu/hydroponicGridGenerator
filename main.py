import bpy
from functions import *
# Later code some kind of GUI

BASE_PLATFORM_SIZE = 12
ARM_BASE_LOC = 5
ARM_MIN_LOC = 3.5
CORNER_BASE_LOC = 6


MIN_PLATFORM_SIZE = 12
MAX_PLATFORM_SIZE = 20

PLATFORM_NAME = "platform"
PLATFORM_PATH = "models_4.0/ModularPlatform.blend"
SAVE_TO = "output/platform_ready.blend"


PLATFORM_CORNER_VERT_GROUPS = ["RU", "LU", "RD", "LD"]
PLATFORM_ARM_VERT_GROUPS = ["RUarm", "LUarm", "RDarm", "LDarm"]
MOVE_INSTRUCTIONS_CORNER = {"RU" : (1, 1, 0), "LU" : (-1, 1, 0), "RD" : (1, -1, 0), "LD" : (-1, -1, 0)}
MOVE_INSTRUCTIONS_ARM = {"RUarm" : (1, 1, 0), "LUarm" : (-1, 1, 0), "RDarm" : (1, -1, 0), "LDarm" : (-1, -1, 0)}


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


def edit_platforms(x_size, y_size):

    x_move_corners = (x_size - BASE_PLATFORM_SIZE) / 2
    y_move_corners = (y_size - BASE_PLATFORM_SIZE) / 2

    bpy.ops.wm.open_mainfile(filepath=PLATFORM_PATH)

    # TODO: Edit the files here
    # Note: at least 2 unique corner pieces are needed along with the base piece

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
    #print(arm_move)
    for name in PLATFORM_ARM_VERT_GROUPS:
        instr = tuple(a*b for a, b in zip(arm_move, MOVE_INSTRUCTIONS_ARM[name]))
        move_vertices(PLATFORM_NAME, [name], instr)

    # save
    bpy.ops.wm.save_as_mainfile(filepath=SAVE_TO)


def edit_supports():


    pass


def main():

    x, y = ask_container_size()
    x_size, y_size, x_amount, y_amount = calc_grid_dim_limits(x, y)
    print(f" Creating platforms of size {x_size:.2f}cm *{y_size:.2f}cm \n Amount to be printed: {x_amount} * {y_amount} = {x_amount*y_amount}")
    edit_platforms(x_size, y_size)
    #edit_platforms(15, 15)
    return 0


if __name__ == "__main__":
    main()




