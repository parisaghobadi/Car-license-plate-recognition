import numpy as np
import cv2 as cv
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import imutils

def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        car_img = cv.imread(file_path)
        car_img_gray = cv.cvtColor(car_img, cv.COLOR_BGR2GRAY)
        bilateral_filtered = cv.bilateralFilter(car_img_gray, 11, 15, 15)
        edges = cv.Canny(bilateral_filtered, 30, 200)
        contours = cv.findContours(edges.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours_refined = imutils.grab_contours(contours)
        contours_sorted = sorted(contours_refined, key=cv.contourArea, reverse=True)[:4]
        for contour in contours_sorted:
            contours_approx = cv.approxPolyDP(contour, 10, True)
            if len(contours_approx) == 4:
                plate_location = contours_approx
                break
        plate_mask0 = np.zeros(car_img_gray.shape, np.uint8)
        plate_mask = cv.drawContours(plate_mask0, [plate_location], 0, 255, -1)
        plate_image = cv.bitwise_and(car_img, car_img, mask=plate_mask)
        display_image(plate_image)

def display_image(image):
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    img_pil = Image.fromarray(image_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    label.config(image=img_tk)
    label.image = img_tk

root = tk.Tk()
root.title("پروژه‌ی تشخیص پلاک ماشین")
root.geometry("800x600")  
root.configure(bg="dark blue") 

load_button = tk.Button(root, text="بارگذاری تصویر", command=load_image, bg="light blue", font=("Helvetica", 12))
load_button.pack(pady=20)  

text_label = tk.Label(root, text=" : پلاک ماشین ", font=("Helvetica", 14), fg="white", bg="dark blue")
text_label.pack()

label = tk.Label(root)
label.pack()

root.mainloop()