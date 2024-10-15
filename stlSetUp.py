from stl import mesh
import numpy as np
import copy 


'''
The point is to create a function that reads the output stl files as a stream.
The function knows the users print area, and base on that, combines
the .stl files into fewer stl files. The arrangement of the meshes
will be done using bounding boxes, so it won't of course be optimal, 
just good enough.  


'''



def arrange(input_folder_path: str, output_folder_path: str, margin_edge: int = 5, margin_between: int = 5):
    # in margins 1 unit = 1mm
    # n = number, look for patter '_{k*n}x' in .stl file name to 
    # figure out how many times it should be printed

    #TODO:

    # Read all files
    # output_file = new_file
    # while (next file)
    #   for (file_iterations)
    #      if (ouput full)
    #         save output
    #         output = new_file
    #      add to output


    pass





