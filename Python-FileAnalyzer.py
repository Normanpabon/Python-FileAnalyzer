#wikiti

import os, sys, hashlib, json, shutil


# The blocks reffers to a part of the file thats going to be read, and get hash calculation
def hashCalculator(location, blocks = 131072):
	nfile = open(location, 'rb')
	# Uses Sha1 as a hash metod
	metod = hashlib.sha1()
	buf = nfile.read(blocks)
	while len(buf) > 0:
		metod.update(buf)
		buf = nfile.read(blocks)
	nfile.close()
	return metod.hexdigest()


# Look and hash files in the selected folder
def duplicatedFiles(Folder):
	# Created a empty dictionary to save the duplicated files
	duplicated = {}
	for dirName, subdirs, fileList in os.walk(Folder):
		# Prints the directory that is getting scanning 
		print("Parsing %s..." % dirName)
		for filename in fileList:
			# Get file location//path
			location = os.path.join(dirName, filename)
			# Get file hash
			fileHash = hashCalculator(location)
			# Add or append th file 
			if fileHash in duplicated:
				# Appends the hashfile and location, to the dictionary if duplicated
				duplicated[fileHash].append(location)
			else:
				duplicated[fileHash] = [location]

	return duplicated



# Unites dictionaries
def uniteDict(dictA, dictB):
	for key in dictB.keys():
		if key in dictA:
			dictA[key] = dictA[key] + dictB[key]
		else:
			dictA[key] = dictB[key]


def outPutResults(dictA):
	results = list(filter(lambda x: len(x) > 1, dictA.values()))
	if len(results) > 0:
		print('Duplicates Found:', '\n')
		print('The following are the same, even if the name is different: ', '\n')
		print('**********************')
		for result in results:
			for subresult in result:
				print('\t\t%s' % subresult)
			print('**********************')
		return True
	else:
		return False
	

# Save dictionary on log.txt (file in main folder)

def logArchive(dictio):
	dictio = {'dictio': dictio}
	with open('log.txt', 'w') as file:
		file.write(json.dumps(dictio))



def fileTypes():
	# Predefines files extension List's
	# Documents
	docFiles = ('.txt', '.docx', '.doc', '.pdf')
	# Images
	imagFiles = ('.png', '.gif', '.jpg', '.jpge')
	# Audio
	audFiles = ('.mp3', '.wma', '.flac', '.acc', 'm4a', '.ogg')
	# Video
	vidFiles = ('.mp4', '.wmv', '.mov', '.m4v', '.flv', '.mpg', '.avi' ) 
	# Custom list with specific extencions gived by the user
	customFiles = [] 

	print("Please select the archives that you want to copy. \n")
	print("1) Doc files (txt, docx, doc, pdf). \n",	"2) Images files (png, gif, jpg, jpge). \n", "3) Audio files (mp3, wma, flac...). \n", "4) Video files (mp4, wmv, mov...). \n", "5) Custom files extension.")
	x = int(input(""))
	# no finished, use a for plox
	if (x > 0) and (x < 7):
		if (x == 1):
			return docFiles
		elif (x == 2):
			return imagFiles
		elif (x == 3):
			return audFiles
		elif (x == 4):
			return vidFiles
		elif (x == 5):
			print("Please write the type of files you want. ### INSIDE singles quotes! ### eg: '.bat','.iso','.wav'\n")
		
################################################
################################################
################################################
################################################
			################################################
################################################
################################################
			ownFiles= input(":")
			print(ownFiles)
			return ownFiles
		else:
			print("how did you get here ?")

		print("wikiti")
		#add for to get all elements in the list 
	else:
		print("Select a valid option. \n")
		return fileTypes()




def FilesCollector(path):



	"""
	Recives a path, and copies every file to a new folder called: FILESCOLLECTION
	"""
	try:

		# Create target Directory
		folderName = "FilesCollection"
		os.mkdir(folderName)
		print(folderName ,  "Folder Created", '\n Folder Name = "FilesCollection"\n') 
	except FileExistsError:
		print("Directory " , folderName ,  " already exists \n")
	
	if os.path.exists(folderName):
		
		fTypes = int(input("Do you want to copy every type of file? \n 1)Yes \n 2)No \n:"))

		if fTypes == 2:
			filestypes = fileTypes()

		for dirName, subdirs, fileList in os.walk(path):
			for filename in fileList:

				if fTypes == 2:

					if filename.endswith(filestypes):
					# The endswith works with a parameter like ('.txt','.wav'). The parenthesis and sigle quotes are mandatory.
					# That's why we have to use tuples, because tuples are like ('','','').
					  
						# Get file location//path
						location = os.path.join(dirName, filename)
						print("This archive is going to be copied: ")
						print(location)
						print('\n')
						try:
							shutil.copy2(location, folderName)
						except OSError as e:
							print(f'Error: {location} : {e.strerror}')
				
				if fTypes == 1:

					location = os.path.join(dirName, filename)
					print("This archive is going to be copied: ")
					print(location)
					print('\n')
					try:
						shutil.copy2(location, folderName)
					except OSError as e:
						print(f'Error: {location} : {e.strerror}')

def Incinerate(path):
	"""
	Recives a path, and erase the archive in that path
	"""	
	print("This archive is going to be deleted: ")
	print(path)
	print('\n')
	try:
		os.remove(path)
	except OSError as e:
		print(f'Error: {path} : {e.strerror}')


def TurnOnIncinerator(dic):
	"""
	Erase everything but the first file of each duplicate in the dictionary
	"""
	filesLeft = {}
	dic = list(dic.values())
	for Duplicate_files in dic:
		for file in Duplicate_files[1:]: 
			#The for starts after the first item duplicated.
			Incinerate(file)

	print("That's All of your Trash...\n")


def menu():
	print("wikitiki")
	duplicated = {}
	folders = sys.argv[1:]
	for i in folders:
		# Iterate the folders given
		if os.path.exists(i):
		# Find the duplicated files and append them to the dictionary
			uniteDict(duplicated, duplicatedFiles(i))
		else:
			print('%s is not a valid path, please verify' % i)
			sys.exit()
	if outPutResults(duplicated):
		Go = int(input("What you want to do? \n 1) Delete All of the Duplicates \n 2) Start the file collector without deleting the duplicates! \n 3) Exit \n"))
		if Go == 1:
			TurnOnIncinerator(duplicated)

			print('Log archive in main directory, saved as log.txt. ')
			logArchive(duplicated)
				
			#conditional to copy the archives to a new folder
			#opt == option choosed by the user
			opt = 0 
			while opt != 1 or opt != 2:
				opt = int(input("Do you want to copy the archives to a new folder ? \n 1) Yes \n 2) No, exit. \n Option = "))
				if opt == 1:
					for i in folders:
						#This copies the remain archives to a new folder 
						FilesCollector(i)
				else:
					print("Bye.")
					sys.exit()
		if Go == 2:
			for i in folders:
				#This copies the remain archives to a new folder 
				FilesCollector(i)	
		else:
			print('No duplicated files found... Byeeeee!')

	else:
		print('\n', 'Usage: python "Python-FileAnalyzer.py" folder or folders to analyse.')
		



# POO Main 
if __name__ == '__main__':
	if len(sys.argv) > 1:
		menu()
		





