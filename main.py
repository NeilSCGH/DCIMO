import sys
import os
from lib.tools import *

class program():
    def __init__(self,args):
        self.tool = tools(args)
        self.setup(args)

    def setup(self,args):
        if self.tool.argExist("-h") or self.tool.argExist("-help"):#the folder for output files
          self.help()

        if self.tool.argHasValue("-sf"):#the folder for source files
          val=self.tool.argValue("-sf")
          self.folderPathSource=val.replace("\\","/")
        else:
          self.stop("Error, -sf (source fold) is missing !")

        if self.tool.argHasValue("-df"):#the folder for output files
          val=self.tool.argValue("-df")
          self.folderPathOutput=val.replace("\\","/")
        else:
          self.folderPathOutput=self.folderPathSource
          #self.stop("Error, -of (output folder) is missing !")

        if self.tool.argExist("-print"):#the folder for output files
          self.printFileNames=True
        else:
          self.printFileNames=False

        try:
          os.makedirs(self.folderPathOutput,0o777)
        except:1

    def run(self):
        for root, dirs, files in os.walk(self.folderPathSource):
            for filename in files:
                try:
                    self.move(root,filename)
                except:1
    def move(self,rootPath,file):
        year=file[:4]
        month=file[4:6]

        previousPath=rootPath + "/" + file

        if "2000"<= year and year<="2030" and "01"<=month and month<="12":
            if self.printFileNames: print("OK",file)
            newFolderPath=self.folderPathOutput + "/" + year + "/" + month + "/"
        else:#invalid filename
            if self.printFileNames: print("NO",file)
            newFolderPath=self.folderPathOutput + "/Invalid/"

        try:
            os.makedirs(newFolderPath,0o777)
        except:1

        newPath=newFolderPath + file

        try:
            os.rename(previousPath, newPath)
        except:1


    def stop(self,msg=""):
        if msg!="": print(msg)
        exit(0)

    def help(self):
        print("")
        print("Usage: python main.py -sf sourceFolder [-df outputFolder]  [-print]")
        print("")
        print("Options:")
        print("    -sf path        Path of the source folder")
        print("    -df path        Path of the destination folder (Optional, by default it's the source folder)")
        print("    -print          Print all files moved (Optional)")
        print("")
        print("")
        exit(0)


if __name__ == '__main__':
    prog=program(sys.argv)
    prog.run()