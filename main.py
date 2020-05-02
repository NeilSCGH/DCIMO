import sys
import os
from lib.tools import *

class program():
    def __init__(self,args):
        self.tool = tools(args)
        self.setup(args)#process the arguments

    def setup(self,args):
        #Help
        if self.tool.argExist("-h") or self.tool.argExist("-help"):
          self.help()

        #the folder for source files
        if self.tool.argHasValue("-sf"):
          val = self.tool.argValue("-sf")
          self.sourceFolderPath = val.replace("\\","/")
        else:
          self.stop("Error, -sf (source fold) is missing !")

        #the folder for output files
        if self.tool.argHasValue("-df"):
          val = self.tool.argValue("-df")
          self.destinationFolderPath = val.replace("\\","/")
        else:
          self.destinationFolderPath = self.sourceFolderPath
        os.makedirs(self.destinationFolderPath, 0o777, exist_ok = True)

        #print all files moved
        self.printFileNames = self.tool.argExist("-print")

    def run(self):
        valid=0
        invalid=0

        print("Working...")

        for root, dirs, files in os.walk(self.sourceFolderPath):
            for filename in files:
                try: 
                    self.move(root,filename)
                    valid += 1
                except: 
                    print("Error with file",previousPath)
                    invalid += 1

        print("{} file.s moved ({} error.s)".format(valid,invalid))

    def move(self,rootPath,file):
        #model 20200425_123551.jpg
        #      YYYYMMDD_HHMMSS.ext
        year = file[:4]
        month = file[4:6]

        sourcePath = rootPath + "/" + file
        destinationPath = self.destinationFolderPath

        if "1950" <= year and year <= "2050" and "01" <= month and month <= "12":
            if self.printFileNames: print("OK",file)
            destinationPath += "/" + year + "/" + month + "/"

        else:#invalid filename
            if self.printFileNames: print("NO",file)
            destinationPath += "/Invalid/"

        os.makedirs(destinationPath, 0o777, exist_ok = True)

        destinationFilePath = destinationPath + file

        try: os.rename(sourcePath, destinationFilePath) #we move the file
        except: print("Error with file",sourcePath) #cannot move file, or file already exists
            

    def stop(self, msg = ""):
        if msg != "": print(msg)
        exit(0)#stop the program

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
    prog = program(sys.argv)
    prog.run()