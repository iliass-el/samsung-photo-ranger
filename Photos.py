import os, re, argparse
from shutil import copy2, move


def TraverseAndOrder(dirPath, args): 
	listOfFiles = os.listdir(dirPath)
	#Create log file
	if args.log:
		log = open("log.txt","a")
		log.write("###############################################\n")

	for filename in listOfFiles:
		# Create full path
		fullPath = os.path.join(dirPath, filename)
		# If fullPath is a directory then get the list of files in this directory
		if os.path.isdir(fullPath):
			FolderName = os.path.basename(fullPath)
			m = re.match(r'20\d{2}$', FolderName)
			#Check if it's not already sorted
			if m == None:
				TraverseAndOrder(fullPath, args)				
		else:
			#If a file
			#check pattern : extract date from image Name
			m = re.search(r'20\d{2}', filename)

			if m != None:
				#Create folder (20**) 
				DistDirName = os.path.join(dirPath,m.group(0))
				
				if not os.path.exists(DistDirName):
					try:
						os.mkdir(DistDirName)
						if args.log:
							log.write("\nCreating Folder {0}\n".format(os.path.basename(DistDirName)))
					except:
						log.write("Error while creating folder {0}.\n".format(DistDirName))
						print("Error while creating folder {0}.\n".format(DistDirName))

				#move the file to folder (20**)
				old = os.path.join(fullPath)
				new = os.path.join(dirPath, DistDirName, filename)
				try:
					move(old, new)
					if args.log:
						log.write("Moving File {0} ----> {1}\n".format(old, new))
				except:
					log.write("An Error while moving file {0} ----> {1}\n".format(old, new))
					print("An Error while moving file {0} ----> {1}\n".format(old, new))
	if args.log:
		log.close()

def merge(rootPath, args):
	if args.log:
		log = open('log.txt', 'a')
	
	#Get Sub Folders	
	SubFolders = [e[0] for e in os.walk(rootPath)]

	for folder in SubFolders:
		extractFolderName = os.path.basename(folder)
		#if folder already exist in root directory then move file to that folder
		if re.match(r'(^20\d{2}$)', extractFolderName) != None:
			DistinationFolder = os.path.join(rootPath, extractFolderName)
			if os.path.isdir(DistinationFolder):
				#if folder exist in root folder then copy/replace content to the same folder
				for filename in os.listdir(folder):
					old = os.path.join(folder,filename)
					new = os.path.join(DistinationFolder,filename)
					
					try:
						os.rename(old, new)
					except FileExistsError:
						log.write("File {0} already Exist in folder {1}\n".format(old, new))

					if args.log:
						log.write("Merge: moving file {0} ----> {1}\n".format(folder, DistinationFolder))
 
			else:
				#otherwise move folder to the root directory
				try:
					move(folder, DistinationFolder)
					if args.log:
						log.write("Merge : Moving Folder {0} ----> {1}\n".format(filename, DistinationFolder))
				except:
					#print("Error while moving Folder {0} to root folder {}\n".format(e, DistinationFolder))
					log.write("Error while moving folder {0} ----> {1}\n".format(DistinationFolder, rootPath))
	if args.log:
		log.close()

def main():
	usage = '''
		path 	: -p for the path
		stream 	: live console message for live moving files
		ignore 	: Create "Unkown Folder" || let images in their folders
		replace : When merging if the folder contains the same name replace it
		copy 	: just copy files let's the original files
		merge 	: "Merge Folders"
		log 	: Save log to txt file
	'''
	parser = argparse.ArgumentParser()

	parser.add_argument('-p', '--path', help='specifie the images path.', required=True)
	#parser.add_argument('-s', '--stream', help='print the current action on console	', action="store_true")
	#parser.add_argument('-i', '--ignore', help='Create "Unknown" Folder || keep unrecognized images in their folders', action="store_true")
	#parser.add_argument('-r', '--replace', help='When merging if the folder contains the same name replace it', action="store_true")
	#parser.add_argument('-c', '--copy', help='just copy files lets the original files', action="store_true")
	parser.add_argument('-m', '--merge', help='Merge Folders with same date.', action="store_true")
	parser.add_argument('-l', '--log', help='Generate Log file.', action="store_true")
	args = parser.parse_args()

	path = args.path
	try:
		if(os.path.isdir(path)):
			TraverseAndOrder(path, args)
	except:
		print("Specfie a valid path.\n")
	
	if args.merge:
		merge(path, args)


if __name__ == "__main__":
	main()
	print("Done.")