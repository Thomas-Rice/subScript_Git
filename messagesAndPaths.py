
class messagesAndPaths:
	def __init__(self):
		self.message_dictionary = {}
		self.paths = {}


		self.error_messages()
		# self.paths()

	def error_messages(self):
		''' 
			Set Error messages
		'''

		self.message_dictionary['No_Jenkins_Connection'] = 'Cannot Connect to Jenkins, \n Please Check Connection'
		self.message_dictionary['Cannot_Find_New_Product'] = 'If you have added a new product, \n please check the name is correct (This is case sensitive)'

	def return_error_messages(self,key):
		'''
			Returns the desired message
		'''
		return self.message_dictionary[key]

	def paths(self):
		# '''
		# 	Set paths
		# '''
		# self.paths['run_builds_path'] = 'ToM'
		pass
	
	def return_paths(self,key):
		'''
			Returns the desired paths
		'''
		return self.message_dictionary[key]