import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import ImageHandler


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

    #widgets i.3 buttons entry fields, etc.
    def widgets(self):
        
        #open file(image) button
        openImageButton = ttk.Button(self,text="Open Image",command=self.open_image)
        openImageButton.place(relx=0.7,rely=0.07,relheight=0.07,relwidth=0.25)
        
        #crop widget fields
        ttk.Label(self,text="Crop image enter values in pixels",font=("arial",8),foreground="white",background="#2C3333").place(relx=0.7,rely=0.15,relwidth=0.25,relheight=0.07)
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

    def current_image_label(self,image):
        tk.Label(self, background="#2C3333" , image=image).place(relx=0.07,rely=0.07,relwidth=0.55,relheight=0.86)

    #open image function when open file button is pressed
    def open_image(self):
        #defining file types supported
        fileTypeSupported = [("Image files","*.png *.jpg *.jpeg")]
        self.fileName = filedialog.askopenfilename(title="Open Photo",initialdir="/",filetypes=fileTypeSupported)

        try:
            #calling ImageHandler module
            img = ImageHandler.ImageHandling(path=self.fileName).imageReturn()[0]
            img = Image.fromarray(img)
            self.imgTk = ImageTk.PhotoImage(image=img)
            #now update image label
            self.current_image_label(self.imgTk)
            
        except AttributeError:
            pass

    def crop_image(self):
        try:
            img = ImageHandler.ImageHandling(path=self.fileName).imageCrop(self.leftCrop.get(),self.rightCrop.get(),self.topCrop.get(),self.bottomCrop.get())[0]
            img = Image.fromarray(img)
            self.croppedImageTk = ImageTk.PhotoImage(image=img)
            self.current_image_label(self.croppedImageTk)
        except AttributeError:
            pass
        


mainWindow()