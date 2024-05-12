import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog

# Global variables for image and selection
image = None
image_rgb = None
image_with_path = None
points = []
mouse_path = []

def mouse_callback(event, x, y, flags, param):
    global points, mouse_path, image_with_path

    # Mouse movement (left button held down)
    if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        points.append((x, y))
        mouse_path.append((x, y))

    # Mouse button released (right button)
    elif event == cv2.EVENT_RBUTTONUP:
        # Create a mask with the selected region
        mask = np.zeros_like(image)
        cv2.fillPoly(mask, [np.array(points)], (255, 255, 255))

        # Apply the mask to the original image
        selected_region = cv2.bitwise_and(image, mask)

        # Convert selected region to RGB format for display
        selected_region_rgb = cv2.cvtColor(selected_region, cv2.COLOR_BGR2RGB)

        # Update the canvas with the selected region
        img = Image.fromarray(selected_region_rgb)
        img_tk = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.img_tk = img_tk  # Keep reference to avoid garbage collection

    # Mouse button released (left button)
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_path = []  # Clear mouse path

def open_image():
    global image, image_rgb, image_with_path

    file_path = filedialog.askopenfilename(
        initialdir="C:/Users/ASUS/Pictures/Camera Roll")
    image = cv2.imread(file_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    canvas.delete("all")  # Clear the canvas
    img = Image.fromarray(image_rgb)
    img_tk = ImageTk.PhotoImage(image=img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.img_tk = img_tk  # Keep reference to avoid garbage collection

def clear_selection():
    global points, mouse_path
    points = []
    mouse_path = []
    canvas.delete("all")  # Clear the canvas
    img = Image.fromarray(image_rgb)
    img_tk = ImageTk.PhotoImage(image=img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.img_tk = img_tk  # Keep reference to avoid garbage collection

root = tk.Tk()
root.title("Region Selection")

frame = ttk.Frame(root)
frame.pack(side=tk.LEFT, padx=10, pady=10)

canvas = tk.Canvas(frame, width=800, height=600)
canvas.pack()

open_button = ttk.Button(frame, text="Open Image", command=open_image)
open_button.pack(pady=5)

clear_button = ttk.Button(frame, text="Clear Selection", command=clear_selection)
clear_button.pack(pady=5)

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouse_callback)

root.mainloop()
