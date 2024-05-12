
import numpy as np
import matplotlib.pyplot as plt
import cv2



def count_func():
    img = cv2.imread("C:/Users/ASUS/Pictures/Camera Roll")
    img_copy_1 = img.copy()
    img_g = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ret,thresh_img = cv2.threshold(img_g,60,255,0)

    thresh_final = cv2.bitwise_not(thresh_img)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(31,31))

    opened_img = cv2.morphologyEx(thresh_final,cv2.MORPH_OPEN,kernel)

    contours,h = cv2.findContours(opened_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_img = cv2.drawContours(img_copy_1,contours,-1,(0,255,0),2)

    print(len(contours))

    area = 0
    perimeter = 0

    for i in range(len(contours)):
        temp_area = cv2.contourArea(contours[i])
        temp_perimeter = cv2.arcLength(contours[i],True)
        area += temp_area
        perimeter += temp_perimeter
        

    print("Area : ",area,"Perimeter : ",perimeter)
    sort_area = sorted(contours,key=cv2.contourArea,reverse=True)
    print("Perimeter of 2nd largest coin",cv2.arcLength(sort_area[1],True))


    plt.subplot(141)
    plt.title("Image")
    plt.axis('off')
    plt.imshow(img)

    plt.subplot(142)
    plt.title("Thresholded image")
    plt.axis('off')
    plt.imshow(thresh_img,cmap="gray")

    plt.subplot(143)
    plt.title("Morphological Operation")
    plt.axis('off')
    plt.imshow(opened_img,cmap="gray")

    plt.subplot(144)
    plt.title("Contour image")
    plt.axis('off')
    plt.imshow(contour_img,cmap="gray")

    plt.show()

count_func()