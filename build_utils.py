import os
import shutil
import subprocess
import urllib
import sys
import json
from jenkinsBuild import *

class build_utils:
	def __init__(self,productType,buildType):
		self.location = os.getcwd ()
		self.product_type = productType
		self.buildType = buildType
		self.buildNumber = ''
		self.product_folder_name = self.product_type + '_Builds'
		self.builds_folder_name = buildType + '_Builds'
		configuration = self.decode_dictionary(productType,buildType)

		self.folderPath = os.path.join(self.location,self.product_folder_name,self.builds_folder_name)
		self.build_number_address = 'http://jenkinsii:8080/job/{}/lastSuccessfulBuild/{}'.format(buildType,configuration)		
		self.address = 'http://jenkinsii:8080/job/{}/lastSuccessfulBuild/{}/artifact/Archive.tgz'.format(buildType,configuration)

	def createLicense(self, buildNumber):
		'''
			Create a license for the current build
		'''

		licgen_folder = os.path.join(self.location,'Licensing','licgen')
		license_folder = os.path.join(self.location,'Licensing','{}_Licenses'.format(self.buildType))
		# Change directory to the license generation folder
		if not os.path.exists(license_folder):
			os.makedirs(license_folder)
		os.chdir(licgen_folder)

		# Creates a variable for running the license tool
		self.fLicrun = os.path.join(licgen_folder,'licgen.sh')
		# Runs the license tool with the build number as a parameter
		subprocess.call([self.fLicrun, buildNumber])
		license = 'joota{}.lic'.format(buildNumber)
		original_location = os.path.join(licgen_folder,license)
		new_location = os.path.join(license_folder,license)
		# Moves the license from the project folder to the selected destination
		shutil.move(original_location, new_location)

	def retrieveFromJenkins(self,userDefinedBuildNumber = None,version = None):
		os.chdir(self.location)
		fileName = '{}_Archive.tgz'.format(self.buildType)

		# print 'Archive Files is....' + fileName
		archive_to_be_deleted = os.path.join(self.location,fileName) 
		#Delete Old Archives in this folder in order to make sure there is only one.
		if os.path.exists(archive_to_be_deleted):
			os.remove(archive_to_be_deleted)
			# print 'deleted old archive.tgz'

		lastSuccessfulBuild = urllib.URLopener()
		lastSuccessfulBuild.retrieve(self.address, fileName)
		return fileName

	def get_file_size(self,userDefinedBuildNumber = None,version = None):
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

		# Empty the list
		self.buildList = []
		# loop through all the folders within the folder Joota_Downloads and append them to the list self.buildList
		for folder in os.listdir(self.folderPath):
			if folder == '.DS_Store':
				pass
			else:
				self.buildList.append(folder)

		return self.buildList

	def runBuild(self,selected_build):
		app = self.return_app_name(self.buildType)
		filename = os.path.join(self.folderPath,selected_build,app)

		if sys.platform == "Windows":
			os.startfile((filename+'.exe'))
		else:
			opener ="open" if sys.platform == "darwin" else "xdg-open"
			subprocess.call([opener, (filename+'.app')])

	def upack_Nuke(self):
		#unpack the dmg
		hdiutil attach -mountpoint "/Users/Tom/Downloads/Nuke" Nuke10.0v1.001291b-mac-x86-release-64.dmg
		cd Nuke10.0v1.001291b-mac-x86-release-64.pkg/Contents/
		#Unpack archive Archive.pax.gz
		


	def return_app_name(self,app_name):
		'''
			I HATE THiSS
		'''
		if 'Joota' in app_name:
			return 'Joota'
		elif 'Honda' in app_name:
			return 'Honda'
		elif 'Oakley' in app_name:
			return 'Oakley'
		elif 'Katana' in app_name:
			return 'Katana'
		elif 'Mari' in app_name:
			return 'Mari'
		elif 'Nuke' in app_name:
			return 'Nuke'

	def checkIfExists(self,folder_name):
		#If the folder already exists (this program has been run on this day) then it will not create a new folder.
		if os.path.exists(folder_name):
			return True
		else:
			return False

	def getBuildNumber(self):
		'''
			Read the build number from the jenkins API

		'''
		self.product_url = self.build_number_address + '/injectedEnvVars/api/json'
		response = urllib.urlopen(self.product_url)
		output = json.loads(response.read())

		self.buildNumber = output['envMap']['BUILD_NUMBER']
		self.path = os.path.join(self.folderPath,self.buildNumber)
		return self.buildNumber

	def decode_dictionary(self,product,build):
		#Load original dictionary
		with open('jenkins_Builds.json') as in_file:
			original_dict = json.load(in_file)
		#Load new dictionary with chosen products in it
		with open('subScript_generator.json') as data_file:
			product_list = json.load(data_file)

		configuration = product_list['generator'][product][build]
		configuration_address = original_dict[product][build][configuration]
		return configuration_address 


	def handle_download(self):
		self.getBuildNumber()
		if self.checkIfExists(self.path) == True:
			pass
		else:
			self.createLicense(self.buildNumber)
			downloaded_file_name = self.retrieveFromJenkins()
			jenkins_build = jenkinsBuild(self.location,downloaded_file_name,self.folderPath,self.buildType,self.buildNumber)
			jenkins_build.MoveAndExtract()



if __name__ == "__main__":
	util = build_utils('Modo','Joota_901stable')
	# util.get_file_size()
	# util.getFolderList()
	# util.retrieveFromJenkins()
	# util.runBuild()UNTESTED
	# util.handle_download()
	# util.runBuild('601')
	# util.getBuildNumber()
	# util.runBuild('/Users/Tom/Desktop/SupaScript_V1.1_For_Me/Joota_Builds/Stable_Builds/Stable_594','Joota.app')

