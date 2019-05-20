#wikiti

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
 
    else:
        print('No duplicate files found.')

# Save dictionary on log.txt (file in main folder)

def logArchive(dictio):
	dictio = {'dictio': dictio}
	with open('log.txt', 'w') as file:
		file.write(json.dumps(dictio))


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
        outPutResults(duplicated)
        print('Log archive in main directory, saved as log.txt. ')
        logArchive(duplicated)
    else:
        print('Usage: python archive.py folder or folders to analyse.')







