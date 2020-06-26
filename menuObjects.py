import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import time

class mainFunctions:
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(True, False)
        self.filepath = "No Folder Selected"
        self.imageCount = 0
        self.headerFrame = self.createFrame(self.window)
        self.listFrame = self.createFrame(self.window)
        self.selecteditemsList = list()
        self.canvasWidth = 400
        self.canvasHeight = 400
        self.mainImage = None
        self.numberofFolderButtons = 0


        self.fileLabel = self.createLabel(self.listFrame, "No Folder Selected")
        self.folderButton = self.createButton(self.listFrame, "Select Folder")
        self.folderButton.bind("<Button-1>", self.openFolderDirectory)
        self.imageList = list()
        self.folderButton.pack()
        self.fileLabel.pack()






        self.mainScroll = tk.Scrollbar(self.listFrame, orient="vertical")
        self.mainScroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.contentList = tk.Listbox(self.listFrame, selectmode=tk.EXTENDED, activestyle=tk.NONE, height=18)
        self.contentList.bind('<<ListboxSelect>>', self.listboxSelect)
        self.contentList.pack(side=tk.LEFT, fill=tk.Y)




        self.mainScroll.config(command=self.contentList.yview)
        self.contentList.config(yscrollcommand=self.mainScroll.set)


        self.imageCanvas = tk.Canvas(self.window, width=self.canvasWidth, height=self.canvasHeight, bg='grey')



        self.foldersFrame = self.createFrame(self.window)
        self.createFolderButton = self.createButton(self.foldersFrame, "Create Directory", 15, 2)
        self.setOutputDirectoryButton = self.createButton(self.foldersFrame, "Set Output", 15, 2)
        self.importFoldersButton = self.createButton(self.foldersFrame, "Import Folders", 15, 2)
        self.setOutputDirectoryButton.bind("<Button-1>", self.setOutputDirectory)
        self.createFolderButton.bind("<Button-1>", self.createDirectoryButton)


        self.window.bind("<Key>", self.key)
        self.outputDirectory = "No Dest. Folder Selected"
        self.outputSet = False
        self.outputLabel = self.createLabel(self.foldersFrame, self.outputDirectory, "white", "black")
        self.outputLabel.pack(side=tk.BOTTOM)
        self.createFolderButton.pack(side=tk.LEFT)
        self.setOutputDirectoryButton.pack(side=tk.LEFT)
        self.importFoldersButton.pack(side=tk.LEFT)


        self.outputFoldersFrame = tk.Frame(self.window)


    def key(self, event):
        kp = repr(event.char)
        print("pressed", kp)


    def setOutputDirectory(self, event):
        self.outputSet = True
        folder_selected = filedialog.askdirectory()
        self.outputDirectory = folder_selected
        self.outputLabel['text'] = self.outputDirectory
        self.outputLabel['fg'] = 'black'



    def createDirectoryButton(self, event):
        self.numberofFolderButtons += 1
        button = self.createButton(self.outputFoldersFrame, "Test")
        button.bind("<Button-3>", self.test)
        print(button)
        if self.numberofFolderButtons % 6 == 0:
            button.pack(side=tk.RIGHT)
        else:
            button.pack(side=tk.TOP)



    def test(self, event):
        object = event.widget
        object.destroy()
        self.numberofFolderButtons -= 1




    def displayImage(self):

        image = Image.open(self.filepath + "/" + self.selecteditemsList[0])
        width = image.size[0]
        height = image.size[1]
        aspect_ratio = width/height
        aspect_ratio = round(aspect_ratio, 3)
        if width > self.canvasWidth and width >= height:
            x = 1/self.canvasWidth
            result = aspect_ratio*x
            result = 1/result
            result = round(result)
            image = image.resize((self.canvasWidth, result))
            self.mainImage = ImageTk.PhotoImage(image)
            halfmark = round(result/2)
            offset = self.canvasHeight/2 - halfmark
            self.imageCanvas.create_image(self.canvasWidth / 2, offset, anchor=tk.N, image=self.mainImage)

        elif height > self.canvasHeight and height > width:
            x = 1/self.canvasHeight
            result = aspect_ratio/x
            result = round(result)
            image = image.resize((result, self.canvasHeight))
            self.mainImage = ImageTk.PhotoImage(image)
            self.imageCanvas.create_image(self.canvasWidth / 2, 0, anchor=tk.N, image=self.mainImage)
        else:
            halfmark = round(height/2)
            offset = self.canvasHeight/2 - halfmark
            self.mainImage = ImageTk.PhotoImage(image)
            self.imageCanvas.create_image(self.canvasWidth/2, offset, anchor=tk.N, image=self.mainImage)




        # self.mainImage = ImageTk.PhotoImage(Image.open(self.filepath + "/" + self.selecteditemsList[0]))




    def listboxSelect(self, event):


        self.selecteditemsList.clear()
        wid = event.widget
        index = wid.curselection()
        for x in index:
            self.selecteditemsList.append(wid.get(x))

        self.displayImage()








        # item = wid.get(index)
        # print(type(index))
        # print(item)






    def createFrame(self, master):
        frame = tk.Frame(master)
        return frame

    def __str__(self):
        return self.filepath

    def createButton(self, frame, iText, iWidth=12, iHeight=2, iBg="Grey", iFg="White"):
        button = tk.Button(frame, text=iText, width=iWidth, height=iHeight, bg=iBg, fg=iFg)
        return button

    def createLabel(self, frame, itext, iBg="White", iFg="Black"):
        label = tk.Label(frame, text=itext, bg=iBg, fg=iFg)
        return label

    def openFolderDirectory(self, event):
        # self.window.withdraw()
        self.imageList.clear()
        self.contentList.delete(0, tk.END)

        folder_selected = filedialog.askdirectory()
        self.filepath = folder_selected
        self.fileLabel['text'] = self.filepath
        if not self.outputSet:
            self.outputLabel['text'] = self.filepath
            self.outputLabel['fg'] = 'blue'
        try:
            fileList = os.listdir(folder_selected)
        except:
            self.fileLabel['text'] = "No Folder Selected"
            self.filepath = None
            return

        for x in fileList:
            if ".jpg" in x or ".png" in x:
                self.imageList.append(x)
        self.imageCount = len(self.imageList)
        # self.displayImageData()
        for x in range(self.imageCount):
            self.contentList.insert(x, self.imageList[x])




    def displayImageData(self):
        print(str(self.imageCount) + " items found")
        for x in self.imageList:
            print(x)



    def initializeWindows(self):



        # self.headerFrame.pack(side=tk.LEFT)
        self.listFrame.pack(side=tk.LEFT, anchor=tk.NW)
        self.imageCanvas.pack(side=tk.LEFT)
        self.foldersFrame.pack(side=tk.TOP, anchor=tk.N)
        self.outputFoldersFrame.pack(side=tk.TOP, anchor=tk.NW)





        self.window.mainloop()
