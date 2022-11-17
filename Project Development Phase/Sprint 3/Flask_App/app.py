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
    return redirect("https://github.com/IBM-EPBL/IBM-Project-23124-1659867455")

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


if __name__ == '__main__':
    app.run(debug=True)

