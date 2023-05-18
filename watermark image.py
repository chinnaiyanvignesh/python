from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
import tkinter.font as tkfont

def get_font_styles():
    font_families = tkfont.families()
    return sorted(font_families)

def get_font_sizes():
    return [str(i) for i in range(8, 101)]

def watermark_image(image_path, watermark_text, position, color, font_path, font_size, border_style, border_width, spacing):
    # Load the original image
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    # Create a transparent image for the watermark
    watermark = Image.new("RGBA", image.size, (0, 0, 0, 0))

    # Create a drawing context for the watermark
    draw = ImageDraw.Draw(watermark)

    # Define the font and size
    font = ImageFont.truetype(font_path, font_size)

    # Determine the position of the watermark based on user input
    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    x_position, y_position = get_position_coordinates(position, width, height, text_bbox)

    # Add the border to the text
    border_text_bbox = (text_bbox[0] - border_width - spacing, text_bbox[1] - border_width - spacing,
                        text_bbox[2] + border_width + spacing, text_bbox[3] + border_width + spacing)
    draw.rectangle(border_text_bbox, outline=color, width=border_width)

    # Add the text to the watermark
    draw.text((x_position, y_position), watermark_text, font=font, fill=color)

    # Combine the original image with the watermark
    watermarked_image = Image.alpha_composite(image, watermark)

    # Save the watermarked image
    output_path = os.path.splitext(image_path)[0] + "_watermarked.png"
    watermarked_image.save(output_path)

    return output_path

def get_position_coordinates(position, width, height, text_bbox):
    space = 25  # Space from page edge
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    if position == "Top Left":
        x_position = space
        y_position = space
    elif position == "Top Right":
        x_position = width - text_width - space
        y_position = space
    elif position == "Bottom Left":
        x_position = space
        y_position = height - text_height - space
    elif position == "Bottom Right":
        x_position = width - text_width - space
        y_position = height - text_height - space
    elif position == "Center":
        x_position = (width - text_width) // 2
        y_position = (height - text_height) // 2
    elif position == "Center Right":
        x_position = width - text_width - space
        y_position = (height - text_height) // 2
    elif position == "Center Left":
        x_position = space
        y_position = (height - text_height) // 2
    return x_position, y_position

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg"), ("All files", "*.*")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)

def choose_color():
    color = colorchooser.askcolor(title="Choose Watermark Color")
    if color[1] is not None:
        color_value_label.config(bg=color[1])
        color_value_label.color = color[1]
        color_value_label.update()

def watermark_image_gui():
    image_path = input_file_entry.get()
    watermark_text = watermark_text_entry.get()
    position = position_combobox.get()
    color = color_value_label.color
    font_path = font_path_combobox.get()
    font_size = int(font_size_combobox.get())
    border_style = border_style_combobox.get()
    border_width = int(border_width_combobox.get())
    spacing = int(spacing_combobox.get())

    if not os.path.isfile(image_path):
        messagebox.showerror("Error", "Please choose a valid input file.")
        return

    try:
        output_path = watermark_image(image_path, watermark_text, position, color, font_path, font_size,
                                      border_style, border_width, spacing)
        messagebox.showinfo("Success", f"Watermarked image saved as {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

root = tk.Tk()
root.title("Image Watermarking")
root.geometry("400x500")

# Input file
input_file_label = tk.Label(root, text="Input File:")
input_file_label.pack()
input_file_entry = tk.Entry(root, width=40)
input_file_entry.pack(side=tk.LEFT)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(side=tk.LEFT)

# Watermark text
watermark_text_label = tk.Label(root, text="Watermark Text:")
watermark_text_label.pack()
watermark_text_entry = tk.Entry(root, width=40)
watermark_text_entry.pack()

# Watermark position
position_label = tk.Label(root, text="Watermark Position:")
position_label.pack()
position_combobox = ttk.Combobox(root, values=["Top Left", "Top Right", "Bottom Left", "Bottom Right", "Center", "Center Right", "Center Left"])
position_combobox.pack()

# Watermark color
color_label = tk.Label(root, text="Watermark Color:")
color_label.pack()
color_frame = tk.Frame(root)
color_frame.pack()
color_value_label = tk.Label(color_frame, width=10, relief=tk.RAISED)
color_value_label.pack(side=tk.LEFT)
color_value_label.color = "black"  # Initial color (black)
choose_color_button = tk.Button(color_frame, text="Choose", command=choose_color)
choose_color_button.pack(side=tk.LEFT)

# Font details
font_path_label = tk.Label(root, text="Font Style:")
font_path_label.pack()
font_path_combobox = ttk.Combobox(root, values=get_font_styles())
font_path_combobox.pack()

font_size_label = tk.Label(root, text="Font Size:")
font_size_label.pack()
font_size_combobox = ttk.Combobox(root, values=get_font_sizes())
font_size_combobox.pack()

# Border style
border_style_label = tk.Label(root, text="Border Style:")
border_style_label.pack()
border_style_combobox = ttk.Combobox(root, values=["Solid", "Dashed", "Dotted"])
border_style_combobox.pack()

# Border width
border_width_label = tk.Label(root, text="Border Width:")
border_width_label.pack()
border_width_combobox = ttk.Combobox(root, values=[str(i) for i in range(1, 11)])
border_width_combobox.pack()

# Spacing
spacing_label = tk.Label(root, text="Spacing:")
spacing_label.pack()
spacing_combobox = ttk.Combobox(root, values=[str(i) for i in range(0, 51)])
spacing_combobox.pack()

# Watermark button
watermark_button = tk.Button(root, text="Watermark Image", command=watermark_image_gui)
watermark_button.pack(pady=10)

root.mainloop()
