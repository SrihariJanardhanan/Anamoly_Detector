import pickle as pkl
import cv2
import numpy as np
import os
from videoTransforms import *
from model import model

def predict_from_model(filename):
    model.load_weights('keras_model.h5')
    # Convert from video to numpy
    tdata = Video2Npy('./uploads/'+filename)
    tdata = np.uint8(tdata)
    tdata = np.float32(tdata)

    # Applying transforms
    tdata = uniform_sampling(video=tdata, target_frames=64)
    tdata[...,:3] = color_jitter(tdata[...,:3])
    tdata = random_flip(tdata, prob=0.5)
    tdata[...,:3] = normalize(tdata[...,:3])
    tdata[...,3:] = normalize(tdata[...,3:])
    tdata = tdata[np.newaxis, ...]
    # Generate Model predictions
    pred = model(tdata)
    pred = np.array(pred).argmax()
    out = "Anomaly" if pred==0 else "Normal" 
    return out
    


