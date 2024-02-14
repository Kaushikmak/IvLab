import os
import cv2
import numpy as np

class vectorfeature:
    def __init__(self, imagepath, chiThreshold :float):
        image = cv2.imread(imagepath)
        self.vector = self.imageHistogramVector(image)
        #images lits in database
        listOfImages = self.imagesInFolder("visualQueryEngine/ImageDataset/BBT")
        list2OfImages = self.imagesInFolder("visualQueryEngine/ImageDataset/Hobbit")
        list3OfImages = self.imagesInFolder("visualQueryEngine/ImageDataset/HouseMD")
        list4OfImages = self.imagesInFolder("visualQueryEngine/ImageDataset/TSimpsons")

        allImages = [listOfImages,list2OfImages,list3OfImages,list4OfImages]
        #vector if images in database
        bbtVector = np.array([self.imageHistogramVector(listOfImages[i]) for i in range(len(listOfImages))])
        HobbitVector = np.array([self.imageHistogramVector(list2OfImages[i]) for i in range(len(list2OfImages))])
        HouseMDVector = np.array([self.imageHistogramVector(list3OfImages[i]) for i in range(len(list3OfImages))])
        TSimpsonsVector = np.array([self.imageHistogramVector(list4OfImages[i]) for i in range(len(list4OfImages))])
        
        #chi-squared distance between searched Image and images in database
        bbtDistance = np.array([self.chiSquareDistance(self.vector,bbtVector[i]) for i in range(len(bbtVector))])
        HobbitDistance = np.array([self.chiSquareDistance(self.vector,HobbitVector[i]) for i in range(len(HobbitVector))])
        HouseMDDistance = np.array([self.chiSquareDistance(self.vector,HouseMDVector[i]) for i in range(len(HouseMDVector))])
        TSimpsonsDistance = np.array([self.chiSquareDistance(self.vector,TSimpsonsVector[i]) for i in range(len(TSimpsonsVector))])
        
        allDistances = [bbtDistance, HobbitDistance, HouseMDDistance, TSimpsonsDistance]
        # all distance which lies in given threshold
        indexesReq = []
        for i in range(len(allDistances)):
            for j in range(len(allDistances[i])):
                if (allDistances[i][j] <= chiThreshold):
                    indexesReq.append([i,j])
        print(indexesReq)
        for i in range(len(indexesReq)):
            folderIndex = indexesReq[i][0]
            imageIndex = indexesReq[i][1]
            print(folderIndex,imageIndex)
            cv2.imshow("Images Matched",allImages[folderIndex][imageIndex])
            cv2.waitKey(0)

        
    # find all images in folder
    def imagesInFolder(self,folder):
        images = []
        for filename in os.listdir(folder):
            img = cv2.imread(os.path.join(folder,filename))
            if img is not None:
                images.append(img)
        return images
    # return normalised vector hgistogram
    def imageHistogramVector(self,image):
        
        b, g, r = cv2.split(image)
        histBlue = cv2.calcHist([b], [0], None, [256], [0, 256])
        histGreen = cv2.calcHist([g], [0], None, [256], [0, 256])
        histRed = cv2.calcHist([r], [0], None, [256], [0, 256])

        histogramVector = np.concatenate((histBlue, histGreen, histRed), axis=None)
        normalizedvector = histogramVector/np.sum(histogramVector)

        return normalizedvector

    # return chi square diustance between two vectors
    def chiSquareDistance(self,imagevector1, imagevector2):
        distance = cv2.compareHist(imagevector1, imagevector2, cv2.HISTCMP_CHISQR)
        return distance
    


vectorfeature("visualQueryEngine/ImageDataset/BBT/bbt1.jpg",0.2)

