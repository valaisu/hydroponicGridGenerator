
# TODO: add more labels to the images
'''
images for:
margins
edge height
'''

titles = [
    "   Container size    ", 
    "   Platform amount   ", 
    "     Edge height     ", 
    "     Bevel size      ", 
    "     Bevel count     ", 
    " Connector edge lift ", 
    "       Margins       ", 
    "     Model scale     ", 
    "Print area dimensions", 
]

generic_info = [
    "Some of params have been pre-filled. These are my guesses of the optimal params. Fill out all params and click generate. This will create a folder with test prints and a folder with the 'real print'. I recommend starting with the test print to verify that the parameters have been chosen correctly. \nClick '?' for a quick explanation of each param. \nTo input decimal numbers, use '.' as the decimal separator. "
]

paragraphs = [
    "Please input the dimensions of your container. It is not important which dimension you choose as X and which as Y, as long as you keep this consistent.",
    "Input the amounts of platforms you want to have in each direction. For the picture above, the correct input would be x=5 and y=3. \nNote that the amount of platforms in each direction is limited by minimum (12cm) and maximum (20cm) sizes of these platforms.",
    "This is the height of the edge as demonstrated in the picture. The edges makes the platform structurally more stable, and allow the platforms to be set on different heights.",
    "Some containers have round edges as demonstrated in the picture. To account for this, the corner pieces need to be trimmed accordingly. Please measure the length of A or alternatively measure B, and divide it by 1.42. If you are unsure of your measurements, go for a bigger number rather than a smaller one. ",
    "This defines the 'roundness' of the corner. Low values are a bit safer if you are unsure of your measurements. High values give rounder corners. ",
    "The bottom seams of the container might be rounded. This value affects the edges of the bottom grid. Please measure the length of A, or alternatively measure B and divide it by 1.42. ",
    "Margins are the distances left between the platforms and between the grid pieces. Note that if you set the margins to 0.0, the pieces are unlikely to fit due to inaccuracies in the printing process. You can always verify your choice with the test prints. ",
    "The models have been made with scale 1 blender unit = 1cm. Scale 10 would mean that in the output file, 10 blender units = 1cm. This would be correct scale for Prusa slicer. Note that your slicer also should have a scaling feature.",
    "The program generates a separate stl file for each individual part, as well as combined stl files, with correct amounts of parts for the whole print. For the latter part, the X and Y dimensions of your printer are needed.",
    
]