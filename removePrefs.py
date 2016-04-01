import os
import platform
import sys
import shutil
import getpass


class removePrefs:
	def __init__(self, product,specific_project, footwearPath = None):
		self.prefs = ''
		self.prefsPath = ''
		self.jootaDir = ''
		self.dirPath = ''
		self.settingsPath = ''
		self.prefsList = []
		self.user = os.path.expanduser("~")
		self.localOS = platform.system()

		#Choose product
		if product == "Modo":
			if 'Joota' in specific_project:
				#Folder to delete
				self.jootaDir = 'Joota'
			self.footwearPath = footwearPath
			self.Modo_Delete('luxology')

		elif product == 'Mari':
			self.Mari_Delete()

		elif product == "Nuke":
			self.delete('nuke')
		elif product == "Katana":
			self.delete('katana')
		else:
			pass


	def Modo_Delete(self,files_to_delete):
		self.prefs = []
		#Windows 
		if self.localOS == 'Windows':
			self.prefs = 'JOOTA901.CFG'
			self.prefsPath = '{}\AppData\Roaming\Luxology\{}'.format(self.user, self.prefs)
			self.prefsList.append(self.prefsPath)

			if self.footwearPath != '':
				self.settingsPath = '{}\Settings\Modo\mAdiGlobalSettings.py'.format(self.footwearPath)
				self.prefsList.append(self.settingsPath)

			self.dirPath = '{}\AppData\Roaming\Luxology\{}'.format(self.user, self.jootaDir)
		
		#Mac
		elif self.localOS == 'Darwin' or self.localOS == 'MacOS':
			#Get user name
			prefs_path = "/Users/{}/Library/Preferences".format(getpass.getuser())
			# find all the files in this directory that contain the word luxology
			files_list = self.get_files_in_dir(files_to_delete,prefs_path)

			# append filepath strings to a list for deletion
			for pref in files_list:
				self.prefsPath = '{}/Library/Preferences/{}'.format(self.user, pref)
				self.prefsList.append(self.prefsPath)

			if self.footwearPath != '':
				self.settingsPath = '{}/mAdiGlobalSettings.py'.format(self.footwearPath)
				self.prefsList.append(self.settingsPath)

			self.dirPath = '{}/Library/Preferences/{}'.format(self.user, self.jootaDir)

		#Get files and delete them ALLLL!!!
		self.delete_files(self.prefsList)
		self.delete_folder(self.dirPath)

	def Mari_Delete(self):
		if self.localOS == 'Windows':
			prefs_path = 'C:/Users/{}/.mari/TheFoundry'.format(self.user)
		elif self.localOS == 'Darwin' or self.localOS == 'MacOS':
			prefs_path = os.path.join(self.user,'.config/TheFoundry')
		elif self.localOS == 'Linux':
			prefs_path = '~/.config/TheFoundry'
		
		self.delete_folder(prefs_path)


	def get_files_in_dir(self,search_term,prefs_path):
		prefs = []
		for preference in os.listdir(prefs_path):
			if search_term in preference:
				prefs.append(preference)
		return prefs

	def delete_files(self, prefs_list):
 		#Delete Prefs stored in the list
		for eachPref in prefs_list:
			if os.path.exists(eachPref):
				os.remove(eachPref)

	def delete_folder(self, path):
		if os.path.exists(path):
			shutil.rmtree(path)




if __name__ == "__main__":
    removePrefs = removePrefs('Mari','Joota_901stable','/Users/Tom/Desktop/Joota/Joota_Depot/Footwear/Settings/Modo')
