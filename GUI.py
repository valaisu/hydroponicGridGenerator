import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

from constants import *
from stl_generation_logic import generate

from combine_stl_files import *


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
        event.widget.config(fg="black") # color back to black
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
        if not entry.get().isnumeric() or entry.cget("fg") == "red": # if a number, dont override, else:
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
        all = check_all_entries_numbers(float_entries, int_entries)
        print(all)
        return False # we got some problems
    
    x_min, x_max, y_min, y_max = get_count_limits(float(all_entries[0].get()), float(all_entries[1].get()))
    if not (x_min <= int(all_entries[2].get()) <= x_max):
        all_entries[2].config(fg="red")
        return False # problems
    if not (y_min <= int(all_entries[3].get()) <= y_max):
        all_entries[3].config(fg="red")
        return False # shit hit fan

    if float(all_entries[5].get()) > get_max_bevel(all_entries[0], all_entries[1], all_entries[2], all_entries[3]):
        all_entries[5].config(fg="red")
        return False # this is not fine

    return True
    # also do something with the 11 and 12


def check_all_entries_numbers(float_entries, int_entries):
    # for each entry
    # takes entry, removes up to 1 ".", checks if rest of chars in 0...9
    floats = [entry.get().replace(".", "", 1).isnumeric() for entry in float_entries]
    ints = [entry.get().isnumeric() for entry in int_entries]

    #print([entry.get().isnumeric() for entry in float_entries])

    
    # highlight with red color
    for i, entry in enumerate(floats):
        if not entry:
            float_entries[i].config(fg="red")
    for i, entry in enumerate(ints):
        if not entry:
            int_entries[i].config(fg="red")
    
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

def round_corners(image, radius, background_color):

    rounded_image = Image.new("RGBA", image.size, background_color)
    
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + image.size, radius=radius, fill=255)
    
    rounded_image.paste(image, (0, 0), mask=mask)
    return rounded_image

def hex_to_rgba(hex_color, alpha=255):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (alpha,)


