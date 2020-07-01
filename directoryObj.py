import shutil
import os

class directoryObj:
    def __init__(self, filepath, button):
        self.destFilepath = filepath
        self.button = button

    def moveFile(self, filenames, inputPath, folder):
        if not os.path.exists(self.destFilepath + "/" + folder):
            os.makedirs(self.destFilepath + "/" + folder)
            print("Creating folder: " + folder)
        try:
            for files in filenames:
                shutil.move(inputPath + "/" + files, self.destFilepath + "/" + folder + "/" + files)
                print("Move Successful")
            return True

        except:
            print("Move file failed...")
            return False

    def makeDirectory(self, name, path):
        os.mkdir(path + "/" + name)