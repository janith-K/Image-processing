import tkinter as tk
import numpy as np
import cv2

image = cv2.imread("C:/Users/ASUS/Pictures/Camera Roll/cameraman.tif")
# Initialize tkinter
root = tk.Tk()
root.title("Tkinter Canvas Example")

# Create a canvas widget
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Initialize global variables
points = []
mouse_path = []

def mouse_callback(event):
    global points, mouse_path

    # Mouse movement (left button held down)
    if event.type == tk.EventType.ButtonPress and event.num == 1:
        x, y = event.x, event.y
        points.append((x, y))
        mouse_path.append((x, y))

    # Mouse button released (right button)
    elif event.type == tk.EventType.ButtonRelease and event.num == 3:
        # Create a mask with the selected region
        mask = np.zeros((400, 400), dtype=np.uint8)
        point_array = np.array(points, dtype=np.int32)
        cv2.fillPoly(mask, [point_array], 255)

        # Apply the mask to the original image (replace 'image' with your image)
        selected_region = cv2.bitwise_and(image, image, mask=mask)

        # Display the selected region (replace 'cv2.imshow' with your tkinter canvas drawing code)
        # For example, you can draw the selected region on the canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=selected_region)

    # Mouse button released (left button)
    elif event.type == tk.EventType.ButtonRelease and event.num == 1:
        mouse_path = []  # Clear mouse path

# Bind mouse events to the canvas
canvas.bind("<Button-1>", mouse_callback)
canvas.bind("<Button-3>", mouse_callback)

root.mainloop()
