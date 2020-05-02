# DCIMO(rganizer)
This program will organize photos and videos according to the date in the filename. For example 20200425_123551.jpg will be moved in the folder 2020/04/. Or in 2020/04/25/ if the -day flag is provided.

	Usage: python dcimo.py -sf sourceFolder [-df outputFolder]  [-print [x]]  [-day]

	Options:

		-sf path	Path of the source folder

		-df path	Path of the destination folder (Optional, by default it's the source folder)

		-print x	Print a counter each x files moved (Optional, by default set to 1000 if no flag). 
			If no x is specified, print all file's names.

		-day		Separate files by day (Optional)
