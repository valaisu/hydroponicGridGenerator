import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# TODO: make this file importable

LIGHT_GREEN = "#91CF99"
DARK_GREEN = "#517A52"
TEXT_GREEN = "#2A2C2A"
BG_WHITE = "#D9D9D9"
BG_GREEN = "#7EC27F"


BASE_PLATFORM_SIZE = 12
ARM_BASE_LOC = 5
ARM_MIN_LOC = 3.5
CORNER_BASE_LOC = 6
EDGE_BASE_HEIGHT = 1

CONNECTOR_BASE_START = 1
CONNECTOR_BASE_MID = 2
CONNECTOR_BASE_END = 3

TEST_CONNECTOR_SIZE = 6

MIN_PLATFORM_SIZE = 12
MAX_PLATFORM_SIZE = 20


def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
        
    points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, 
              x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, 
              x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, 
              x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)


def circular_button(canvas, x, y, radius, text, command):

    circle = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=BG_WHITE, outline="")
    label = canvas.create_text(x, y, text=text, font=("Arial", 11), fill=TEXT_GREEN)
    
    def on_click(event):
        command()
    
    canvas.tag_bind(circle, "<Button-1>", on_click)
    canvas.tag_bind(label, "<Button-1>", on_click)


def rectangular_button(canvas, x1, y1, x2, y2, text, command, radius=0, **kwargs):

    rect = round_rectangle(canvas, x1, y1, x2, y2, radius=radius, **kwargs)
    
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    
    label = canvas.create_text(center_x, center_y, text=text, font=("Arial", 14), fill=TEXT_GREEN)

    def on_click(event):
        command()

    canvas.tag_bind(rect, "<Button-1>", on_click)
    canvas.tag_bind(label, "<Button-1>", on_click)


def add_placeholder(entry, placeholder_text):
    # Store the placeholder text in a list to allow modifications
    placeholder = [placeholder_text]
    
    # Set the placeholder initially
    entry.insert(0, placeholder[0])
    entry.config(fg="grey")

    # remove when clicked
    def on_focus_in(event):
        if entry.get() == placeholder[0]:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    # add back if empty
    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder[0])
            entry.config(fg="grey")

    # Bind focus in and focus out events to the Entry widget
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    # Function to update the placeholder dynamically
    def update_placeholder(new_text):
        placeholder[0] = new_text
        if not entry.get().isnumeric(): # if a number, dont override, else:
            entry.delete(0, tk.END)
            entry.insert(0, placeholder[0])
            entry.config(fg="grey")

    return update_placeholder


def create_text_input_unit(root, canvas, x, y, text, placeholder, on_click_function):
    text = tk.Label(root, text=text, bg=LIGHT_GREEN, fg=TEXT_GREEN, font=("Arial", 10))
    text.place(x = x, y = y)

    # button background
    round_rectangle(canvas, x, y+25, x+200, y+50, radius=15, fill=BG_WHITE, outline="")
    # button input
    entry = tk.Entry(root, font=("Arial", 11), bd=0, highlightthickness=0, bg=BG_WHITE, fg=DARK_GREEN)
    entry.place(x=x+5, y=y+27, width=180, height=20)
    update_func = add_placeholder(entry, placeholder)

    # question mark
    circular_button(canvas, x+230, y+36, 13, "?", on_click_function)
    return entry, update_func


def create_double_text_input_unit(root, canvas, x, y, text, placeholder1, placeholder2, on_click_function):
    text = tk.Label(root, text=text, bg=LIGHT_GREEN, fg=TEXT_GREEN, font=("Arial", 10))
    text.place(x = x, y = y)

    round_rectangle(canvas, x, y+25, x+90, y+50, radius=15, fill=BG_WHITE, outline="")
    entry1 = tk.Entry(root, font=("Arial", 11), bd=0, highlightthickness=0, bg=BG_WHITE, fg=DARK_GREEN)
    entry1.place(x=x+5, y=y+27, width=80, height=20)
    update_func1 = add_placeholder(entry1, placeholder1)

    round_rectangle(canvas, x + 110, y+25, x+200, y+50, radius=15, fill=BG_WHITE, outline="")
    entry2 = tk.Entry(root, font=("Arial", 11), bd=0, highlightthickness=0, bg=BG_WHITE, fg=DARK_GREEN)
    entry2.place(x=x+115, y=y+27, width=80, height=20)
    update_func2 = add_placeholder(entry2, placeholder2)

    # question mark
    circular_button(canvas, x+230, y+36, 13, "?", on_click_function)
    return entry1, entry2, update_func1, update_func2


def create_slider(x, y):
    # do it without sliders first though
    # TODO: ball on a line slider
    pass


def check_value_consistency(all_entries, float_entries, int_entries):
    # calls some other functions
    if False in check_all_entries_numbers(float_entries, int_entries):
        print(check_all_entries_numbers(float_entries, int_entries))
        return False # we got some problems
    
    x_min, x_max, y_min, y_max = get_count_limits(float(all_entries[0].get()), float(all_entries[1].get()))
    if not (x_min <= int(all_entries[2].get()) <= x_max):
        return False # problems
    if not (y_min <= int(all_entries[3].get()) <= y_max):
        return False # shit hit fan

    if float(all_entries[5].get()) > get_max_bevel(all_entries[0], all_entries[1], all_entries[2], all_entries[3]):
        return False # this is not fine

    return True
    # also do something with the 11 and 12


