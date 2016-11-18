import os
import shutil

class jenkinsBuild:
	def __init__(self, location, fileName, folderPath, buildType,buildNumber, integrationLocation = None):

		self.location = location
		self.buildNumber = buildNumber
		# self.product_type = productType
		# self.builds_folder_name = self.product_type + '_Builds'

		self.archive_file = fileName
		self.file_location = os.path.join(self.location,fileName)
		self.folder_name = buildType + '_Builds'
		self.tmpFolder = os.path.join(folderPath,'tmp')
		self.Type = buildType
		self.folder_build_type_path = folderPath

	def MoveAndExtract(self):	
		import tarfile	

		#Delete Any pre exisitng tmp folders
		if os.path.exists(self.tmpFolder):
			#delete new folder as you already have the build
			shutil.rmtree(self.tmpFolder, ignore_errors=True)

		if os.path.exists(self.file_location):
			#Make temp folder to put archive in
			os.makedirs(self.tmpFolder);
			#Move the .tgz to the new folder
			shutil.move(self.file_location, self.tmpFolder)
			#Change to the directory
			os.chdir(self.tmpFolder)
			#open the .tgz file
			self.tfile = tarfile.open(self.archive_file)
			#extract all
			self.tfile.extractall()
			#close the operation 
			self.tfile.close()


			newFolderPath = os.path.join(self.folder_build_type_path,self.buildNumber)

			#Move back into the folder directory so we can rename it to that of the build number
			os.chdir(self.location)
			#Rename the folder from stable to stable_buildName
			os.rename(self.tmpFolder , newFolderPath)
			# print 'Unpacked your build'

		else:
			# #If the file does not exist in your downloads then print out this message on the Gui
			print("No compressed file with the name \" Archive.tgz \" in your downloads directory...No action taken ")

		return self.buildNumber

	# def integrationMoveAndExtract(self,filePath,folderName):

	# 	compressionType = filePath[-4:]

	# 	buildPath = os.path.join(self.location, self.builds_folder_name, 'Integration_Builds')
	# 	self.fileName = os.path.basename(filePath)
	# 	self.newFolderPath = os.path.join(buildPath,folderName)
	# 	#Make sure the folder to be created does not exist and if it does check if there is a .ds_store in it, then get rid of that.
	# 	if os.path.exists(self.newFolderPath):
	# 		if len(self.newFolderPath) >0:
	# 			emptyFolder = os.listdir(self.newFolderPath)
	# 			if len(emptyFolder) == 0:
	# 				shutil.rmtree(self.newFolderPath, ignore_errors=True)
	# 			if len(emptyFolder) == 1 and emptyFolder[0] == '.DS_Store':
	# 				shutil.rmtree(self.newFolderPath, ignore_errors=True)
	# 			else: 
	# 				pass
	# 		else:
	# 			pass
	# 	else:
	# 		pass
	# 	#Make Stable folder to put archive in
	# 	os.makedirs( self.newFolderPath );

	# 	shutil.move(filePath, (self.newFolderPath))
	# 	#Change to the directory
	# 	os.chdir(self.newFolderPath )

	# 	if compressionType == '.zip':
	# 		subprocess.call(['unzip', self.fileName])	
	# 	if compressionType == '.tgz':
	# 		import tarfile	
	# 		self.file = tarfile.open(self.fileName)
	# 		#extract all
	# 		self.file.extractall()
	# 		#close the operation
	# 		self.file.close()



if __name__ == "__main__":
	Stable = jenkinsBuild()
	Stable.retrieveFromJenkins()

