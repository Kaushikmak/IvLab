import numpy as np
import matplotlib.pyplot as plt
from PIL import Image #since we need to convert ndarray into image so we have to use this module

#class which will handle all image processing
class ImageHandling():
    def __init__(self,path):
        self.path = path
        
        
    '''this function will return image if exists to the main.py file, to get image array for tkinter to show on UI
    also it will return both scale down version of image to fit it into tkinter label(but we are woking with real image shape
    here we are downsampling our image by factor of 5) and original image in form of array
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

    def imageToBeBlend(self,imagepath2):
        global imageToBlend
        imageToBlend = plt.imread(imagepath2)
        
    def imageBlend(self,weight):
        try:
            image1 = plt.imread(self.path)
            image2 = imageToBlend
            #making both images of equall shape
            imageShape1 = image1.shape
            imageShape2 = image2.shape
            desiredShape = (min(imageShape1[0],imageShape2[0]),min(imageShape1[1],imageShape2[1]))

            image1 = np.array(Image.fromarray(image1).resize(desiredShape[::-1]))
            image2 = np.array(Image.fromarray(image2).resize(desiredShape[::-1]))

            blendedImage = image1*weight + image2*(1-weight)
            
            return [blendedImage[::5,::5,:].astype(np.uint8),blendedImage.astype(np.uint8)]
        except (FileNotFoundError, NameError):
            pass

    #rotate image
    def rotationOfImage(self,angle):
        
        image = self.imageReturn()[1]

        angle = angle * (np.pi/80)
        sincosMatrix = np.transpose(np.array([[np.cos(angle),-np.sin(angle)],
                                                [np.sin(angle),np.cos(angle)]]))
        a =  image.shape[0]
        b = image.shape[1]
        
        startPointX =  0
        startPointY = 0
        #rotate image from defined matrix of sin and cos
        rotatedImage = np.zeros(image.shape,dtype='u1') 
        for height in range(a):
            for width in range(b):
                xyMatrix = np.array([[width-startPointX],[height-startPointY]])
                rotatedMatrix = np.dot(sincosMatrix,xyMatrix)
                xModified = startPointX + int(rotatedMatrix[0])
                yModified = startPointY + int(rotatedMatrix[1])
                print("working:")
                if (0<=xModified<=b-1) and (0<=yModified<=a-1): 
                    rotatedImage[yModified,xModified] = image[height,width]

        print("done")
      
        return [rotatedImage[::5,::5,:].astype(np.uint8),rotatedImage.astype(np.uint8)]

        


    


