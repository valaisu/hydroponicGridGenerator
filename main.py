import bpy
from functions import *
# Later code some kind of GUI

BASE_PLATFORM_SIZE = 12

MIN_PLATFORM_SIZE = 12
MAX_PLATFORM_SIZE = 20

PLATFORM_NAME = "platform"
PLATFORM_PATH = "models/ModularPlatform.blend"
SAVE_TO = "output/platform_ready.blend"


PLATFORM_CORNER_VERT_GROUPS = ["RU", "LU", "RD", "LD"]
MOVE_INSTRUCTIONS = {"RU" : (1, 1, 0), "LU" : (-1, 1, 0), "RD" : (1, -1, 0), "LD" : (-1, -1, 0)}


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

    x_move = (x_size - BASE_PLATFORM_SIZE) / 2
    y_move = (y_size - BASE_PLATFORM_SIZE) / 2
    move_instruction_multipliers = (x_move, y_move, 1)

    bpy.ops.wm.open_mainfile(filepath=PLATFORM_PATH)

    # TODO: Edit the files here
    # Note: at least 2 unique corner pieces are needed along with the base piece

    # Get correct size
    for name in PLATFORM_CORNER_VERT_GROUPS:
        instr = tuple(a*b for a, b in zip(move_instruction_multipliers, MOVE_INSTRUCTIONS[name]))
        move_vertices(PLATFORM_NAME, [name], instr)
    
    bpy.ops.wm.save_as_mainfile(filepath=SAVE_TO)

    

def main():

    x, y = ask_container_size()
    x_size, y_size, x_amount, y_amount = calc_grid_dim_limits(x, y)
    print(f" Creating platforms of size {x_size:.2f}cm *{y_size:.2f}cm \n Amount to be printed: {x_amount} * {y_amount} = {x_amount*y_amount}")
    edit_platforms(x_size, y_size)
    return 0


if __name__ == "__main__":
    main()




