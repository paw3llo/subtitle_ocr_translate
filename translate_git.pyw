import requests
import tkinter as tk
import re
import numpy as np
    #import cv2
from PIL import ImageGrab
from easyocr import Reader
import string
import config
window = tk.Tk()
#window.title('translate')
window.geometry("+35+70")

import os
lista_plikow=os.listdir('c:/Users/pawel/Desktop/slownik_skrypt/')
lista_txt=list(filter(lambda nazwa_pliku:nazwa_pliku.endswith('.txt'), lista_plikow))
lista_txt_strvar=tk.StringVar(value=lista_txt)

file_list=tk.Listbox(window,height=3,listvariable=lista_txt_strvar,selectmode=tk.SINGLE,exportselection=False)
file_list.select_set(lista_txt.index('lista_slowek.txt'))
file_list.pack()


def quit_window(event):
    window.destroy()


window.bind('<Escape>', quit_window)


def output_txt(zrodlo, tlumaczenie):
    #with open('lista_slowek.txt', 'a') as f:
    with open(file_list.get(file_list.curselection()[0]), 'a') as f:
        #f.write(str(file_list.get(file_list.curselection()[0])) + '\r')
        f.write(zrodlo + '  ' + tlumaczenie + '\r')


def clear_word_labels():
    for x in propositions_list:
        x.destroy()
    propositions_list.clear()
    for word_details_label in word_details_labels:
        word_details_label.destroy()
    word_details_labels.clear()
    for word_label in word_labels:
        word_label.destroy()
    word_labels.clear()
    for word_button1 in word_buttons:
        word_button1.destroy()
    word_buttons.clear()
    for word_frame in word_frames:
        word_frame.destroy()
    word_frames.clear()
    for scrollbar1 in scrollbar:
        scrollbar1.destroy()
    scrollbar.clear()
    for translation_frame1 in translation_frame:
        translation_frame1.destroy()
    translation_frame.clear()
    for translation_canvas1 in translation_canvas:
        translation_canvas1.destroy()
    translation_canvas.clear()


def onScrollWheel(event,canvas):
    canvas.yview_scroll(-1*(event.delta/120), "units")



