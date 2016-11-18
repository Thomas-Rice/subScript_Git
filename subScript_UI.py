import sys
import json

from removePrefs import *
from build_utils import *
from PySide import QtCore, QtGui



class change_list_widget(QtGui.QWidget):
	def __init__(self,parent = None):
		super(change_list_widget, self).__init__(parent)

		self.change_list = ['jsdlkjflksdjflksdjklfjsdklfjslkjflkejflksjflkjselkjfeslkjflksjklfjlknvlknkjjlvehrkgjhskjhfskjhgkdfhgkjdhfkjghdfjkgh','ksdfkjsdkjhfkjsdhfkjsdhkfjhskfbsjhjhsgjfgsldgfsdgkfgsdklhfg']
		self.create_widgets()
		self.create_layout()

	def create_widgets(self):
		self.scroll = QtGui.QScrollArea()
		self.list_layout = QtGui.QListWidget(self)

		for name in self.change_list:
			self.list_layout.addItem(name)

		self.scroll.setWidget(self.list_layout)
		self.scroll.setWidgetResizable(True)

	def create_layout(self):
		main_layout = QtGui.QVBoxLayout()
		main_layout.addWidget(self.scroll)
		main_layout.setContentsMargins(0,3,0,8)
		self.setLayout(main_layout)

	def create_connections(self):
		value = self.list_layout.currentItem()
		print value.text()


class build_list_widget(QtGui.QWidget):
	selected_item = QtCore.Signal(str)
	def __init__(self,build_utils_object, parent = None):
		super(build_list_widget, self).__init__(parent)

		self.checkbox_list = build_utils_object.getFolderList()

		self.create_widgets()
		self.create_connections()
		self.create_layout()

	def create_widgets(self):
		self.scroll = QtGui.QScrollArea()
		self.list_layout = QtGui.QListWidget(self)

		for name in self.checkbox_list:
			self.list_layout.addItem(name)

		self.scroll.setWidget(self.list_layout)
		self.scroll.setWidgetResizable(True)

	def create_layout(self):
		main_layout = QtGui.QVBoxLayout()
		main_layout.addWidget(self.scroll)
		main_layout.setContentsMargins(0,3,0,8)
		self.setLayout(main_layout)

	def create_connections(self):
		self.list_layout.currentItemChanged.connect(self.return_value)

	def return_value(self):
		value = self.list_layout.currentItem().text()
		self.selected_item.emit(value)
		print value


class productButtonLayout(QtGui.QWidget):
	layout_changed = QtCore.Signal(str)
	button_pressed = QtCore.Signal()
	def __init__(self, numbers, parent = None):
		super(productButtonLayout, self).__init__(parent)

		self.numbers = numbers

		# print numbers

		self.create_widgets()
		self.create_layout()
		self.create_connections()

	def create_widgets(self):
		self.button = []
		self.buttonContainer = QtGui.QWidget(self)
		buttonLayout = QtGui.QVBoxLayout()

		#Create as many pushbuttons as there are products
		for index, number in enumerate(self.numbers):
			# print number
			self.button.append(QtGui.QPushButton(number))
			buttonLayout.addWidget(self.button[index])

		self.buttonContainer.setLayout(buttonLayout)
		self.change_list_checkbox = QtGui.QCheckBox('Show Changelist')

	def create_layout(self):
		main_layout = QtGui.QVBoxLayout()
		main_layout.setContentsMargins(0,0,0,0)
		main_layout.addWidget(self.buttonContainer)
		main_layout.addWidget(self.change_list_checkbox)
		self.setLayout(main_layout)

	def create_connections(self):
		# Create as many connections as there are product buttons
		for item in range(0,len(self.numbers)):
			self.button[item].clicked.connect(lambda text = "{}".format(item): self.output(text))
		self.change_list_checkbox.clicked.connect(self.emit_sig)

	def output(self,number):
		self.layout_changed.emit(number)


	def emit_sig(self):
		self.button_pressed.emit()



