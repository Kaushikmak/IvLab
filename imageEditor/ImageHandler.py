import numpy as np
import matplotlib.pyplot as plt

#class which will handle all image processing
class ImageHandling():
    def __init__(self,path):
        self.path = path
        
        
    '''thi8s function will return image if exists to the main.py file, to get image array for tkinter to show on UI
    also it will return both scale down version of image to fit it into tkinter label(but we are woking with real image shape
    here we are downsampling our image by factor of 3) and original image in form of array'''
    def imageReturn(self):
        try:
            image = plt.imread(self.path)
            shape = list(image.shape)
            return [image[::5,::5,:],image,shape]
        except FileNotFoundError:
            pass

    def imageCrop(self,leftcrop,rightcrop,topcrop,bottomcrop):
        image = self.imageReturn()[1]
        shape = self.imageReturn()[2]
        try:
            croppedImage = image[topcrop:shape[0]-bottomcrop,leftcrop:shape[1]-rightcrop,:]
            return [croppedImage[::5,::5,:],croppedImage]
        except ValueError:
            pass


    


