import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

def save_canvas_image(canvas, file_path):
    # Get the dimensions of the canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Create a PIL image with the same dimensions as the canvas
    image = Image.new("RGB", (canvas_width, canvas_height), "white")

    # Create a draw object to draw on the image
    draw = ImageDraw.Draw(image)

    # Capture the contents of the canvas and paste it onto the PIL image
    canvas_image = ImageTk.PhotoImage(canvas.create_image(0, 0, anchor=tk.NW, image=image))
    
    # Save the PIL image to the specified file path
    image.save(file_path)

    # Clean up the canvas
    canvas.delete(canvas_image)

# Example usage:
root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

# Load an image onto the canvas (you can replace this with your image loading logic)
image = Image.open("C:/Users/ASUS/Desktop/Janith/Janith/Y3S1/CS314/Lesson 4/messi.jpg")
photo = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Function to save the canvas contents as an image
def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        save_canvas_image(canvas, file_path)

save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack()

root.mainloop()
