from PySide2 import QtCore, QtWidgets, QtGui
from maya import cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from imp import reload
import DNA.module.YG_DNA as YG_DNA
reload(YG_DNA)
# YG_DNA = DNA.module.YG_DNA.YG_DNA()

from os import environ
from os import path as ospath
from sys import path as syspath
from sys import platform

# if you use Maya, use absolute path
usd = cmds.internalVar(usd=True)
mayascripts = '%s/%s' % (usd.rsplit('/', 3)[0], 'scripts/')

ROOT_DIR = mayascripts+"DNA/"
ROOT_LIB_DIR = f"{ROOT_DIR}/lib"
if platform == "win32":
    LIB_DIR = f"{ROOT_LIB_DIR}/windows"
elif platform == "linux":
    LIB_DIR = f"{ROOT_LIB_DIR}/linux"
else:
    raise OSError(
        "OS not supported, please compile dependencies and add value to LIB_DIR"
    )

# Add bin directory to maya plugin path
if "MAYA_PLUG_IN_PATH" in environ:
    separator = ":" if platform == "linux" else ";"
    environ["MAYA_PLUG_IN_PATH"] = separator.join([environ["MAYA_PLUG_IN_PATH"], LIB_DIR])
else:
    environ["MAYA_PLUG_IN_PATH"] = LIB_DIR

# Adds directories to path
syspath.insert(0, ROOT_DIR)
syspath.insert(0, LIB_DIR)

# this example is intended to be used in Maya
from dna_viewer import show_dna_viewer_window

def get_maya_win():
    for obj in QtWidgets.QApplication.topLevelWidgets():
        if obj.objectName() == "MayaWindow":
            return obj
    raise RuntimeError("Could not find MayaWindow instance")

