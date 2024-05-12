import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk

# Variables to store the coordinates of the region and mouse path
points = []
mouse_path = []

def mouse_callback(event, x, y, flags, param):
    global points, mouse_path

    # Mouse movement (left button held down)
    if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        points.append((x, y))
        mouse_path.append((x, y))

    # Mouse button released (right button)
    elif event == cv2.EVENT_RBUTTONUP:
        # Create a mask with the selected region
        mask = np.zeros_like(image_gray)
        cv2.fillPoly(mask, [np.array(points)], (255, 255, 255))

        # Apply the mask to the original image
        selected_region = cv2.bitwise_and(image, image, mask=mask)

        # Display the selected region
        cv2.imshow("Selected Region", selected_region)

    # Mouse button released (left button)
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_path = []  # Clear mouse path

# Create a Tkinter window
root = tk.Tk()
root.title("OpenCV in Tkinter")

# Load the image
image = cv2.imread("C:/Users/ASUS/Desktop/Janith/Janith/Y3S1/CS314/tkinter/Picture1.jpg")
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Create a window and bind the mouse callback function to it
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouse_callback)

# Create a label to display the OpenCV image
label = tk.Label(root)
label.pack()

while True:
    # Clone the image to draw the mouse path
    image_with_path = image.copy()

    # Draw the mouse path on the cloned image
    for i in range(1, len(mouse_path)):
        cv2.line(image_with_path, mouse_path[i - 1], mouse_path[i], (0, 0, 255), 2)

    # Convert the OpenCV image to a format that Tkinter can display
    image_rgb = cv2.cvtColor(image_with_path, cv2.COLOR_BGR2RGB)
    image_tk = ImageTk.PhotoImage(Image.fromarray(image_rgb))

    # Update the label with the new image
    label.config(image=image_tk)
    label.image = image_tk

    # Break the loop if the 'Esc' key is pressed
    if cv2.waitKey(1) == 27:
        break

# Destroy the OpenCV window and close Tkinter
cv2.destroyAllWindows()
root.destroy()
