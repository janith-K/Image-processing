import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw

def save_image():
    # Create a blank image
    image = Image.new("RGB", (300, 300), "white")

    # Draw something on the image (you can replace this with your image creation logic)
    draw = ImageDraw.Draw(image)
    draw.text((100, 100), "Hello, Image!", fill="black")

    # Open a file dialog to choose the save location
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    # Save the image to the chosen location
    if file_path:
        image.save(file_path)
        print(f"Image saved to {file_path}")

# Create the main window
root = tk.Tk()
root.title("Image Save Example")

# Create a button to trigger image saving
save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