def onFrameConfigure(event,canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.configure(width=canvas.bbox('all')[2])
    if canvas.bbox('all')[3]>300:
        canvas.configure(height=300)
    else:
        canvas.configure(height=canvas.bbox('all')[3])

def get_word(*args):
    clear_word_labels()
    input_word = word_entry.get()
    api_url = 'https://api.pons.com/v1/dictionary'
    api_params = {'q': input_word, 'l': 'depl','fm':'1' ,'ref': 'false'}
    api_header = {
        'X-Secret': config.api_key}
    response = requests.get(api_url, params=api_params, headers=api_header)
    
    if response.status_code==200:
        translation_canvas.append(tk.Canvas())
        scrollbar.append(tk.Scrollbar(orient="vertical", command=translation_canvas[0].yview))
        translation_frame.append(tk.Frame(translation_canvas[0]))
        translation_canvas[0].configure(yscrollcommand=scrollbar[0].set)
        scrollbar[0].pack(side="right", fill="y")
        word_list = response.json()
        word_dict = word_list[0]
        ##
        #word_details = word_dict['hits'][0]['roms'][0]['headword_full']
        #word_details_labels.append(
        #    tk.Label(translation_frame[0],text=re.sub('<[^<]+?>', '', word_details)))
        #word_details_labels[len(word_details_labels)-1].pack()
        ##
        word_hits = word_dict['hits']
        for word_hit in word_hits:
            word_roms = word_hit['roms']
            for word_rom in word_roms:
                word_details = word_rom['headword_full']
                word_details_labels.append(
                tk.Label(translation_frame[0], bg='sky blue',text=re.sub('<[^<]+?>', '', word_details)))
                word_details_labels[len(word_details_labels)-1].pack()
                word_arabs = word_rom['arabs']
                for word_arab in word_arabs:
                    word_translations = word_arab['translations']
                    for word_translation in word_translations:
                        word_frames.append(tk.Frame(translation_frame[0]))
                        word_frames[len(word_frames)-1].pack()
                        word_labels.append(tk.Label(master=word_frames[len(
                            word_frames)-1], text=re.sub('<[^<]+?>', '', word_translation['source']), relief='ridge'))
                        word_labels[len(word_labels)-1].pack(side=tk.LEFT)
                        word_buttons.append(tk.Button(master=word_frames[len(
                            word_frames)-1], text=re.sub('<[^<]+?>', '', word_translation['target']),command=lambda zrodlo=re.sub(
                            '<[^<]+?>', '', word_translation['source']), tlumaczenie=re.sub('<[^<]+?>', '', word_translation['target']): output_txt(zrodlo, tlumaczenie), relief='ridge'))
                        word_buttons[len(word_buttons)-1].pack(side=tk.RIGHT)
            translation_frame[0].pack()
            translation_canvas[0].create_window(0, 0, anchor='nw', window=translation_frame[0])
            translation_canvas[0].pack()
            translation_frame[0].bind("<Configure>", lambda event, canvas=translation_canvas[0]: onFrameConfigure(event,canvas))
            #window.bind_all("<MouseWheel>", lambda event, canvas=translation_canvas[0]:  onScrollWheel(event,canvas))
            
    else:
        word_details_labels.append(tk.Label(text=str(response.status_code) +' nie znaleziono',bg='red'))
        word_details_labels[len(word_details_labels)-1].pack()
    word_entry.selection_range(0, tk.END)

def get_clipboard():
    word_entry.delete(0,tk.END)
    word_entry.insert(0, window.clipboard_get())
    get_word()

word_entry = tk.Entry()
word_entry.pack()
word_entry.focus()
word_entry.bind('<Return>', get_word)
# special character buttons
special_char_frame = tk.Frame()
special_char_frame.pack()
special_a_button = tk.Button(special_char_frame, text='(f1) ä', command=lambda: word_entry.insert(
    word_entry.index(tk.INSERT), 'ä')).pack(side=tk.LEFT)
window.bind('<F1>',lambda event: word_entry.insert(word_entry.index(tk.INSERT), 'ä'))
special_o_button = tk.Button(special_char_frame, text='(f2) ö', command=lambda: word_entry.insert(
    word_entry.index(tk.INSERT), 'ö')).pack(side=tk.LEFT)
window.bind('<F2>',lambda event: word_entry.insert(word_entry.index(tk.INSERT), 'ö'))
special_u_button = tk.Button(special_char_frame, text='(f3) ü', command=lambda: word_entry.insert(
    word_entry.index(tk.INSERT), 'ü')).pack(side=tk.LEFT)
window.bind('<F3>',lambda event: word_entry.insert(word_entry.index(tk.INSERT), 'ü'))
special_ss_button = tk.Button(special_char_frame, text='(f4) ß', command=lambda: word_entry.insert(
    word_entry.index(tk.INSERT), 'ß')).pack(side=tk.LEFT)
window.bind('<F4>',lambda event: word_entry.insert(word_entry.index(tk.INSERT), 'ß'))

scrollbar=[]
translation_canvas=[]
translation_frame=[]
word_frames = []
word_labels = []
word_buttons = []
word_details_labels = []
propositions_list=[]

gui_buttons_frame=tk.Frame(window)
gui_buttons_frame.pack()


def word_proposition_lookup(word_prop):
    for x in propositions_list:
        x.destroy()
    propositions_list.clear()
    word_entry.delete(0,tk.END)
    word_entry.insert(0, word_prop)
    get_word()


def scr_ocr(*args):
    clear_word_labels()
    #ard default: image = ImageGrab.grab(bbox=(460,860,1300,965))
    #probne zdf (pauza) + ard ponizej + ard firefox
    image = ImageGrab.grab(bbox=(350,827,1450,1025))
    #image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    image = np.array(image)
    reader = Reader(['de'], gpu=False)
    result = reader.readtext(image,paragraph="False")
    for line in result:
        ocr_word_list=line[1].split()
        for word_proposition in ocr_word_list:
            word_prop_bezinterpun=word_proposition.translate(str.maketrans('', '', string.punctuation))
            propositions_list.append(tk.Button(window,text=word_prop_bezinterpun,command=lambda word_prop=word_prop_bezinterpun : word_proposition_lookup(word_prop)))
            propositions_list[len(propositions_list)-1].pack()


button1=tk.Button(gui_buttons_frame,text='(f5)ocr',command=scr_ocr)
button1.pack(side=tk.RIGHT)
window.bind('<F5>',lambda event:scr_ocr())
word_button = tk.Button(gui_buttons_frame,text='wyszukaj', command=get_word)
word_button.pack(side=tk.RIGHT)
button2=tk.Button(gui_buttons_frame,text='(f6)clip',command=get_clipboard)
button2.pack(side=tk.LEFT)
window.bind('<F6>',lambda event:get_clipboard())


window.mainloop()

