from stl import mesh
import numpy as np
import copy 

import os
from os import listdir
from os.path import isfile, join
import re

'''
The point is to create a function that reads the output stl files as a stream.
The function knows the users print area, and base on that, combines
the .stl files into fewer stl files. The arrangement of the meshes
will be done using bounding boxes, so it won't of course be optimal, 
just good enough.  
'''


def extract_print_counts(stl_files: list[str]) -> list[int]:
    counts = []
    pattern = "_\d+x"
    for p in stl_files:
        x = re.findall(pattern, p)
        counts.append(int(x[0][1:-1]))
    return counts

# reads folder combining files with single .stl
def arrange(printer_dimension_x: float, printer_dimension_y: float, input_folder_path: str, output_folder_path: str, scale = 1, margin_edge: int = 0.05, margin_between: int = 0.05):
    
    if scale != 1:
        printer_dimension_x *= scale
        printer_dimension_y *= scale
        margin_between *= scale
        margin_edge *= scale
    
    # get all files
    stl_files = [f for f in listdir(input_folder_path) if isfile(join(input_folder_path, f)) and f.endswith(".stl")]
    print_counts = extract_print_counts(stl_files)
    all_mesh = []
    file_number = 1
    x_filled = margin_edge
    y_filled = margin_edge
    y_row_height = 0

    # files
    for i in range(len(stl_files)):
        path = join(input_folder_path, stl_files[i])
        #print(f"process {path}")
        file = mesh.Mesh.from_file(path)

        # each copy
        for _ in range(print_counts[i]):
            file_width = file.x.max() - file.x.min()
            file_height = file.y.max() - file.y.min()

            # check x
            if file_width + margin_between + x_filled > printer_dimension_x:
                y_filled += y_row_height + margin_between
                x_filled = margin_edge
                y_row_height = 0

            # check y
            if file_height + margin_between + y_filled > printer_dimension_y:
                final_product = mesh.Mesh(np.concatenate([m.data for m in all_mesh]))
                final_product.save(join(output_folder_path, f"print_{file_number}.stl"))
                #print(f"saved print_{file_number}.stl")
                file_number += 1
                all_mesh = []
                x_filled = margin_edge
                y_filled = margin_edge
                y_row_height = 0

            mesh_copy = copy.deepcopy(file)
            mesh_copy.translate([x_filled, y_filled, 0])
            all_mesh.append(mesh_copy)

            x_filled += file_width + margin_between
            y_row_height = max(y_row_height, file_height)

    # save remaining
    if all_mesh:
        final_product = mesh.Mesh(np.concatenate([m.data for m in all_mesh]))
        final_product.save(join(output_folder_path, f"print_{file_number}.stl"))
        #print(f"saved print_{file_number}.stl")   


