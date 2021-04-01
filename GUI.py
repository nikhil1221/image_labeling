#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 23:12:15 2021

@author: nikhil
"""
## UI FOR THE IMAGE LABELLING 
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.applications.xception import Xception
from keras.models import load_model
from pickle import load
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog


def load_img():
    global img, image_data
    for img_display in frame.winfo_children():
        img_display.destroy()

    image_data = filedialog.askopenfilename(initialdir="/", title="Choose an image",
                                       filetypes=(("all files", "*.*"), ("jpg files", "*.jpg")))
    basewidth = 150
    img = Image.open(image_data)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    file_name = image_data.split('/')
    panel = tk.Label(frame, text= str(file_name[len(file_name)-1]).upper()).pack()
    panel_image = tk.Label(frame, image=img).pack()
    
    
    

def extract_features(filename, model):
        try:
            image = Image.open(filename)
            
        except:
            print("ERROR: Couldn't open image! Make sure the image path and extension is correct")
        image = image.resize((299,299))
        image = np.array(image)
        # for images that has 4 channels, we convert them into 3 channels
        if image.shape[2] == 4: 
            image = image[..., :3]
        image = np.expand_dims(image, axis=0)
        image = image/127.5
        image = image - 1.0
        feature = model.predict(image)
        return feature

def word_for_id(integer, tokenizer):
 for word, index in tokenizer.word_index.items():
     if index == integer:
         return word
 return None


def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'start'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        pred = model.predict([photo,sequence], verbose=0)
        pred = np.argmax(pred)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'end':
            break
    return in_text



    
def caption_img():
    max_length = 32
    tokenizer = load(open("tokenizer.p","rb"))
    model = load_model('models/model_5.h5')
    xception_model = Xception(include_top=False, pooling="avg")
    
    photo = extract_features(image_data, xception_model)
    img = Image.open(image_data)
    
    description = generate_desc(model, tokenizer, photo, max_length)
    description=description[6:-4]
    text=tk.Label(root,text=description)
    text.place(x=100,y=300)


root =tk.Tk()
root.title("IMAGE CAPTION")
root.iconbitmap('class.ico')
root.resizable(False,False)

tit =tk.Label(root,text="Image Captioing",padx=25,pady=10,font=("",16)).pack()

canvas=tk.Canvas(root,height=500,width=500,bg='grey')
canvas.pack()

frame=tk.Frame(root,bg='white')
frame.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)

choseImage=tk.Button(root,text="Choose Image",padx=35,pady=10,fg="#f4b41a",bg="#143d59",command=load_img)
choseImage.pack(side=tk.LEFT)

captionImage=tk.Button(root,text="Caption Image",padx=35,pady=10,fg="#f4b41a",bg="#143d59",command=caption_img)
captionImage.pack(side=tk.RIGHT)                  
                     
root.mainloop()                     
                     
            