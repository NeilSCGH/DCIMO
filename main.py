import sys
import os
from lib.tools import *

class program():
    def __init__(self,args):
        self.tool = tools(args)
        self.setup(args)

    def setup(self,args):
        if self.tool.argHasValue("-sf"):#the folder for source files
          val=self.tool.argValue("-sf")
          self.folderPathSource=val.replace("\\","/")
        else:
          self.stop("Error, -sf (source fold) is missing !")

        if self.tool.argHasValue("-of"):#the folder for output files
          val=self.tool.argValue("-of")
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


    def stop(self,msg):
        print(msg)
        exit(0)


if __name__ == '__main__':
    prog=program(sys.argv)
    prog.run()