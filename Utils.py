import os,shutil,subprocess
from jenkinsBuild import *

class Utils:
	def __init__(self,productType,buildType,configuration):


		self.location = os. getcwd ()
		self.product_type = productType
		self.buildType = buildType
		self.product_folder_name = self.product_type + '_Builds'
		self.builds_folder_name = buildType + '_Builds'

		self.folderPath = os.path.join(self.location,self.product_folder_name,self.builds_folder_name)

		self.address = 'http://jenkinsii:8080/job/{}/lastSuccessfulBuild/{}/artifact/Archive.tgz'.format(buildType,configuration)



	def createLicense(self, buildNumber):
		'''
			Create a license for the current build
		'''

		licgen_folder = os.path.join(self.location,'Licensing','licgen')
		joota_license_folder = os.path.join(self.location,'Licensing','Joota_Licenses')
		# Change directory to the license generation folder
		os.chdir(licgen_folder)
		# Creates a variable for running the license tool
		self.fLicrun = os.path.join(licgen_folder,'licgen.sh')
		# Runs the license tool with the build number as a parameter
		subprocess.call([self.fLicrun, buildNumber])
		license = 'joota{}.lic'.format(buildNumber)
		original_location = os.path.join(licgen_folder,license)
		new_location = os.path.join(joota_license_folder,license)
		# Moves the license from the project folder to the selected destination
		shutil.move(original_location, new_location)

	def retrieveFromJenkins(self,userDefinedBuildNumber = None,version = None):
		import urllib



		os.chdir(self.location)
		fileName = '{}_Archive.tgz'.format(self.buildType)

		print 'Archive Files is....' +fileName

		#Delete Old Archives in this folder in order to make sure there is only one.
		if os.path.exists(self.location + fileName):
			os.remove(self.location + fileName)
			# print 'deleted old archive.tgz'
		else:
			pass


		lastSuccessfulBuild = urllib.URLopener()
		lastSuccessfulBuild.retrieve(self.address, fileName)
		return fileName


	def get_file_size(self,userDefinedBuildNumber = None,version = None):
		import urllib
		#Get the total file size of the 
		site = urllib.urlopen(self.address)
		meta = site.info()
		fileSize =  meta.getheaders("Content-Length") 
		return fileSize




	def getFolderList(self):

		''' 
			Search through your builds folder and populate a list so that the dropdown box has Content
		'''

		#create the folder path



		if not os.path.exists(self.folderPath):
			os.makedirs(self.folderPath)
		else:
			pass

		# Empty the list
		self.buildList = []
		# loop through all the folders within the folder Joota_Downloads and append them to the list self.buildList
		for file in os.listdir(self.folderPath):
			if file == '.DS_Store':
				pass
			else:
				self.buildList.append(file)

		# print self.buildList.sort(key = lambda x: os.stat(os.path.join(folderPath, x)).st_mtime)

		return self.buildList

	def runBuild(self,build):

		self.JootaCrashReportPath = os.path.join(self.folderPath,build,'joota.app','Contents','MacOS','joota')
		# Create the extension beacuse subprocess says so.... 
		extension = '-dboff:crashreport'
		#Run Joota with crash report 
		subprocess.Popen([self.JootaCrashReportPath, extension])


	def handle_download(self):
		downloaded_file_name=self.retrieveFromJenkins()
		jenkins_build = jenkinsBuild(self.location,downloaded_file_name,self.folderPath,self.buildType)
		build_number = jenkins_build.stableMoveAndExtract()
		self.createLicense(build_number)


if __name__ == "__main__":
	util = Utils('Joota','Joota_901dev','FnMachineSpec=meerman,FnOptType=release,FnProductLabel=Joota')
	# util.get_file_size()
	# util.getFolderList()
	# util.retrieveFromJenkins()
	# util.runBuild()UNTESTED
	util.handle_download()