class section1Layout(QtGui.QWidget):
	def __init__(self, build_utils_object, parent = None):
		super(section1Layout, self).__init__(parent)
		#Create Utils instance for each product and build 
		self.build_utils = build_utils_object

		self.create_widgets()
		self.create_layout()
		self.create_connections()

	def create_widgets(self):
		self.get_build_button = QtGui.QPushButton('Get Last Successful \n Build From Jenkins')
		self.get_build_button.setSizePolicy (QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

		self.progressbar = QtGui.QProgressBar(self)

		self.get_specific_build_button = QtGui.QPushButton('Get Specific \n Build From Jenkins')
		self.get_specific_build_button.setSizePolicy (QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)


	def create_layout(self):
		main_layout = QtGui.QVBoxLayout()
		main_layout.setContentsMargins(0,0,0,0)
		main_layout.setSpacing(0)
		main_layout.addWidget(self.get_build_button)
		main_layout.addWidget(self.progressbar)
		main_layout.addWidget(self.get_specific_build_button)
		self.setLayout(main_layout)

	def create_connections(self):
		self.get_build_button.clicked.connect(self.get_build)
		
	def get_build(self):
		self.build_utils.handle_download()

class section2Layout(QtGui.QWidget):
	def __init__(self, build_utils_object, parent = None):
		super(section2Layout, self).__init__(parent)

		self.build_utils = build_utils_object
		self.build = ''

		self.create_widgets()
		self.create_layout()
		self.create_connections()

	def create_widgets(self):
		self.run_button = QtGui.QPushButton('Run')
		self.run_button.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

	def create_layout(self):
		pass
		main_layout = QtGui.QVBoxLayout()
		main_layout.setContentsMargins(0,0,0,0)
		main_layout.addWidget(self.run_button)
		self.setLayout(main_layout)

	def create_connections(self):
		self.run_button.clicked.connect(self.run_build)

	def run_build(self):
		self.build_utils.runBuild()

class tabLayout(QtGui.QWidget):
	def __init__(self,product_build,parent = None):
		super(tabLayout, self).__init__(parent)
		#Product and its associated build tuple
		self.build_utils_object = build_utils(product_build[0],product_build[1])

		self.section_1 = section1Layout(self.build_utils_object)
		self.section_2 = build_list_widget(self.build_utils_object)
		self.section_3 = section2Layout(self.build_utils_object)
		# print message

		self.create_widgets()
		self.create_layout()
		self.create_connections()

	def create_widgets(self):
		self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
		self.prefs_bar = QtGui.QPushButton('Delete Preferences')
		self.messages = QtGui.QLabel('', self)

		self.splitter.addWidget(self.section_1)
		self.splitter.addWidget(self.section_2)
		self.splitter.addWidget(self.section_3)
		self.splitter.setSizes([150,200,200])

	def create_layout(self):
		main_layout = QtGui.QVBoxLayout()
		main_layout.setContentsMargins(0,0,0,0)
		main_layout.addWidget(self.splitter)
		main_layout.addWidget(self.prefs_bar)
		main_layout.addWidget(self.messages)
		self.setLayout(main_layout)

	def create_connections(self):
		self.prefs_bar.clicked.connect(self.remove_prefs)
	

	def convert_alias(self):
		pass

	def remove_prefs(self):
		removePrefs(self.product_build[0],product_build[1],'/Users/Tom/Desktop/Joota/Joota_Depot/Footwear/Settings/Modo')



class tab_main_window(QtGui.QWidget):
	def __init__(self,configurations, parent = None):
		super(tab_main_window, self).__init__(parent)
		self.product_name = configurations
		self.configurations_list = configurations
		print configurations

		self.create_widgets()
		self.create_layout()
		self.create_connections()

	def create_widgets(self):
		self.widget_list = []
		self.tab_widget = QtGui.QTabWidget()

		#Add a tab for each configuration
		for index, configuration in enumerate(self.configurations_list):
			self.widget_list.append(tabLayout(configuration))
			self.tab_widget.addTab(self.widget_list[index],configuration[1])

		self.tab_widget.setWindowTitle('subScript') 

	def create_layout(self):
		main_layout = QtGui.QVBoxLayout()
		main_layout.addWidget(self.tab_widget)
		main_layout.setContentsMargins(5,5,5,5)
		self.setLayout(main_layout)

	def create_connections(self):
		pass


class main_window(QtGui.QWidget):
	def __init__(self,parent = None):
		super(main_window, self).__init__(parent)
		self.height = 300
		self.width = 900
		self.resize(self.width,self.height)
		self.state = True

		with open("subScript_generator.json") as data_file:
			product_dict = json.load(data_file)

		self.product_dict = product_dict['generator']
		self.change_list = change_list_widget()
		# self.product_dict = {'Nuke':{'Dev':'meerman'}, 'Joota' : {'Stable': 'meerman', 'Dev' : 'windows'}, 'Katana' : {'Stable': 'meerman', 'Integration' : 'windows'}}

		self.use_dictionary()
		self.create_widgets()
		self.create_layout()
		self.create_connections()

	def use_dictionary(self):
		self.product_list = []
		self.tab_list = []
		# Append nake of products to a list for the button to read
		for product in self.product_dict:
			self.test = []
			self.product_list.append(product)
			# Create a list of tabs to use for each product
			for tab in self.product_dict[product]:
				self.test.append((product,tab))
			self.tab_list.append(tab_main_window(self.test))

		self.tab = productButtonLayout(self.product_list)

	def create_widgets(self):
		self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
		self.splitter.addWidget(self.tab)
		self.splitter.addWidget(self.tab_list[0])
		self.splitter.addWidget(self.change_list)
		self.splitter.setSizes([5,595,300])

	def create_layout(self):
		main_layout = QtGui.QVBoxLayout()
		main_layout.setContentsMargins(0,0,0,0)
		main_layout.addWidget(self.splitter)
		self.setLayout(main_layout)


	def create_connections(self):
		# The singal that a button has been pressed from the products buttons
		self.tab.layout_changed.connect(self.change_tab)
		self.tab.button_pressed.connect(self.show_hide_changelist)

	def change_tab(self,number):
		self.use_dictionary()
		# Change the layout according to the product button chosen
		self.splitter.widget(1).hide()
		# For some reason this comes out as unicode so need to cast it as an int
		self.tab = self.tab_list[int(number)]
		self.splitter.insertWidget(1,self.tab)

	def show_hide_changelist(self):
		if self.state == True:
			self.splitter.setSizes([5,595,0])
			self.resize(600,self.height)
			self.state = False
		elif self.state == False:
			self.splitter.setSizes([5,595,300])
			self.resize(self.width,self.height)
			self.state = True



def main():
	global app
	global wid

	app = QtGui.QApplication(sys.argv)

	wid = main_window()

	wid.show()

	sys.exit(app.exec_())

if __name__ == '__main__':
   test = main()