def check_all_entries_numbers(float_entries, int_entries):
    # for each entry
    # takes entry, removes up to 1 ".", checks if rest of chars in 0...9
    floats = [entry.get().replace(".", "", 1).isnumeric() for entry in float_entries]
    ints = [entry.get().isnumeric() for entry in int_entries]
    return floats + ints #[entry.get().replace(".", "", 1).isnumeric() for entry in all_entries]
            

def get_count_limits(tot_size_x, tot_size_y):
    x_max = int(round(tot_size_x/MIN_PLATFORM_SIZE - 0.49999))
    y_max = int(round(tot_size_y/MIN_PLATFORM_SIZE - 0.49999))
    x_min = int(round(tot_size_x/MAX_PLATFORM_SIZE + 0.50000))
    y_min = int(round(tot_size_y/MAX_PLATFORM_SIZE + 0.50000))
    return x_min, x_max, y_min, y_max


def get_max_bevel(entry1, entry2, entry3, entry4):
    x_size = float(entry1.get()) / int(entry3.get())
    y_size = float(entry2.get()) / int(entry4.get())
    x_move_corners = (x_size - BASE_PLATFORM_SIZE) / 2
    y_move_corners = (y_size - BASE_PLATFORM_SIZE) / 2
    x_corner_loc = CORNER_BASE_LOC + x_move_corners
    y_corner_loc = CORNER_BASE_LOC + y_move_corners
    arm_loc_x = (2 * ARM_MIN_LOC + 1 * x_corner_loc) / 3
    arm_loc_y = (2 * ARM_MIN_LOC + 1 * y_corner_loc) / 3

    return min(x_corner_loc - arm_loc_x, y_corner_loc - arm_loc_y)
    #corner_loc - arm_loc 




def main():

    # background
    root = tk.Tk()
    root.geometry("1000x800")
    root.title("Window")
    root.configure(bg=BG_WHITE)

    canvas = tk.Canvas(root, width=1000, height=800)
    canvas.pack()

    # Boxes
    canvas.create_polygon(0, 0, 0, 800, 1000, 800, fill=BG_GREEN)

    param_box_shadow = round_rectangle(canvas, 60, 100, 360, 740, radius=20, fill=DARK_GREEN)
    param_box = round_rectangle(canvas, 100, 60, 400, 700, radius=20, fill=LIGHT_GREEN)

    info_box_shadow = round_rectangle(canvas, 460, 100, 910, 740, radius=20, fill=DARK_GREEN)
    info_box = round_rectangle(canvas, 500, 60, 950, 700, radius=20, fill=LIGHT_GREEN)

    def new_placeholder():
        update_func3("kissa")
        update_func4("kissa")

    def update_platform_count_placeholders():
        x_min, x_max, y_min, y_max = get_count_limits(float(entry1.get()), float(entry2.get()))
        print(x_min, x_max, y_min, y_max)
        update_func3(f"{x_min} - {x_max}")
        update_func4(f"{y_min} - {y_max}")
        root.focus()

    def click():
        root.focus()
        #print("Click")

    # Inputs and buttons
    entry1, entry2, update_func1, update_func2 = create_double_text_input_unit(root, canvas, 130, 90, "Container size", "x", "y", click)
    entry3, entry4, update_func3, update_func4 = create_double_text_input_unit(root, canvas, 130, 90 + 60, "Platform amount", "x", "y", update_platform_count_placeholders)

    entry5, update_func5 = create_text_input_unit(root, canvas, 130, 90 + 120, "Edge height (cm)", "", click)
    entry6, update_func6 = create_text_input_unit(root, canvas, 130, 90 + 180, "Bevel size (cm)", "", click)
    entry7, update_func7 = create_text_input_unit(root, canvas, 130, 90 + 240, "Bevel count", "", click)
    entry8, update_func8 = create_text_input_unit(root, canvas, 130, 90 + 300, "Connector edge lift (cm)", "", click)
    entry9, update_func9 = create_text_input_unit(root, canvas, 130, 90 + 360, "Margins (cm)", "", click)
    entry10, update_func10 = create_text_input_unit(root, canvas, 130, 90 + 420, "Model scale", "", click)

    entry11, entry12, update_func11, update_func12 = create_double_text_input_unit(root, canvas, 130, 90 + 480, "Print area dimensions", "x", "y", click)

    # make distinction between int and float entries?
    all_entries = [entry1, entry2, entry3, entry4, entry5, entry6, entry7, entry8, entry9, entry10, entry11, entry12]
    int_entries = [entry1, entry2, entry5, entry6, entry8, entry9, entry10, entry11, entry12]
    float_entries = [entry3, entry4, entry7]

    def generate_files():
        if not check_value_consistency(all_entries, float_entries, int_entries):
            print("the numbers not ok")
            return
        print("Success!")

    # the "submit" button
    rectangular_button(canvas, 150, 635, 350, 680, "Generate", generate_files, 20, fill=BG_GREEN)

    # TODO: The info box
    # TODO: Object oriented approach would probably be smart
    #       for the whole GUI project, but especially for the info box

    root.mainloop()
    return 0

if __name__ == "__main__":
    main()