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





def FilesCollector(path):
	"""
	Recives a path, and copies every file to a new folder called: FILESCOLLECTION
	"""
	try:

		# Create target Directory
		folderName = "FilesCollection"
		os.mkdir(folderName)
		print(folderName ,  "Folder Created", '\n Folder Name = "FilesCollection"') 
	except FileExistsError:
		print("Directory " , folderName ,  " already exists")
	
	if os.path.exists(folderName):

		for dirName, subdirs, fileList in os.walk(path):
			for filename in fileList:
				# Get file location//path
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





# POO Main 
if __name__ == '__main__':
	if len(sys.argv) > 1:
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
			Go = int(input("What you want to do? \n 1) Delete All of the Duplicates \n 2) Exit \n"))
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
			
		else:
			print('No duplicated files found... Byeeeee!')

	else:
		print('Usage: python "Python-FileAnalyzer.py" folder or folders to analyse.')
		






