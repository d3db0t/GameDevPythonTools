import sd
from sd.tools import export
from sd.api.sdproperty import SDPropertyCategory
from sd.api.sdvaluefloat import SDValueFloat
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QFont
import os
import glob

'''
DOCUMENTATION
https://shadytantawy.art/sdanimateplugin
'''

class SDAnimate():
	# Initial variables and attributes
	parameter_value   = 0
	step_value        = 0.1
	sprites_number    = 1
	parameter_index   = 0
	folder_path       = None
	file_type         = '\*.png'
	file_prefix       = ""

	# Get the application and the UI Manager.
	app   = sd.getContext().getSDApplication()
	uiMgr = app.getQtForPythonUIMgr()

	# Create a new dialog. For shortcuts to work correctly
	mainWindow = uiMgr.getMainWindow()
	dialog     = QtWidgets.QDialog(parent=mainWindow)
	dialog.setWindowTitle("SDAnimate v1.0 - by Shady Tantawy")
	dialog.setFixedSize(QtCore.QSize(400, 300))

	# Get the current graph and the selected node
	current_graph  = uiMgr.getCurrentGraph()

	# Getting the graph properties (Exposed parameters)
	input_section = SDPropertyCategory.Input
	props         = current_graph.getProperties(input_section)
	prop          = props[parameter_index]

	props_labels = []
	for p in props:
		props_labels.append(p.getLabel())


	# Create a layout
	layout = QtWidgets.QVBoxLayout()
	margin_value = 30
	layout.setContentsMargins(margin_value,margin_value,margin_value,margin_value)


	# Labels (lbl)
	lbl_exposed_parameters = QtWidgets.QLabel("Parameter (must be exposed)")
	lbl_step_value         = QtWidgets.QLabel("Step Value")
	lbl_sprites_number     = QtWidgets.QLabel("Sprites Number")
	lbl_file_prefix        = QtWidgets.QLabel("File Prefix")
	lbl_folder_path        = QtWidgets.QLabel("")

	lbl_exposed_parameters.setFont(QFont("Times", 10, QFont.Bold))
	lbl_step_value.setFont(QFont("Times", 10, QFont.Bold))
	lbl_sprites_number.setFont(QFont("Times", 10, QFont.Bold))
	lbl_file_prefix.setFont(QFont("Times", 10, QFont.Bold))

	# Buttons (btn)
	btn_generate_flipbook = QtWidgets.QPushButton("Generate")
	btn_browse_folder     = QtWidgets.QPushButton("Browse Folder")

	btn_generate_flipbook.setStyleSheet("background-color : green")

	# Drop down menus (ddm)
	ddm_exposed_parameters = QtWidgets.QComboBox()
	
	ddm_exposed_parameters.addItems(props_labels)
	

	# Spin Box (sb)
	sb_step_value = QtWidgets.QDoubleSpinBox()
	sb_step_value.setSingleStep(0.1)
	sb_step_value.setMinimum(0.1)
	sb_step_value.setMaximum(1)

	sb_sprites_number = QtWidgets.QSpinBox()
	sb_sprites_number.setSingleStep(1)
	sb_sprites_number.setMinimum(1)
	sb_sprites_number.setMaximum(16)

	# Line Edit (le)
	le_file_prefix = QtWidgets.QLineEdit()
	le_file_prefix.setPlaceholderText("Default: " + "[index].png")
	le_file_prefix.setMaxLength(20)

	# Add widgets to layout
	layout.addWidget(lbl_exposed_parameters)
	layout.addWidget(ddm_exposed_parameters)
	layout.addWidget(lbl_step_value)
	layout.addWidget(sb_step_value)
	layout.addWidget(lbl_sprites_number)
	layout.addWidget(sb_sprites_number)
	layout.addWidget(lbl_file_prefix)
	layout.addWidget(le_file_prefix)
	layout.addWidget(btn_browse_folder)
	layout.addWidget(lbl_folder_path)
	layout.addWidget(btn_generate_flipbook)
	dialog.setLayout(layout)
	
	def __init__(self):
		# Actions (Widgets)
		self.btn_generate_flipbook.clicked.connect(self.on_btn_generate_flipbook)
		self.btn_browse_folder.clicked.connect(self.on_btn_browse_folder)
		self.ddm_exposed_parameters.currentIndexChanged.connect(self.on_ddm_exposed_parameters_index_change)
		self.sb_step_value.valueChanged.connect(self.on_sb_step_value_change)
		self.sb_sprites_number.valueChanged.connect(self.on_sb_sprites_number_change)
		self.le_file_prefix.textChanged.connect(self.on_le_file_prefix_change)
	

	# Functions
	@classmethod
	def on_btn_generate_flipbook(self):
		print("Generating images...")
		if not self.folder_path:
			self.lbl_folder_path.setText("You must select a folder!")
			print("You must select a folder!")
			return

		for x in range(sprites_number):
			export.exportSDGraphOutputs(self.current_graph, self.folder_path, str(x) + ".png")
			self.current_graph.setPropertyValue(self.prop, SDValueFloat.sNew(self.parameter_value))
			self.parameter_value += self.step_value

			# File Naming
			files               = glob.glob(self.folder_path + self.file_type)
			newest_file_created = max(files, key=os.path.getctime)
			new_file_name       = self.file_prefix + str(x) + ".png"
			os.rename(newest_file_created, os.path.join(self.folder_path, new_file_name))


	@classmethod
	def on_btn_browse_folder(self):
		f = str(QtWidgets.QFileDialog.getExistingDirectory())
		self.folder_path = f
		self.lbl_folder_path.setText(f)
		print(f)


	@classmethod
	def on_ddm_exposed_parameters_index_change(self, i):
		self.parameter_index = i
		self.prop = self.props[i]
		print("[Parameter Selected]" + '\n' 
		+ "Label: " + self.prop.getLabel() + '\n'
		+ "ID: " + self.prop.getId() + '\n'
		+ "Index: " + str(i))
		

	@classmethod
	def on_sb_step_value_change(self, i):
		global step_value
		x = round(i, 1)
		step_value = x

	@classmethod
	def on_sb_sprites_number_change(self, i):
		global sprites_number
		sprites_number = i

	@classmethod
	def on_le_file_prefix_change(self, s):
		self.file_prefix = s

def initializeSDPlugin():
	print("SDAnimate v1.0 - by Shady Tantawy")
	sdanimate = SDAnimate()
	sdanimate.dialog.show()

	
	
