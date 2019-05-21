#wikiti




# borrar automaticamente duplicados (si el usuario asi lo desea).
# Traer todos los archivos de las subcarpetas a una carpeta raiz.
# que el log quede organizado y contenga la lista solamente de los archivos duplicados
# Traer todos los archivos de las subcarpetas a una carpeta raiz. (esto colocar luego 
# 	la opcion de que tipos de archivo desea)
# que al final del programa, despues que termine el análisis, diga: 
# si es posible el peso total de los archivos analizados, el peso de los 
# archivos duplicados. cuantos archivos sea analizaron y cuantos estan duplicados.
#  si vas a hacer, empeza con el primero papi y asi bajando.
# Luego podemos tirar un "branch", que se llame "Master-gui" y una interfaz 
# de usuario suavelan hecha en tkinter. asi dejamos una version hecha en consola y otra en gui.
#  y con eso dejamos suspendido ese proyecto,  luego le implementamos mas cosas.
#   de alli pasamos a hacer el bicho para windows, para limpiar registros.









import os, sys, hashlib, json


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
		print("Looking %s..." % dirName)
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

	print("That's All your Trash...\n")



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
		else:
			print('No duplicate files found... Byeeeee!')

	else:
		print('Usage: python archive.py folder or folders to analyse.')







