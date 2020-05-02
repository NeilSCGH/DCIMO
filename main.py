import sys
import os
from lib.tools import *

class program():
	def __init__(self,args):
	    self.tool = tools(args)
	    self.setup(args)

	def setup(self,args):
	    if self.tool.argHasValue("-f"):#the folder for source files
	      val=self.tool.argValue("-f")
	      self.folderPath=val.replace("\\","/")
	      print("folderPath",self.folderPath)
	    else:
	      self.stop("Error, -f is missing !")

	def run(self):
		for root, dirs, files in os.walk(self.folderPath):
		    for filename in files:
		    	try:
		    		self.move(filename)
		    	except:1
	def move(self,file):
		year=file[:4]
		month=file[4:6]

		if "2000"<= year and year<="2030" and "01"<=month and month<="12":
			print("OK",file)
			previousPath=self.folderPath + "/" + file
			newFolderPath=self.folderPath + "/" + year
			try:
				os.mkdir(newFolderPath,0o777)
			except:1
			newFolderPath += "/" + month + "/" 
			try:
				os.mkdir(newFolderPath,0o777)
			except:1

			newPath=newFolderPath + file

			os.rename(previousPath, newPath)
		else:
			print("NO",file)


	def stop(self,msg):
		print(msg)
		exit(0)


if __name__ == '__main__':
	prog=program(sys.argv)
	prog.run()