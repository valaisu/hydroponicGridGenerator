import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# TODO: make this file importable

LIGHT_GREEN = "#91CF99"
DARK_GREEN = "#517A52"
TEXT_GREEN = "#2A2C2A"
BG_WHITE = "#D9D9D9"
BG_GREEN = "#7EC27F"


def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
        
    points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, 
              x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, 
              x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, 
              x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)


def circular_button(x, y, radius, text, command):

    circle = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=BG_WHITE, outline="")
    label = canvas.create_text(x, y, text=text, font=("Arial", 11), fill=TEXT_GREEN)
    
    def on_click(event):
        command()
    
    canvas.tag_bind(circle, "<Button-1>", on_click)
    canvas.tag_bind(label, "<Button-1>", on_click)


def rectangular_button(x1, y1, x2, y2, text, command, radius=0, **kwargs):

    rect = round_rectangle(x1, y1, x2, y2, radius=radius, **kwargs)
    
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    
    label = canvas.create_text(center_x, center_y, text=text, font=("Arial", 14), fill=TEXT_GREEN)

    def on_click(event):
        command()

    canvas.tag_bind(rect, "<Button-1>", on_click)
    canvas.tag_bind(label, "<Button-1>", on_click)


def click():
    print("Click")


def add_placeholder(entry, placeholder_text):
    # Set the placeholder initially
    entry.insert(0, placeholder_text)
    entry.config(fg="grey") 

    # remove when clicked
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg="black")  # is this the color hmm

    # add back if empty
    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg="grey")

    # Bind focus in and focus out events to the Entry widget
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def create_text_input_unit(x, y, text, placeholder, on_click_function):
    text = tk.Label(root, text=text, bg=LIGHT_GREEN, fg=TEXT_GREEN, font=("Arial", 10))
    text.place(x = x, y = y)

    # button background
    round_rectangle(x, y+25, x+200, y+50, radius=15, fill=BG_WHITE, outline="")
    # button input
    entry = tk.Entry(root, font=("Arial", 11), bd=0, highlightthickness=0, bg=BG_WHITE, fg=DARK_GREEN)
    entry.place(x=x+5, y=y+27, width=180, height=20)
    add_placeholder(entry, placeholder)

    # question mark
    circular_button(x+230, y+36, 13, "?", on_click_function)


def create_double_text_input_unit(x, y, text, placeholder1, placeholder2, on_click_function):
    text = tk.Label(root, text=text, bg=LIGHT_GREEN, fg=TEXT_GREEN, font=("Arial", 10))
    text.place(x = x, y = y)

    round_rectangle(x, y+25, x+90, y+50, radius=15, fill=BG_WHITE, outline="")
    entry1 = tk.Entry(root, font=("Arial", 11), bd=0, highlightthickness=0, bg=BG_WHITE, fg=DARK_GREEN)
    entry1.place(x=x+5, y=y+27, width=80, height=20)
    add_placeholder(entry1, placeholder1)

    round_rectangle(x + 110, y+25, x+200, y+50, radius=15, fill=BG_WHITE, outline="")
    entry2 = tk.Entry(root, font=("Arial", 11), bd=0, highlightthickness=0, bg=BG_WHITE, fg=DARK_GREEN)
    entry2.place(x=x+115, y=y+27, width=80, height=20)
    add_placeholder(entry2, placeholder2)

    # question mark
    circular_button(x+230, y+36, 13, "?", on_click_function)


def create_slider(x, y):
    # do it without sliders first though
    # TODO: ball on a line slider
    pass


# background
root = tk.Tk()
root.geometry("1000x800")
root.title("Window")
root.configure(bg=BG_WHITE)

canvas = tk.Canvas(root, width=1000, height=800)
canvas.pack()

# Boxes
canvas.create_polygon(0, 0, 0, 800, 1000, 800, fill=BG_GREEN)

param_box_shadow = round_rectangle(60, 100, 360, 740, radius=20, fill=DARK_GREEN)
param_box = round_rectangle(100, 60, 400, 700, radius=20, fill=LIGHT_GREEN)

info_box_shadow = round_rectangle(460, 100, 910, 740, radius=20, fill=DARK_GREEN)
info_box = round_rectangle(500, 60, 950, 700, radius=20, fill=LIGHT_GREEN)

# Inputs and buttons
create_double_text_input_unit(130, 90, "Bevel size", "x", "y", click)
create_double_text_input_unit(130, 90 + 60, "Bevel size", "x", "y", click)

create_text_input_unit(130, 90 + 120, "Edge height (cm)", "", click)
create_text_input_unit(130, 90 + 180, "Bevel size (cm)", "", click)
create_text_input_unit(130, 90 + 240, "Bevel count", "", click)
create_text_input_unit(130, 90 + 300, "Connector edge lift (cm)", "", click)
create_text_input_unit(130, 90 + 360, "Margins (cm)", "", click)
create_text_input_unit(130, 90 + 420, "Model scale", "", click)

create_double_text_input_unit(130, 90 + 480, "Bevel size", "x", "y", click)

# the "submit" button
rectangular_button(150, 635, 350, 680, "Generate", click, 20, fill=BG_GREEN)

# TODO: The info box



root.mainloop()
