import numpy as np
import matplotlib.pyplot as plt

#class which will handle all image processing
class ImageHandling():
    def __init__(self,path):
        self.path = path
        
        
    '''this function will return image if exists to the main.py file, to get image array for tkinter to show on UI
    also it will return both scale down version of image to fit it into tkinter label(but we are woking with real image shape
    here we are downsampling our image by factor of 3) and original image in form of array
    [Later edition] I've also added a shape return type as it was required
    '''
    def imageReturn(self):
        try:
            image = plt.imread(self.path)
            shape = list(image.shape)
            return [image[::5,::5,:],image,shape]
        except FileNotFoundError:
            pass
    '''
        this function will crop image from top bottom right left as values given by user in UI
        and return a original and scaledown version of image to UI
    '''
    def imageCrop(self,leftcrop,rightcrop,topcrop,bottomcrop):
        image = self.imageReturn()[1]
        shape = self.imageReturn()[2]
        try:
            croppedImage = image[topcrop:shape[0]-bottomcrop,leftcrop:shape[1]-rightcrop,:]
            return [croppedImage[::5,::5,:],croppedImage]
        except ValueError:
            pass

    
    def imageBlend(self,imagePath2,weight):
        try:
            image1 = plt.imread(self.path)
            image2 = plt.imread(imagePath2)
            #making both images of equall shape
            imageShape1 = image1.shape
            imageShape2 = image2.shape
            desiredShape = (max(image1[0],image2[0]),max(image1[1],image2[1]))
            print(imageShape1)
            print(imageShape2)
            
            print(desiredShape)
            image1 = image1.reshape(desiredShape)
            image2 = image2.reshape(desiredShape)

            blendedImage = image1*weight + image2*(1-weight)
            blendedImage = np.clip(blendedImage,0,255)
            return [blendedImage[::5,::5,:],blendedImage]
            pass
        except FileNotFoundError:
            pass




    


