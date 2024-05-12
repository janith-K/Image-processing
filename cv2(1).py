import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

# Create a Tkinter window
root = tk.Tk()
root.title("Image Viewer")

# Create a canvas to display the image
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

# Define the function to add and process an image
def add_img():
    global file_path
    file_path = filedialog.askopenfilename(initialdir="C:/Users/ASUS/Pictures/Camera Roll")
    original_image = Image.open(file_path)
    
    # Apply a grayscale conversion using OpenCV
    opencv_image = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2GRAY)
    
    width, height = int(original_image.width / 2), int(original_image.height / 2)
    resized_image = original_image.resize((width, height), Image.ANTIALIAS)
    
    canvas.config(width=resized_image.width, height=resized_image.height)
    
    # Convert the processed OpenCV image to a format suitable for Tkinter
    image = ImageTk.PhotoImage(Image.fromarray(opencv_image))
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

# Create a button to trigger the image selection and processing
add_img_button = tk.Button(root, text="Add Image", command=add_img)
add_img_button.pack()

# Run the Tkinter main loop
root.mainloop()
