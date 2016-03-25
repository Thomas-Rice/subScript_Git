import os,shutil

class jenkinsBuild:
	def __init__(self, location, fileName, folderPath, buildType, integrationLocation = None):

		self.location = location
		self.buildNumber = ''
		# self.product_type = productType
		# self.builds_folder_name = self.product_type + '_Builds'

		self.archive_file = fileName
		self.file_location = os.path.join(self.location,fileName)
		self.folder_name = buildType + '_Builds'
		self.tmpFolder = os.path.join(folderPath,'tmp')
		self.Type = buildType
		self.folder_build_type_path = folderPath







	def stableMoveAndExtract(self):	
		import tarfile	

		#Delete Any pre exisitng tmp folders
		if os.path.exists(self.tmpFolder):
			#delete new folder as you already have the build
			shutil.rmtree(self.tmpFolder, ignore_errors=True)
		else:
			pass


		if os.path.exists(self.file_location):
			#Make Stable folder to put archive in
			os.makedirs( self.tmpFolder);
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


			#Get the build number from the plist in the extracted Joota app in order to rename the folder
			self.buildNumber = self.getBuildNumber()


			newFolderPath = os.path.join(self.folder_build_type_path, self.Type +'_' + self.buildNumber)

			if self.checkIfExists(newFolderPath):
				pass
			else:
				# #Move back into the folder directory so we can rename it to that of the build number
				os.chdir(self.location)
				#Rename the folder from stable to stable_buildName
				os.rename(self.tmpFolder , newFolderPath)

				# print 'Unpacked your build'

		else:
			# #If the file does not exist in your downloads then print out this message on the Gui
			# print("No compressed file with the name \" Archive.tgz \" in your downloads directory...No action taken ")
			pass

		return self.buildNumber

	def integrationMoveAndExtract(self,filePath,folderName):

		compressionType = filePath[-4:]

		buildPath = os.path.join(self.location, self.builds_folder_name, 'Integration_Builds')
		self.fileName = os.path.basename(filePath)
		self.newFolderPath = os.path.join(buildPath,folderName)
		#Make sure the folder to be created does not exist and if it does check if there is a .ds_store in it, then get rid of that.
		if os.path.exists(self.newFolderPath):
			if len(self.newFolderPath) >0:
				emptyFolder = os.listdir(self.newFolderPath)
				if len(emptyFolder) == 0:
					shutil.rmtree(self.newFolderPath, ignore_errors=True)
				if len(emptyFolder) == 1 and emptyFolder[0] == '.DS_Store':
					shutil.rmtree(self.newFolderPath, ignore_errors=True)
				else: 
					pass
			else:
				pass
		else:
			pass
		#Make Stable folder to put archive in
		os.makedirs( self.newFolderPath );

		shutil.move(filePath, (self.newFolderPath))
		#Change to the directory
		os.chdir(self.newFolderPath )

		if compressionType == '.zip':
			subprocess.call(['unzip', self.fileName])	
		if compressionType == '.tgz':
			import tarfile	
			self.file = tarfile.open(self.fileName)
			#extract all
			self.file.extractall()
			#close the operation
			self.file.close()


	def checkIfExists(self,newFolderPath):
		#If the folder already exists (this program has been run on this day) then it will not create a new folder.
		if os.path.exists(newFolderPath):
			tmp_file_path = os.path.join(self.tmpFolder,self.archive_file)
			#Move the archive out of the location so it doesn't get deleted
			shutil.move(tmp_file_path, self.location)	
			#delete new folder as you already have the build
			shutil.rmtree(self.tmpFolder, ignore_errors=True)
			# os.remove(self.tmpFolder)
			# print("You already have this build extracted in the correct place .... make sure that you're using the correct Archive.tgz")

			return True
		else:

			return False

	def getBuildNumber(self):
		import plistlib
		'''
			Reads the PList from the Joota build to determine the build number

			if darwin.....
		'''


		# Reads the plist build file an stores it in a dict
		self.my_plist = plistlib.readPlist(self.folder_build_type_path + '/tmp/joota.app/Contents/info.plist')
		# Searches through the dict for the CFBundleShortVersionString entry
		self.buildString = self.my_plist["CFBundleShortVersionString"]
		# Slices the line to the build number and removes the final character and stores it in the buildNumber variable
		self.buildNumber = self.buildString[4:-1]

		# print ('new folder build name is', self.buildNumber)
		return self.buildNumber









if __name__ == "__main__":
	Stable = jenkinsBuild()
	Stable.retrieveFromJenkins()