# class MyDockableWindow(MayaQWidgetDockableMixin, QtWidgets.QDialog):
class MyDockableWindow(QtWidgets.QDialog):
    TOOL_NAME = 'YG_DNA_v1.1'

    selected_filter = "DNA (*.dna)"

    def __init__(self, parent=get_maya_win()):
        super(self.__class__, self).__init__(parent=parent)
        self.setObjectName(self.__class__.TOOL_NAME)

        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(self.TOOL_NAME)
        self.resize(400, 200)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        '''
        DNA
        '''
        self.filepath_le = QtWidgets.QLineEdit()
        self.select_file_path_btn = QtWidgets.QPushButton("...")
        self.select_file_path_btn.setIcon(QtGui.QIcon(":fileOpen.png"))

        '''
        Modify DNA
        '''
        self.modify_filepath_le = QtWidgets.QLineEdit()
        self.select_modify_file_path_btn = QtWidgets.QPushButton("...")
        self.select_modify_file_path_btn.setIcon(QtGui.QIcon(":fileOpen.png"))

        '''
        Button
        '''
        self.DNAViewer = QtWidgets.QPushButton('DNA Viewer')
        self.currentDNA = QtWidgets.QPushButton('Memory Current DNA Veterx Position')
        self.checkLOD = QtWidgets.QCheckBox('LOD_3_4')
        self.modifyTransform = QtWidgets.QPushButton('Modify Joint and Vertex Transform')
        self.saveDNA = QtWidgets.QPushButton('Save Modify DNA')
        self.Assemble = QtWidgets.QPushButton('Assemble Maya Scene')

    def create_layout(self):
        '''
        separator
        '''
        self.separatorLine_1 = QtWidgets.QFrame()
        self.separatorLine_1.setFrameShape( QtWidgets.QFrame.HLine )
        self.separatorLine_1.setFrameShadow( QtWidgets.QFrame.Raised )

        '''
        layout
        '''
        # top
        btn_layout_0 = QtWidgets.QHBoxLayout()
        btn_layout_0.addWidget(QtWidgets.QLabel("DNA Calibration"))
        btn_layout_0.addWidget(self.DNAViewer)

        # 1st
        file_path_layout = QtWidgets.QHBoxLayout()
        file_path_layout.addWidget(self.filepath_le)
        file_path_layout.addWidget(self.select_file_path_btn)

        form_layout_1 = QtWidgets.QFormLayout()
        form_layout_1.addRow("DNA :", file_path_layout)

        # 2nd
        btn_layout_1 = QtWidgets.QVBoxLayout()
        btn_layout_1.addWidget(QtWidgets.QLabel("2nd"))
        btn_layout_1.addWidget(self.currentDNA)

        # 3rd
        chk_layout = QtWidgets.QHBoxLayout()
        chk_layout.addWidget(QtWidgets.QLabel("modify rig in maya..."))
        chk_layout.addWidget(self.checkLOD)
        layout_3rd = QtWidgets.QVBoxLayout()
        layout_3rd.addWidget(self.modifyTransform)

        # 4th
        modify_file_path_layout = QtWidgets.QHBoxLayout()
        modify_file_path_layout.addWidget(self.modify_filepath_le)
        modify_file_path_layout.addWidget(self.select_modify_file_path_btn)

        form_layout_2 = QtWidgets.QFormLayout()
        form_layout_2.addRow("Modify DNA :", modify_file_path_layout)

        btn_layout_2 = QtWidgets.QVBoxLayout()
        btn_layout_2.addWidget(self.saveDNA)

        # 5th
        btn_layout_2.addWidget(QtWidgets.QLabel("5th"))
        btn_layout_2.addWidget(self.Assemble)

        '''
        add widget
        '''
        main_layout = QtWidgets.QVBoxLayout(self)

        # top
        main_layout.addLayout(btn_layout_0)
        main_layout.addWidget(self.separatorLine_1)

        # 1st
        main_layout.addWidget(QtWidgets.QLabel("1st"))
        main_layout.addLayout(form_layout_1)

        # 2nd
        main_layout.addLayout(btn_layout_1)

        # 3rd
        main_layout.addWidget(QtWidgets.QLabel("3rd"))
        main_layout.addLayout(chk_layout)
        main_layout.addLayout(layout_3rd)

        # 4th, 5th
        main_layout.addWidget(QtWidgets.QLabel("4th"))
        main_layout.addLayout(form_layout_2)
        main_layout.addLayout(btn_layout_2)

        main_layout.addStretch()

    def create_connections(self):
        self.DNAViewer.clicked.connect(self.on_button_pressed)
        self.select_file_path_btn.clicked.connect(self.show_file_select_dialog)
        self.currentDNA.clicked.connect(self.on_button_pressed)
        self.checkLOD.toggled.connect(self.on_check_box_toggled)
        self.modifyTransform.clicked.connect(self.on_button_pressed)
        self.select_modify_file_path_btn.clicked.connect(self.show_modify_file_select_dialog)
        self.saveDNA.clicked.connect(self.on_button_pressed)
        self.Assemble.clicked.connect(self.on_button_pressed)

    def show_file_select_dialog(self):
        file_name, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select DNA File", YG_DNA.DNA_DIR, self.selected_filter)
        if file_name:
            self.filepath_le.setText(file_name)
            YG_DNA.CHARACTER_NAME = file_name.rsplit('/', 1)[-1][:-4]
            YG_DNA.MODIFIED_CHARACTER_DNA = f"{YG_DNA.OUTPUT_DIR}/{YG_DNA.CHARACTER_NAME}_modified"
            YG_DNA.CHARACTER_DNA = f"{YG_DNA.DNA_DIR}/{YG_DNA.CHARACTER_NAME}.dna"
            YG_DNA.DNA_NEW = f"{YG_DNA.OUTPUT_DIR}/{YG_DNA.CHARACTER_NAME}_lods_3_4"

    def show_modify_file_select_dialog(self):
        file_name, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Modify DNA File", YG_DNA.OUTPUT_DIR, self.selected_filter)
        if file_name:
            self.modify_filepath_le.setText(file_name)

            if self.checkLOD.checkState() == QtCore.Qt.CheckState.Checked:
                YG_DNA.DNA_NEW = file_name.rsplit('/', 1)[-1][:-4]
            else:
                YG_DNA.MODIFIED_CHARACTER_DNA = file_name.rsplit('/', 1)[-1][:-4]

    def on_button_pressed(self):
        sender = self.sender()
        print ('{0} : pressed'.format(sender.text()))

        if sender.text() == 'Memory Current DNA Veterx Position':
            # print (self.filepath_le.text())
            print (YG_DNA.CHARACTER_NAME)

            if self.checkLOD.checkState() == QtCore.Qt.CheckState.Checked:
                file_name = YG_DNA.DNA_NEW
                self.modify_filepath_le.setText(file_name)
            else:
                file_name = YG_DNA.MODIFIED_CHARACTER_DNA
                self.modify_filepath_le.setText(file_name)

            YG_DNA.memory_current_DNA_vertex_position()



        elif sender.text() == 'Save Modify DNA':
            # print (self.modify_filepath_le.text())
            print (YG_DNA.MODIFIED_CHARACTER_DNA)

            if self.checkLOD.checkState() == QtCore.Qt.CheckState.Checked:
                print('save LOD_3_4')
                YG_DNA.save_setLOD_dna()
            else:
                print('save modify DNA')
                YG_DNA.save_modify_dna()

        elif sender.text() == 'Assemble Maya Scene':
            print ('file save')
            file_name = ''

            if self.checkLOD.checkState() == QtCore.Qt.CheckState.Checked:
                file_name = YG_DNA.DNA_NEW
                # self.modify_filepath_le.setText(file_name)
                print (file_name)
            else:
                file_name = YG_DNA.MODIFIED_CHARACTER_DNA
                # self.modify_filepath_le.setText(file_name)
                print (file_name)

            YG_DNA.assemble_maya_scene(file_name)

        elif sender.text() == 'DNA Viewer':
            print ('viewer')

            show_dna_viewer_window()

        elif sender.text() == 'Modify Joint and Vertex Transform':
            print ('Modify Joint / Vertex Transform')

            YG_DNA.disconnectRL4()
            YG_DNA.select_loop_bones()

    def on_check_box_toggled(self):
        sender = self.sender()
        # print ('{0} : toggled'.format(sender.text()))

        if sender.text() == 'LOD_3_4':
            if self.checkLOD.checkState() == QtCore.Qt.CheckState.Checked:
                print ('checked')
                # print (self.checkLOD.checkState())
            else:
                print ('unchecked')

            # YG_DNA.save_setLOD_dna()

try:
    my_win.deleteLater()
except:
    pass

my_win = MyDockableWindow()
# my_win.show(dockable=True)
my_win.show()
