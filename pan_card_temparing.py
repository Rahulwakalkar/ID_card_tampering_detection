# -*- coding: utf-8 -*-
"""pan card temparing.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Q3Zik1xYTy_WpZxMqXIEVN8WHcKRogZm
"""

from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image
import numpy as np
import requests

!mkdir pan_card_tampering
!mkdir pan_card_tampering/image

original=Image.open(requests.get('https://thestatesman.com/wp-content/uploads/2019/07/pan-card.jpg',stream=True).raw)
tampered=Image.open(requests.get('https://assets1.cleartax-cdn.com/s/img/20170526124335/Pan4.png',stream=True).raw)

#The file format of the source file
print("original image format:",original.format)
print("tampered image format:",tampered.format)
#Image size, in pixels. The size is given as a 2-tuple(woidth,  height)
print("original image size:",original.size)
print("tampered image size:",tampered.size)

#resize images
original=original.resize((250,160))
print(original.size)
original.save('pan_card_tampering/image/original.png')

tampered=tampered.resize((250,160))
print(tampered.size)
tampered.save('pan_card_tampering/image/tampered.png')
tampered=tampered.resize((250,160))

tampered=Image.open('pan_card_tampering/image/tampered.png')
tampered.save('pan_card_tampering/image/tampered.png')

#display original image
original

#display user given image
tampered

#load the two input images
original=cv2.imread('pan_card_tampering/image/original.png')
tampered=cv2.imread('pan_card_tampering/image/tampered.png')

#convert the images to greyscale
original_grey=cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
tampered_grey=cv2.cvtColor(tampered,cv2.COLOR_BGR2GRAY)

# @title Default title text
#converting images into grey scale using open CV because in the image processing many application doesn't help us identifying the important edges of coloured images also coloured images are bit complex to understand by machine because they have three channel while grey scale has only one channel

#compute the structural similarity Index(SSIM) between the two images,  ensuring that the difference image is requ
(score,diff)=structural_similarity(original_grey,tampered_grey,full=True)
diff=(diff*255).astype("uint8")
print("SSIM:{}".format(score))

#calculating  threshold and contors
thresh=cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)

#loop over contours
for c in cnts:
  #applying contours on image
  (x,y,w,h)=cv2.boundingRect(c)
  cv2.rectangle(original,(x,y),(x+w,y+h),(0,0,255),2)
  cv2.rectangle(tampered,(x,y),(x+w,y+h),(0,0,255),2)

#display original image with  colour
print("Original")
Image.fromarray(original)

#display  tampered image with colour
print("Tampered")
Image.fromarray(tampered)

#display difference image with black
print("Difference")
Image.fromarray(diff)

#display threshold image with white
print("Threshold")
Image.fromarray(thresh)

# @title Default title text
Finding out structural  similarity of the images helped us in  finding the
difference or similarity in the shape of you images. similarly, finding out threshold
and counters based on those threshold for the images converted into grey scale binary
also helped us in shape analysis and recognition. As our SSIM is ~31.2%
 we can say that image user provided is fake or tempered. Finally we visualize the difference  and
  similarity between the images using by displaying the images with counters, difference
 and threshold

#Scope
This project can be used in different organisations where customers or users
 need to provide any kind of ID in order to get themself verified the organisation
 can use this project to find out whether the ID is original or fake. similarly this
 can be used for any type of ID like Aadhar voter ID etc