def main():

    # background
    root = tk.Tk()
    root.geometry("1000x800")
    root.title("Window")
    root.configure(bg=BG_WHITE)

    canvas = tk.Canvas(root, width=1000, height=800)
    canvas.pack()

    # info box
    image_label = tk.Label(root, borderwidth=0)
    info_box_title = tk.Label(root, text="Print file generator", bg=LIGHT_GREEN, fg=TEXT_GREEN, font=("Arial", 20))
    info_box_title.place(x=600, y=80)

    info_box_text = tk.Text(root, height=15, width=50, bd=0, highlightthickness=0, bg=LIGHT_GREEN, fg=TEXT_GREEN, wrap=tk.WORD)
    info_box_text.place(x=520, y=440)
    info_box_text.insert(tk.END, generic_info[0])

    # Boxes
    canvas.create_polygon(0, 0, 0, 800, 1000, 800, fill=BG_GREEN)

    param_box_shadow = round_rectangle(canvas, 60, 100, 360, 740, radius=20, fill=DARK_GREEN)
    param_box = round_rectangle(canvas, 100, 60, 400, 700, radius=20, fill=LIGHT_GREEN)

    info_box_shadow = round_rectangle(canvas, 460, 100, 910, 740, radius=20, fill=DARK_GREEN)
    info_box = round_rectangle(canvas, 500, 60, 950, 700, radius=20, fill=LIGHT_GREEN)

    def click(img_path = "", title_text = "", paragraph_text = ""):
        if img_path != "":
            update_image(img_path)
        if title_text != "":
            update_label(info_box_title, title_text)
        if paragraph_text != "":
            update_text(info_box_text, paragraph_text)
        root.focus()
    
    def update_label(text_field, text_contents):
        text_field.config(text = text_contents)
    
    def update_text(text_box, new_text):
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, new_text)

    def update_platform_count_placeholders(img_path = "", title_text = "", paragraph_text = ""):
        click(img_path, title_text, paragraph_text)
        x_min, x_max, y_min, y_max = get_count_limits(float(entry1.get()), float(entry2.get()))
        update_func3(f"{x_min} - {x_max}")
        update_func4(f"{y_min} - {y_max}")
        root.focus()

    def update_bevel_size_placeholders(img_path = "", title_text = "", paragraph_text = ""):
        click(img_path, title_text, paragraph_text)
        max_bevel = get_max_bevel(entry1, entry2, entry3, entry4)
        update_func6(f"{0} - {max_bevel:.2f}")
        root.focus()
    
    def update_image(path):
        image = Image.open(path)
        image = image.resize((400, 296)) 
        image = round_corners(image, 30, hex_to_rgba(LIGHT_GREEN))
        tk_image = ImageTk.PhotoImage(image)
        image_label.config(image=tk_image)
        image_label.image = tk_image
        image_label.place(x=525, y=130)

    # Inputs and buttons
    entry1, entry2, update_func1, update_func2 = create_double_text_input_unit(root, canvas, 130, 90, "Container size", "x", "y", lambda: click(IMAGE_PATHS[2], titles[0], paragraphs[0]))
    entry3, entry4, update_func3, update_func4 = create_double_text_input_unit(root, canvas, 130, 90 + 60, "Platform amount", "x", "y", lambda: update_platform_count_placeholders(IMAGE_PATHS[0], titles[1], paragraphs[1]))

    entry5, update_func5 = create_text_input_unit(root, canvas, 130, 90 + 120, "Edge height (cm)", "", lambda: click(IMAGE_PATHS[6], titles[2], paragraphs[2]))
    entry6, update_func6 = create_text_input_unit(root, canvas, 130, 90 + 180, "Bevel size (cm)", "", lambda: update_bevel_size_placeholders(IMAGE_PATHS[3], titles[3], paragraphs[3]))
    entry7, update_func7 = create_text_input_unit(root, canvas, 130, 90 + 240, "Bevel count", "", lambda: click(IMAGE_PATHS[4], titles[4], paragraphs[4]))
    entry8, update_func8 = create_text_input_unit(root, canvas, 130, 90 + 300, "Connector edge lift (cm)", "", lambda: click(IMAGE_PATHS[1], titles[5], paragraphs[5]))
    entry9, update_func9 = create_text_input_unit(root, canvas, 130, 90 + 360, "Margins (cm)", "", lambda: click(IMAGE_PATHS[7], titles[6], paragraphs[6]))
    entry10, update_func10 = create_text_input_unit(root, canvas, 130, 90 + 420, "Model scale", "", lambda: click(IMAGE_PATHS[8], titles[7], paragraphs[7])) # TODO: some image needed for this too

    entry11, entry12, update_func11, update_func12 = create_double_text_input_unit(root, canvas, 130, 90 + 480, "Print area dimensions", "x", "y", lambda: click(IMAGE_PATHS[8], titles[8], paragraphs[8]))

    # My suggested values
    entry5.insert(0, 2)
    entry7.insert(0, 2)
    entry9.insert(0, 0.001)
    entry10.insert(0, 10)

    # make distinction between int and float entries?
    all_entries = [entry1, entry2, entry3, entry4, entry5, entry6, entry7, entry8, entry9, entry10, entry11, entry12]
    float_entries = [entry1, entry2, entry5, entry7, entry8, entry9, entry10, entry11, entry12]
    int_entries = [entry3, entry4, entry7]

    def generate_files():
        if not check_value_consistency(all_entries, float_entries, int_entries):
            print("the numbers not ok")
            return
        x_size = float(entry1.get()) / int(entry3.get())
        y_size = float(entry2.get()) / int(entry4.get())
        generate(x_size, y_size, 
                 float(entry5.get()), 
                 float(entry6.get()), 
                 int(entry7.get()), 
                 float(entry9.get()), 
                 int(entry3.get()), 
                 int(entry4.get()), 
                 float(entry8.get()), 
                 float(entry10.get()))
        
        arrange(float(entry11.get()), float(entry12.get()), INDIVIDUAL_STL_FOLDER, COMBINED_STL_FOLDER, float(entry10.get()))
        print("Success!")

    # the "submit" button
    rectangular_button(canvas, 150, 635, 350, 680, "Generate", generate_files, 20, fill=BG_GREEN)
    # the base image
    update_image(IMAGE_PATHS[5])

    root.mainloop()
    return 0

if __name__ == "__main__":
    main()


#TODO: add home button
#TODO: add "generated!" indicator