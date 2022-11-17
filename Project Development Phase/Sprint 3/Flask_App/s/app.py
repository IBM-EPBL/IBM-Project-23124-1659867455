# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 09:42:22 2022

@author: achu6
"""

import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, url_for, redirect
from PIL import Image
from tensorflow import keras
from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, ImageOps
import numpy as np

#load the model
model=load_model('models/mnistCNN1.h5') 

app=Flask(__name__)

#index homepage
@app.route('/')
def index():
    return render_template('index.html')

#external github link from navbar
@app.route('/redirect_to')
def redirect_to():
    return redirect("https://github.com/IBM-EPBL/IBM-Project-42343-1660660246/tree/main/Project%20Development%20Phase/Sprint%203")

#upload image web.html page
@app.route('/web',methods=['GET','POST'])
def web():
    if request.method=='POST':
        img = Image.open(request.files['imgfile'].stream).convert("L")
        img = img.resize((28,28))
        im2arr = np.array(img)
        im2arr = im2arr.reshape(1,28,28,1)
        pred = model.predict(im2arr)
        num = np.argmax(pred, axis=1)  
        return render_template('web.html', prediction=str(num[0]),dispimg="True")

    else:
        return render_template('web.html')

@app.route('/draw',methods=['GET','POST'])
def draw():
    def predict_digit(img):
    #resize image to 28×28 pixels
        img = img.resize((28,28))
        #convert rgb to grayscale
        img = img.convert('L')
        img = ImageOps.invert(img)
        img = np.array(img)
        #reshaping to support our model input and normalizing
        img = img.reshape(1,28,28,1)
        img = img/255.0
        #predicting the class
        res = model.predict([img])[0]
        return np.argmax(res), max(res)

    class App(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)

            self.x = self.y = 0

            # Creating elements
            self.canvas = tk.Canvas(self, width=300, height=300, bg = "white", cursor="cross")
            self.label = tk.Label(self, text="Thinking..", font=("Helvetica", 48))
            self.classify_btn = tk.Button(self, text = "Recognise", command =         self.classify_handwriting) 
            self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)

            # Grid structure
            self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
            self.label.grid(row=0, column=1,pady=2, padx=2)
            self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
            self.button_clear.grid(row=1, column=0, pady=2)

            #self.canvas.bind("<Motion>", self.start_pos)
            self.canvas.bind("<B1-Motion>", self.draw_lines)

        def clear_all(self):
            self.canvas.delete("all")

        def classify_handwriting(self):
            HWND = self.canvas.winfo_id() # get the handle of the canvas
            rect = win32gui.GetWindowRect(HWND) # get the coordinate of the canvas
            im = ImageGrab.grab(rect)

            digit, acc = predict_digit(im)
            self.label.configure(text= str(digit)+', '+ str(int(acc*100))+'%')

        def draw_lines(self, event):
            self.x = event.x
            self.y = event.y
            r=8
            self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')

    app = App()
    mainloop()


if __name__ == '__main__':
    app.run(debug=True)

