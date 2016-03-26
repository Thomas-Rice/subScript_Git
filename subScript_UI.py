import sys
import json
from PySide import QtCore, QtGui



class build_list_widget(QtGui.QWidget):
	def __init__(self,parent = None):
		super(build_list_widget, self).__init__(parent)

		self.checkbox_list = ['Stable_1','Stable_12','Stable_13','Stable_14','Stable_15','Stable_16','Stable_17','Stable_18','Stable_19','Stable_11',
								'Stable_12','Stable_13','Stable_14','Stable_15','Stable_16','Stable_17','Stable_18','Stable_19']
		self.create_widgets()
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
		value = self.list_layout.currentItem()
		print value.text()


class productButtonLayout(QtGui.QWidget):
	layout_changed = QtCore.Signal(str)
	def __init__(self, numbers, parent = None):
		super(productButtonLayout, self).__init__(parent)

		self.numbers = numbers

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

	def create_layout(self):
		main_layout = QtGui.QVBoxLayout()
		main_layout.setContentsMargins(0,0,0,0)
		main_layout.addWidget(self.buttonContainer)
		self.setLayout(main_layout)

	def create_connections(self):
		# Create as many connections as there are product buttons
		for item in range(0,len(self.numbers)):
			self.button[item].clicked.connect(lambda text = "{}".format(item): self.output(text))

	def output(self,number):
		self.layout_changed.emit(number)



class section1Layout(QtGui.QWidget):
	def __init__(self,parent = None):
		super(section1Layout, self).__init__(parent)

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
		pass

class section2Layout(QtGui.QWidget):
	def __init__(self,parent = None):
		super(section2Layout, self).__init__(parent)

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
		pass


class tabLayout(QtGui.QWidget):
	def __init__(self,message,parent = None):
		super(tabLayout, self).__init__(parent)

		self.section_1 = section1Layout()
		self.section_2 = build_list_widget()
		self.section_3 = section2Layout()

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
		pass
		# self.progress_bar.clicked.connect(self.returns)

	def returns(self):
		self.section_2.create_connections()



class tab_main_window(QtGui.QWidget):
	def __init__(self,configurations, parent = None):
		super(tab_main_window, self).__init__(parent)

		self.configurations_list = configurations

		self.create_widgets()
		self.create_layout()
		self.create_connections()

	def create_widgets(self):
		self.widget_list = []
		self.tab_widget = QtGui.QTabWidget()

		#Add a tab for each configuration
		for index, configuration in enumerate(self.configurations_list):
			self.widget_list.append(tabLayout(configuration))
			self.tab_widget.addTab(self.widget_list[index],configuration)

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
		self.width = 600
		self.resize(self.width,self.height)

		with open('subScript_generator.json') as data_file:
			self.dict = json.load(data_file)

		#get the right section
		self.product_dict = self.dict['generator']

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
				self.test.append(tab)
			self.tab_list.append(tab_main_window(self.test))

		self.tab = productButtonLayout(self.product_list)



	def create_widgets(self):
		self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
		self.splitter.addWidget(self.tab)
		self.splitter.addWidget(self.tab_list[0])
		self.splitter.setSizes([5,400])

	def create_layout(self):
		main_layout = QtGui.QVBoxLayout()
		main_layout.setContentsMargins(0,0,0,0)
		main_layout.addWidget(self.splitter)
		self.setLayout(main_layout)


	def create_connections(self):
		# The singal that a button has been pressed from the products buttons
		self.tab.layout_changed.connect(self.change_tab)

	def change_tab(self,number):
		self.use_dictionary()
		# Change the layout according to the product button chosen
		self.splitter.widget(1).hide()
		# For some reason this comes out as unicode so need to cast it as an int
		self.tab = self.tab_list[int(number)]
		self.splitter.insertWidget(1,self.tab)






def main():
	global app
	global wid

	app = QtGui.QApplication(sys.argv)

	wid = main_window()

	wid.show()

	sys.exit(app.exec_())

if __name__ == '__main__':
   test = main()