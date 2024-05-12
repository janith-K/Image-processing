import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser
from PIL import Image, ImageOps, ImageTk, ImageFilter,ImageDraw,ImageGrab
import cv2
import numpy as np




pen_color = "black"
pen_size = 5
file_path = ""
points = []
mouse_path = []
def mouse_event():
    points = []
    mouse_path = []

    def mouse_callback(event, x, y, flags, param):
        nonlocal points, mouse_path
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
            selected_region_gray = cv2.cvtColor(selected_region, cv2.COLOR_BGR2GRAY)

            # Convert the grayscale image to RGB format
            pil_image = Image.fromarray(cv2.cvtColor(selected_region_gray, cv2.COLOR_GRAY2RGB))
            pil_image = pil_image.resize((700, 600), Image.ANTIALIAS)

            photo = ImageTk.PhotoImage(pil_image)

            canvas.image = photo
            canvas.create_image(0, 0, image=photo, anchor="nw")

        # Mouse button released (left button)
        elif event == cv2.EVENT_LBUTTONUP:
            mouse_path = []  # Clear mouse path

    image = cv2.imread(file_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", mouse_callback)

    # Display the image
    cv2.imshow("Image", image)

    while True:
        # Clone the image to draw the mouse path
        image_with_path = image.copy()

        # Draw the mouse path on the cloned image
        for i in range(1, len(mouse_path)):
            cv2.line(image_with_path, mouse_path[i - 1], mouse_path[i], (0, 0, 255), 2)

        # Show the image with the mouse path
        cv2.imshow("Image", image_with_path)

        # Break the loop if the 'Esc' key is pressed
        if cv2.waitKey(1) == 27:
            break

    # Destroy all windows
    cv2.destroyAllWindows()

def mouse_brush():
    
    points = []
    mouse_path = []

    def mouse_callback(event, x, y, flags, param):
        nonlocal points, mouse_path
        # Mouse movement (left button held down)
        if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            points.append((x, y))
            mouse_path.append((x, y))

        # Mouse button released (right button)
        elif event == cv2.EVENT_RBUTTONUP:
            # Create a mask with the same size as the image
            mask = np.zeros_like(image)

            
            cv2.fillPoly(mask, [np.array(points)], (255, 255, 255))

            
            selected_region = cv2.bitwise_and(image,mask)
            
            selected_region = cv2.GaussianBlur(selected_region, (25, 25), 0)
            
            inverted_mask = cv2.bitwise_not(mask)
            outside_roi = cv2.bitwise_and(image,inverted_mask)
            result = cv2.add(selected_region, outside_roi)

            # Display the result
            cv2.imshow("Result", result)


            # Convert the selected region to grayscale
            selected_region_gray = result
            # Convert the grayscale image to RGB format
            pil_image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
            pil_image = pil_image.resize((700, 600), Image.ANTIALIAS)

            photo = ImageTk.PhotoImage(pil_image)

            canvas.image = photo
            canvas.create_image(0, 0, image=photo, anchor="nw")

        # Mouse button released (left button)
        elif event == cv2.EVENT_LBUTTONUP:
            mouse_path = []  # Clear mouse path

    image = cv2.imread(file_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", mouse_callback)

    # Display the image
    cv2.imshow("Image", image)

    while True:
        # Clone the image to draw the mouse path
        image_with_path = image.copy()

        # Draw the mouse path on the cloned image
        for i in range(1, len(mouse_path)):
            cv2.line(image_with_path, mouse_path[i - 1], mouse_path[i], (0, 0, 255), 2)

        # Show the image with the mouse path
        cv2.imshow("Image", image_with_path)

        # Break the loop if the 'Esc' key is pressed
        if cv2.waitKey(1) == 27:
            break

    # Destroy all windows
    cv2.destroyAllWindows()


def add_img():
    global file_path
    file_path = filedialog.askopenfilename(
        initialdir="C:/Users/ASUS/Pictures/Camera Roll")
    image = Image.open(file_path)
    image = image.resize((700, 600), Image.ANTIALIAS)
    canvas.config(width=image.width,height=image.height)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0,0,image = image,anchor = "nw")

def draw(event):
    x1,y1 = (event.x - pen_size), (event.y - pen_size)
    x2,y2 = (event.x + pen_size), (event.y + pen_size)
    canvas.create_oval(x1,y1,x2,y2,fill=pen_color,outline='')

def change_clr():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

def change_size(size):
    global pen_size
    pen_size = size

def clear_canvas():
    canvas.delete("all")
    canvas.create_image(0,0,image=canvas.image,anchor ="nw")



def apply_filter(filter):
    x = canvas.winfo_rootx()+150
    y = canvas.winfo_rooty()+50
    x1 = x + 800
    y1 = y + 700
    image = ImageGrab.grab(bbox=(x, y, x1, y1))
    image_resize = image.resize((700, 600), Image.ANTIALIAS)
    image_np_arr = np.array(image_resize)

    
    image_cv2 = cv2.cvtColor(image_np_arr, cv2.COLOR_RGB2BGR)

    if filter == "Black and White":
        opencv_image = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
        return_img = opencv_image
    elif filter == "Threshold":
        opencv_image = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
        ret,return_img = cv2.threshold(opencv_image,125,255,cv2.THRESH_BINARY)
    elif filter == "Blur":
        opencv_image = cv2.cvtColor(image_cv2,cv2.COLOR_BGR2RGB)
        blur = cv2.GaussianBlur(opencv_image, (25, 25), 0)
        return_img = blur
    elif filter == "Inverse":
        opencv_image = cv2.cvtColor(image_cv2,cv2.COLOR_BGR2RGB)
        return_img = cv2.bitwise_not(opencv_image)
    elif filter == "Enhance grayscale image":
        opencv_image = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
        equalise_hist = cv2.equalizeHist(opencv_image)
        return_img = equalise_hist
    elif filter == "Enhance color Image":
        opencv_image = cv2.cvtColor(image_cv2,1)
        H,S,V = cv2.split(cv2.cvtColor(opencv_image,cv2.COLOR_BGR2HSV))
        eq_v = cv2.equalizeHist(V)
        eq_image = cv2.cvtColor(cv2.merge([H,S,eq_v]),cv2.COLOR_HSV2RGB)
        return_img = eq_image
    elif filter == "Edge detection":
        opencv_image = cv2.cvtColor(image_cv2,1)
        laplacian = cv2.Laplacian(opencv_image,cv2.CV_8U,ksize=5)
        return_img = laplacian
    elif filter == "Draw Contours":
        opencv_image = image_cv2
        img_g = cv2.cvtColor(opencv_image,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(img_g,50,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        img_1 = cv2.drawContours(opencv_image,contours,-1,(0,255,0),2)
        return_img = img_1
    elif filter == "Count objects":
        img = image_cv2
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        kernel = np.ones((3,3), np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=1)

        sure_bg = cv2.dilate(opening,kernel,iterations=5)

        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,3)
        ret, sure_fg = cv2.threshold(dist_transform,0.1*dist_transform.max(),255,0)
        sure_fg = np.uint8(sure_fg)

        unknown = np.subtract(sure_bg,sure_fg)

        ret, markers = cv2.connectedComponents(sure_fg)

        markers = markers+1
        markers[unknown ==255] = 0
        markers = cv2.watershed(img,markers)

        img[markers == -1] = (255,0,0)
        return_img = img

        for label in np.unique(markers):
            total_area = np.sum(markers == label)

        print("Total number of items :",len(np.unique(markers)))

    pil_image = Image.fromarray(return_img)
    pil_image = pil_image.resize((700, 600), Image.ANTIALIAS)
    
    photo = ImageTk.PhotoImage(pil_image)
    
    canvas.config(width=pil_image.width, height=pil_image.height)
    
    canvas.photo = photo
    canvas.create_image(0, 0, image=photo, anchor="nw")


def save_canvas_image(canvas, canvas_width, canvas_height):
    # Capture the contents of the canvas as an image
    x = canvas.winfo_rootx()+150
    y = canvas.winfo_rooty()+50
    x1 = x + 800
    y1 = y + 700
    image = ImageGrab.grab(bbox=(x, y, x1, y1))

    # Ask the user for a file path to save the image
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    # Save the captured image to the specified file path
    if file_path:
        image.save(file_path)

def save_image():
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    save_canvas_image(canvas, canvas_width, canvas_height)

root =tk.Tk()
root.geometry("1000x600")
root.title("Image processing tool")
root.config(bg = "white")


left_frame = tk.Frame(root,width=200,height=600,bg="white")
left_frame.pack(side="left" ,fill="y")

canvas = tk.Canvas(root,width=750,height=600)
canvas.pack()

image_btn = tk.Button(left_frame,text="Add image",command = add_img,bg="white")
image_btn.pack(pady=15)

color_btn = tk.Button(left_frame,text="Change pen Color",command= change_clr)
color_btn.pack(pady=5)

pen_size_frame = tk.Frame(left_frame,bg="white")
pen_size_frame.pack(pady=5)

pen_size_1 = tk.Radiobutton(pen_size_frame,text="Small",value=3,command=lambda: change_size(3),bg = "white")
pen_size_1.pack(side="left")

pen_size_2 = tk.Radiobutton(pen_size_frame,text="Medium",value=5,command=lambda: change_size(5),bg = "white")
pen_size_2.pack(side="left")
pen_size_2.select()

pen_size_3 = tk.Radiobutton(pen_size_frame,text="Large",value=7,command=lambda: change_size(7),bg = "white")
pen_size_3.pack(side="left")

clear_btn = tk.Button(left_frame,text="Clear",command=clear_canvas,bg="#FF9797")
clear_btn.pack(pady=10)

filter_lbl = tk.Label(left_frame,text="Select Filter",bg="white")
filter_lbl.pack(pady=10)

filter_combobox = ttk.Combobox(left_frame,values=["Black and White","Threshold","Blur","Inverse","Enhance grayscale image","Enhance color Image","Edge detection",
                                                  "Draw Contours","Count objects"])
filter_combobox.pack()

filter_combobox.bind("<<ComboboxSelected>>",lambda event: apply_filter(filter_combobox.get()))


capture_button = tk.Button(left_frame, text="Crop picture", command=mouse_event)
capture_button.pack(pady=15)

brush_button = tk.Button(left_frame, text=" Apply brush", command=mouse_brush)
brush_button.pack(pady=15)


save_button = tk.Button(left_frame, text="Save Image",command=save_image,bg="white")
save_button.pack(pady=20)

canvas.bind("<B1-Motion>",draw)

root.mainloop()

