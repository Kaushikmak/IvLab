import tkinter as tk
from tkinter import ttk, filedialog, TclError
from PIL import Image, ImageTk
import ImageHandler
import time


#main window class for UI
class mainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # setting up title, size, etc.
        self.title("Image Editor")
        self.geometry("1024x786")
        self.resizable(False,False)

        #calling frames to main window
        self.menu1 = imageFrame(self)
        # self.menu2 = buttonsFrame(self)
        
        self.mainloop()

#left side image frame to fit image in that
class imageFrame(ttk.Frame):
    def __init__(self,mother):
        super().__init__(mother)
        ttk.Label(self,background="#2C3333").pack(expand=True,fill="both")
        self.place(relx=0,rely=0,relwidth=1,relheight=1.0)
        self.widgets()

    #widgets i.e buttons entry fields, etc.
    def widgets(self):
        
        #open file(image) button
        openImageButton = ttk.Button(self,text="Open Image",command=self.open_image)
        openImageButton.place(relx=0.7,rely=0.07,relheight=0.07,relwidth=0.25)
        
        #crop widget fields
        ttk.Label(self,text="Crop image enter values in pixels",font=("arial",9),foreground="white",background="#2C3333").place(relx=0.7,rely=0.15,relwidth=0.25,relheight=0.07)
            #crop entry fields
        self.leftCrop = tk.IntVar()
        self.rightCrop = tk.IntVar()
        self.topCrop = tk.IntVar()
        self.bottomCrop = tk.IntVar()
        #crop entry widgets
        ttk.Entry(self,textvariable=self.leftCrop).place(relx=0.7,rely=0.3,relheight=0.03,relwidth=0.09)
        ttk.Entry(self,textvariable=self.rightCrop).place(relx=0.85,rely=0.3,relheight=0.03,relwidth=0.09)
        ttk.Entry(self,textvariable=self.topCrop).place(relx=0.77,rely=0.25,relheight=0.03,relwidth=0.09)
        ttk.Entry(self,textvariable=self.bottomCrop).place(relx=0.77,rely=0.35,relheight=0.03,relwidth=0.09)
        #crop submit button
        cropButton = ttk.Button(self,text="CROP",command=self.crop_image)
        cropButton.place(rely=0.4,relx=0.7,relheight=0.07,relwidth=0.25)


        #image blending
        ttk.Label(self,text="select another image to blend",font=("arial",9),foreground="white",background="#2C3333").place(relx=0.7,rely=0.45,relwidth=0.25,relheight=0.07)
        openBlendingImage = ttk.Button(self,text="Open blending Image",command=self.blending_image)
        openBlendingImage.place(relx=0.7,rely=0.52,relheight=0.07,relwidth=0.25)
        #image blending weight
        self.weight = tk.DoubleVar()
        ttk.Entry(self,textvariable=self.weight).place(relx=0.8,rely=0.6,relheight=0.05,relwidth=0.15)
        ttk.Label(self,text="Weight of\nfirst image",background="#2C3333",font=("arial",9),foreground="white").place(relx=0.7,rely=0.6,relheight=0.05,relwidth=0.1)
        #image blending button
        blendButton = ttk.Button(self,text="BLEND IMAGES !",command=self.Blend)
        blendButton.place(relx=0.7,rely=0.67,relheight=0.05,relwidth=0.25)

        #image rotation scale
        ttk.Label(self,text="Rotate image !\nEnter angel to rotate image",background="#2C3333",font=("arial",9),foreground="white").place(relx=0.7,rely=0.73,relwidth=0.25)
        self.ScaleVariable = tk.DoubleVar()
        ttk.Entry(self,textvariable=self.ScaleVariable).place(relx=0.7,rely=0.78,relwidth=0.1,relheight=0.05)
        ttk.Button(text="ROTATE",command=self.RotateImage).place(relx=0.85,rely=0.78,relwidth=0.1,relheight=0.05)

        #image blur
        ttk.Label(self,text="blur\nImage",background="#2C3333",font=("arial",9),foreground="white").place(relx=0.7,rely=0.84,relwidth=0.25)
        self.blurVariable = tk.IntVar()
        ttk.Entry(self,textvariable=self.blurVariable).place(relx=0.75,rely=0.84,relwidth=0.08,relheight=0.05)
        ttk.Button(text="Blur",command=self.BlurImage).place(relx=0.85,rely=0.84,relwidth=0.1,relheight=0.05)

        #reset button: this will reset image label
        resetButton = ttk.Button(self,text="RESET",command=self.reset_label)
        resetButton.place(relx=0.7,rely=0.9,relheight=0.07,relwidth=0.25)

    #this label will update in realtime as changes are made by user
    def current_image_label(self,image):
        tk.Label(self, background="#2C3333" , image=image).place(relx=0.07,rely=0.07,relwidth=0.55,relheight=0.86)


    #open image function when open file button is pressed
    def open_image(self):
        #defining file types supported
        global rotImage
        fileTypeSupported = [("Image files","*.png *.jpg *.jpeg")]
        self.fileName = filedialog.askopenfilename(title="Open Photo",initialdir="/",filetypes=fileTypeSupported)
        rotImage = self.fileName
        try:
            #calling ImageHandler module
            img = ImageHandler.ImageHandling(path=self.fileName).imageReturn()[0]
            img = Image.fromarray(img)
            self.imgTk = ImageTk.PhotoImage(image=img)
            #now update image label
            self.current_image_label(self.imgTk)
            
        except AttributeError:
            pass

    '''When crop button is clicked this method is called and it will also invoke ImageHandling class where cropping is done 
    and in return cropped image is obatained both scaled down version and original 1:1 scale'''
    def crop_image(self):
        try:
            #calling crop method
            img = ImageHandler.ImageHandling(path=self.fileName).imageCrop(self.leftCrop.get(),self.rightCrop.get(),self.topCrop.get(),self.bottomCrop.get())[0]
            img = Image.fromarray(img)
            self.croppedImageTk = ImageTk.PhotoImage(image=img)
            #updating real time crop image
            self.current_image_label(self.croppedImageTk)
        except (TclError,AttributeError):
            pass

    #reset lebel function
    def reset_label(self):
        try:
            img = ImageHandler.ImageHandling(path=self.fileName).imageReturn()[0]
            img = Image.fromarray(img)
            self.imgreset = ImageTk.PhotoImage(image=img)
            self.current_image_label(self.imgreset)
        except AttributeError:
            pass

    def blending_image(self):
        fileTypeSupported = [("Image files","*.png *.jpg *.jpeg")]
        self.fileNameblend = filedialog.askopenfilename(title="Open Photo to blend",initialdir="/",filetypes=fileTypeSupported)
        try:
            #calling ImageHandler module and sending image's location which is to be blended
            ImageHandler.ImageHandling(path=self.fileNameblend).imageToBeBlend(self.fileNameblend)
            
        except AttributeError:
            pass

    def Blend(self):
        try:
            img = ImageHandler.ImageHandling(path=self.fileName).imageBlend(self.weight.get())[0]
            img = Image.fromarray(img)
            self.blendedImage = ImageTk.PhotoImage(image=img)
            self.current_image_label(self.blendedImage)
        except (TclError,AttributeError,TypeError):
            pass

  

    def RotateImage(self):
        try:
           
            angle = self.ScaleVariable.get()
            img = ImageHandler.ImageHandling(rotImage).rotationOfImage(angle)[0]
            img = Image.fromarray(img)
            self.resetImage = ImageTk.PhotoImage(image=img)
            self.current_image_label(self.resetImage)
            
        except (TypeError,AttributeError,NameError):
            pass

    def BlurImage(self):
        try:
            blur = self.blurVariable.get()*10
            img = ImageHandler.ImageHandling(rotImage).blurImage(blur)[0]
            img = Image.fromarray(img)
            self.resetImage = ImageTk.PhotoImage(image=img)
            self.current_image_label(self.resetImage)
        except (TypeError, AttributeError, NameError):
            pass

mainWindow()