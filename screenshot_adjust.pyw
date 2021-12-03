import numpy as np
import cv2
import tkinter as tk
from PIL import ImageGrab, ImageTk
from easyocr import Reader

window=tk.Tk()

image_label = []
#ard default[460,860,1300,965]
#zdf(pauza) + ard dafault??? [350,827,1450,965]
#ard firefox [350,827,1450,1025]
scr_coordinates=[350,827,1450,1025]
ard_default_label=tk.Label(text=scr_coordinates)
ard_default_label.pack()
y_up= tk.IntVar()
coord_entry_y_up=tk.Entry(textvariable=y_up)
coord_entry_y_up.pack()
y_up.set(scr_coordinates[0])

x_up= tk.IntVar()
coord_entry_x_up=tk.Entry(textvariable=x_up)
coord_entry_x_up.pack()
x_up.set(scr_coordinates[1])

y_down= tk.IntVar()
coord_entry_y_down=tk.Entry(textvariable=y_down)
coord_entry_y_down.pack()
y_down.set(scr_coordinates[2])

x_down= tk.IntVar()
coord_entry_x_down=tk.Entry(textvariable=x_down)
coord_entry_x_down.pack()
x_down.set(scr_coordinates[3])

def scr_ocr():
    # take screenshot using pyautogui
    #image = pyautogui.screenshot()
    scr_coordinates[0]=y_up.get()
    scr_coordinates[1]=x_up.get()
    scr_coordinates[2]=y_down.get()
    scr_coordinates[3]=x_down.get()

    image_raw = ImageGrab.grab(bbox=scr_coordinates) 
    
    # since the pyautogui takes as a 
    # PIL(pillow) and in RGB we need to 
    # convert it to numpy array and BGR 
    # so we can write it to the disk
    image = cv2.cvtColor(np.array(image_raw),cv2.COLOR_RGB2BGR)
    # writing it to the disk using opencv
    cv2.imwrite("image2.png", image)
    #IMAGE_PATH = 'Przechwytywanie.jpg'
    #reader = Reader(['de'], gpu=False)
    #result = reader.readtext(image,paragraph="True")
    #label1=tk.Label(text=result[0][1]).pack()
    #print(result)
    global image_tk
    image_tk=ImageTk.PhotoImage(image_raw)
    if len(image_label)==1:
        image_label[0].destroy()
        image_label.clear()
    image_label.append(tk.Label(image=image_tk))

    image_label[0].pack()

button1=tk.Button(text='screenshot/ocr',command=scr_ocr)
button1.pack()

window.mainloop()