import sys, os, json
from lib.tools import *
from pymediainfo import MediaInfo

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
          self.stop("Error, -sf (source folder) is missing !")

        #the folder for output files
        if self.tool.argHasValue("-df"):
          val = self.tool.argValue("-df")
          self.destinationFolderPath = val.replace("\\","/")
        else:
          self.destinationFolderPath = self.sourceFolderPath
        os.makedirs(self.destinationFolderPath, 0o777, exist_ok = True)

        #print files moved
        if self.tool.argHasValue("-print"): #exists AND has value
            val = self.tool.argValue("-print")
            self.printFileInterval=int(val) #print each x files moved
            self.printFileNames=False
        elif self.tool.argExist("-print"): #exists but no value
            self.printFileInterval=-1
            self.printFileNames = True #print each file moved or not
        else: #doesnt exists
            self.printFileInterval=1000
            self.printFileNames = False #print nothing

        #flat : all in one folder
        self.flat = self.tool.argExist("-flat")

        #sort by day
        self.day = self.tool.argExist("-day")

        #ask for verification before moving files
        #self.ask = not self.tool.argExist("-y") #TODO

        #skip already scanned folders
        self.scanAll = not self.tool.argExist("-fast")

        #use exif data instead of filename
        self.exif = self.tool.argExist("-exif")

    def run(self):
        valid=0
        invalid=0

        print("Working...")
        for element in os.listdir(self.sourceFolderPath):
            path=os.path.join(self.sourceFolderPath,element)
            if os.path.isfile(path): #is a file
                try: #move it
                    self.move(self.sourceFolderPath, element)
                    if ((self.printFileInterval !=-1) and ((valid % self.printFileInterval)==0)):
                        print("{} files moved".format(valid))
                    valid += 1
                except: 
                    print("Error 1 with file", path)
                    invalid += 1
            else:#if folder
                if self.scanAll:
                    scanThisFolder=True
                else:
                    if element.isnumeric():
                        date=int(element)
                        if 1900<=date and date<=2099:#valid date -> already organized
                            print("Skipping folder", element)
                            scanThisFolder=False
                        else:
                            scanThisFolder=True
                    else:#not numeric
                        scanThisFolder=True

                if scanThisFolder:
                    for root, dirs, files in os.walk(path):

                        for filename in files:
                            try: #move it
                                self.move(root,filename)
                                if ((self.printFileInterval !=-1) and ((valid % self.printFileInterval)==0)):
                                    print("{} files moved".format(valid))
                                valid += 1
                            except: 
                                print("Error 2 with file", root + "/" + filename)
                                invalid += 1                        

        print("{} file.s moved ({} error.s)".format(valid,invalid))
        if invalid !=0 : print("There was error, please retry the same command")
        
    def getDate(self,file):
        media_info = MediaInfo.parse(file, output="JSON")
        data = json.loads(media_info)["media"]["track"][0]["File_Modified_Date_Local"]
        return data

    def move(self,rootPath,file):
        try:
            assert not self.exif

            #model 20200425_123551.jpg
            #      YYYYMMDD_HHMMSS.ext
            year = file[:4]
            month = file[4:6]
            day = file[6:8]

            assert self.validDate(year,month,day)
        except:
            #model 2020-12-07 16:36:47.729
            #      YYYY-MM-DD HH:MM:SS.MS
            data = self.getDate(rootPath+"/"+file)
            year = data[:4]
            month = data[5:7]
            day = data[8:10]

            #if yearExif == year and monthExif == month and dayExif == day:

        sourcePath = rootPath + "/" + file
        destinationPath = self.destinationFolderPath

        if self.validDate(year,month,day):
            if self.printFileNames: print("OK", file)

            if self.flat:
                destinationPath += "/" + year + "-" + month + "-" + day + "/"
            else:
                destinationPath += "/" + year + "/" + month + "/"
                if self.day: destinationPath += day + "/"

        else:#invalid filename
            if self.printFileNames: print("NO",file)
            destinationPath += "/InvalidNames/"

        os.makedirs(destinationPath, 0o777, exist_ok = True)

        destinationFilePath = destinationPath + file

        try: os.rename(sourcePath, destinationFilePath) #we move the file
        except: 
        	print("Error with file",sourcePath) #cannot move file, or file already exists
        	assert False
            
    def validDate(self,year,month,day):
        return ("1950" <= year and year <= "2050") and ("01" <= month and month <= "12") and ("01" <= day and day <= "31")

    def stop(self, msg = ""):
        if msg != "": print(msg)
        self.help()
        exit(0)#stop the program

    def help(self):
        print("")
        print("Usage: python dcimo.py -sf sourceFolder [-df outputFolder]")
        print("                       [-print] [-day] [-fast]")
        print("")
        print("Options:")
        print("    -sf path        Path of the source folder")
        print("    -df path        Path of the destination folder (Optional, by default it's the source folder)")
        print("    -print x        Print a counter each x files moved (Optional, by default set to 1000).")
        print("                    If no x is specified, print all file's names.")
        print("    -day            Separate files by day (Optional)")
        print("    -fast           Skip already organized folders (Optional)")
        print("")
        print("")
        exit(0)


if __name__ == '__main__':
    prog = program(sys.argv)
    prog.run()