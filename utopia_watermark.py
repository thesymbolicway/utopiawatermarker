import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import os

def get_fonts(folder):
    # List all files in the folder
    files = os.listdir(folder)
    # Filter out all files that are not TTF fonts
    fonts = [f for f in files if f.lower().endswith('.ttf')]
    return fonts

def choose_images():
    global image_paths
    image_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if image_paths:
        images = "\n".join(os.path.basename(path) for path in image_paths)
        image_label.config(text=f"Selected Images:\n{images}")


def add_watermark():
    watermark_text = watermark_text_entry.get()
    transparency = transparency_scale.get()
    position = position_var.get()
    selected_font = font_var.get()
    font_path = os.path.join(font_folder, selected_font)

    if image_paths and watermark_text:
        for image_path in image_paths:
            image = Image.open(image_path).convert("RGBA")
            font = ImageFont.truetype(font_path, 50)
            drawing = ImageDraw.Draw(image)
            
            # Use getbbox to get the bounding box of the text
            left, top, right, bottom = font.getbbox(watermark_text)
            text_width = right - left
            text_height = bottom - top

            width, height = image.size
            x = (width - text_width) / 2
            y = (height - text_height) / 2

            # Adjust the x, y coordinates based on the desired position
            if position == "Top-Left":
                x, y = 0, 0
            elif position == "Top-Right":
                x, y = width - text_width, 0
            elif position == "Bottom-Left":
                x, y = 0, height - text_height
            elif position == "Bottom-Right":
                x, y = width - text_width, height - text_height

            drawing.text((x, y), watermark_text, font=font, fill=(255, 255, 255, transparency))
            watermarked_image_path = f"watermarked_{os.path.basename(image_path)}"
            image.save(watermarked_image_path)

        status_label.config(text="Watermarks added successfully to all selected images!")

# Set up the GUI
root = tk.Tk()
root.title("Batch Watermarking Tool")

image_label = tk.Label(root, text="No Images Selected")
image_label.pack()

choose_images_button = tk.Button(root, text="Choose Images", command=choose_images)
choose_images_button.pack()

watermark_text_label = tk.Label(root, text="Enter watermark text:")
watermark_text_label.pack()

watermark_text_entry = tk.Entry(root)
watermark_text_entry.pack()

transparency_label = tk.Label(root, text="Watermark Transparency:")
transparency_label.pack()

transparency_scale = tk.Scale(root, from_=0, to_=255, orient='horizontal')
transparency_scale.set(128)  # Default transparency
transparency_scale.pack()

position_label = tk.Label(root, text="Watermark Position:")
position_label.pack()

position_var = tk.StringVar(root)
position_var.set("Bottom-Right")  # default value
position_options = ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"]
position_menu = tk.OptionMenu(root, position_var, *position_options)
position_menu.pack()

# Font selection dropdown
font_folder = "/System/Library/Fonts/Supplemental/"
font_list = get_fonts(font_folder)
font_var = tk.StringVar(root)
font_var.set(font_list[0])  # set the default value
font_dropdown_label = tk.Label(root, text="Select Font:")
font_dropdown_label.pack()
font_dropdown = tk.OptionMenu(root, font_var, *font_list)
font_dropdown.pack()

add_watermark_button = tk.Button(root, text="Apply Watermark to All", command=add_watermark)
add_watermark_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
