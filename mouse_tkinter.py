import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk

# Create a tkinter window
root = tk.Tk()
root.title("Tkinter Canvas Example")

# Create a tkinter canvas
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Initialize global variables
points = []
mouse_path = []
drawing = False

# Load your image (replace 'image.jpg' with your image file)
image = cv2.imread("C:/Users/ASUS/Desktop/Janith/Janith/Y3S1/CS314/tkinter/Picture1.jpg")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_pil = Image.fromarray(image_rgb)
image_tk = ImageTk.PhotoImage(image_pil)

def cv2_to_tkinter_photo(cv2_image):
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    return ImageTk.PhotoImage(pil_image)

selected_region_photo = None

def mouse_callback(event):
    global points, mouse_path, drawing, selected_region_photo

    x, y = event.x, event.y

    if event == "<Button-1>":
        drawing = True
        points.append((x, y))
        mouse_path.append((x, y))

    elif event == "<ButtonRelease-1>":
        drawing = False

    elif event == "<Motion>" and drawing:
        points.append((x, y))
        mouse_path.append((x, y))

    elif event == "<Button-3>":
        drawing = False
        # Create a mask with the selected region
        mask = np.zeros((400, 400), dtype=np.uint8)
        point_array = np.array(points, dtype=np.int32)
        cv2.fillPoly(mask, [point_array], 255)

        # Apply the mask to the original image
        selected_region = cv2.bitwise_and(image, image, mask=mask)

        # Display the selected region on the canvas
        selected_region_photo = cv2_to_tkinter_photo(selected_region)
        canvas.create_image(0, 0, anchor=tk.NW, image=selected_region_photo)

        # Save the selected region to a file
        cv2.imwrite('test.jpg', selected_region)

        # Clear points and mouse path
        points = []
        mouse_path = []

# Bind mouse events to the canvas
canvas.bind("<Button-1>", mouse_callback)
canvas.bind("<ButtonRelease-1>", mouse_callback)
canvas.bind("<Button-3>", mouse_callback)
canvas.bind("<Motion>", mouse_callback)

# Display the original image on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

root.mainloop()
