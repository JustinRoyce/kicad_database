##
# @mainpage Kicad Database GUI
#
# @section description_main Description
# This GUI applications modifying the bill of materials data in a custom kicad database.  
#
# @section notes_main Notes
# - Add special project notes here that you want to communicate to the user.
# 
# @section author_kicad_DB_GUI Author
# - Created By Justin Gerald Royce

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QFileDialog
from Kicad_Database import Kicad_Database
from Kicad_DB_Config_File import Kicad_DB_Config_File,DEFAULT_CONFIG_PATH
import glob2
import sys
import os
import pathlib
from termcolor import colored



SCRIPT_DIR = os.path.dirname(__file__) ##< script file directory 
LOCAL_CONFIG_FILTER = os.path.join(SCRIPT_DIR,"*.ini")
os.environ["QT_LOGGING_RULES"]='*.debug=false;qt.pysideplugin=false'

KICAD_DB_UI_NAME = "kicad_db_ui.ui"
KICAD_DB_UI_PATH = os.path.join(SCRIPT_DIR,KICAD_DB_UI_NAME) 

GUI_STATUS_TOUT_MS = 1000 ##<  DEFAULT STATUS BAR TIMEOUT IN MILLISECONDS


class Kicad_DB_GUI(QtWidgets.QMainWindow):
    ##
    # @brief initalize GUI
    def __init__(self):
        super(Kicad_DB_GUI,self).__init__()
        uic.loadUi(KICAD_DB_UI_PATH,self)
        self.kicad_db = Kicad_Database()
        
        self.kicad_db_config = Kicad_DB_Config_File()
        self.kicad_db_config.set_config_file_path(config_file_path=DEFAULT_CONFIG_PATH)
        self.kicad_db_config.get_all_paths()

        self.path_DB = self.kicad_db_config.get_path_database()
        self.path_CSV_import = self.kicad_db_config.get_path_CSV_import_dir()
        self.path_DB_export = self.kicad_db_config.get_path_db_export()
        self.path_config_file = self.kicad_db_config.get_path_config_file()

        self.init_path_line_edits()
        self.link_widgets()
        self.init_slots()
    
    ##
    # @brief links QT UI widgets to custom QT mainwindow
    def link_widgets(self):
        
        """ PUSHBUTTON WIDGET INITALIZED """

        self.PB_Link_Datasheet = self.findChild(QtWidgets.QPushButton,'PB_Link_Datasheet')
        self.PB_Query_DB = self.findChild(QtWidgets.QPushButton,'PB_Query_DB')
        self.PB_Reset_Form = self.findChild(QtWidgets.QPushButton,'PB_Reset_Form')
        self.PB_Push_DB = self.findChild(QtWidgets.QPushButton,'PB_Push_DB')
        self.PB_DB_Path = self.findChild(QtWidgets.QPushButton,'PB_DB_Path')
        self.PB_DB_Connect = self.findChild(QtWidgets.QPushButton,'PB_DB_Connect')
        self.PB_Load_Config = self.findChild(QtWidgets.QPushButton,'PB_Load_Config')
        self.PB_Config_Path = self.findChild(QtWidgets.QPushButton,'PB_Config_Path')
        self.PB_Import_CSV = self.findChild(QtWidgets.QPushButton,'PB_Import_CSV')
        self.PB_Export_DB = self.findChild(QtWidgets.QPushButton,'PB_Export_DB')
        self.PB_CSV_Import_Path = self.findChild(QtWidgets.QPushButton,'PB_CSV_Import_Path')
        self.PB_DB_Import_Path = self.findChild(QtWidgets.QPushButton,'PB_DB_Import_Path')

        """ COMBOBOX WIDGET INITALIZED """

        self.CB_Field_Query = self.findChild(QtWidgets.QComboBox,'CB_Field_Query')
        self.CB_Table_Name = self.findChild(QtWidgets.QComboBox,'CB_Table_Name')

        """ LABEL WIDGET INITALIZED """

        self.LB_DB_Connect = self.findChild(QtWidgets.QLabel,'LB_DB_Connect')

        """ TEXT EDIT WIDGET INITALIZED """

        self.TE_Field_Description = self.findChild(QtWidgets.QTextEdit,'TE_Field_Description')
        self.TE_Field_Notes = self.findChild(QtWidgets.QTextEdit,'TE_Field_Notes')

        """ LINE EDIT WIDGET INITALIZED """

        self.LE_Field_Symbol = self.findChild(QtWidgets.QLineEdit,'LE_Field_Symbol')
        self.LE_Field_Footprint = self.findChild(QtWidgets.QLineEdit,'LE_Field_Footprint')
        self.LE_Field_Value = self.findChild(QtWidgets.QLineEdit,'LE_Field_Value')
        self.LE_Field_Manufacturer = self.findChild(QtWidgets.QLineEdit,'LE_Field_Manufacturer')
        self.LE_Field_MPN = self.findChild(QtWidgets.QLineEdit,'LE_Field_MPN')
        self.LE_Field_Digikey_PN = self.findChild(QtWidgets.QLineEdit,'LE_Field_Digikey_PN')
        self.LE_Field_Mouser_PN = self.findChild(QtWidgets.QLineEdit,'LE_Field_Mouser_PN')
        self.LE_Field_LCSC_PN = self.findChild(QtWidgets.QLineEdit,'LE_Field_LCSC_PN')
        self.LE_Field_Distributor = self.findChild(QtWidgets.QLineEdit,'LE_Field_Distributor')
        self.LE_Field_Misc_PN = self.findChild(QtWidgets.QLineEdit,'LE_Field_Misc_PN')
        self.LE_Field_Tolerance = self.findChild(QtWidgets.QLineEdit,'LE_Field_Tolerance')
        self.LE_Field_Rating = self.findChild(QtWidgets.QLineEdit,'LE_Field_Rating')
        self.LE_Field_Package = self.findChild(QtWidgets.QLineEdit,'LE_Field_Package')
        self.LE_Link_Datasheet = self.findChild(QtWidgets.QLineEdit,'LE_Link_Datasheet')
        self.LE_DB_query = self.findChild(QtWidgets.QLineEdit,'LE_DB_query')
        self.LE_DB_Path = self.findChild(QtWidgets.QLineEdit,'LE_DB_Path')
        self.LE_Config_Path = self.findChild(QtWidgets.QLineEdit,'LE_Config_Path')
        self.LE_CSV_Import_Path = self.findChild(QtWidgets.QLineEdit,'LE_CSV_Import_Path')
        self.LE_DB_Export_Path = self.findChild(QtWidgets.QLineEdit,'LE_DB_Export_Path')
    
    ##
    # @brief initialize line edits from member functions extracted from config file  
    #
    def init_path_line_edits(self):
        self.LE_DB_Path.setText(self.path_DB)
        self.LE_Config_Path.setText(self.path_config_file)
        self.LE_DB_Export_Path.setText(self.path_DB_export)
        self.LE_CSV_Import_Path.setText(self.path_CSV_import)

    ##
    # @brief: modify DB connect label to red and False text
    #
    def setDB_Connect_LB_False(self):
        self.LB_DB_Connect.setStyleSheet("background-color: red")
        self.LB_DB_Connect.setText("False")

    ##
    # @brief: modify DB connect label to green and True text
    #
    def setDB_Connect_LB_True(self):
        self.LB_DB_Connect.setStyleSheet("background-color: lightgreen")
        self.LB_DB_Connect.setText("True") 

    ##
    # @brief connect database using PB_DB_conn push button slot function
    #
    def PB_DB_conn_press(self):
        # Access database path through lineedit
        db_path = self.LE_DB_Path.text()
    
        # valid kicad database
        (is_valid_db_bool,status_msg) = self.kicad_db.is_valid_kicad_db(db_path)
        self.statusBar().showMessage(status_msg,GUI_STATUS_TOUT_MS)

    ##
    # @brief connect to database using self.path_DB member function
    #        
    def connect_database(self):

        (conn,status_bool) = self.kicad_db.create_connection(db_fpath=self.path_DB)
        
        if(status_bool == False):
            error_msg = "UNABLE TO CONNECT TO DATABASE"
            self.statusBar().showMessage(error_msg,GUI_STATUS_TOUT_MS)
            return
        else:
            self.kicad_db.SQL_connect

    ##
    # @brief set Database Path from path_DB member function
    #            
    def setDatabasePath(self):  
        init_dir = os.path.dirname(self.path_DB)
        if(os.path.isdir(init_dir)==False):
            init_dir =SCRIPT_DIR
        fileName , _ = QFileDialog.getOpenFileName(self,
                    "Set Database Path", init_dir, "SQL Database (*.sqlite3)")
        
        if(type(fileName)!= str):
            fileName = ""

        
        msg = "Invalid File Name"
        if(os.path.isfile(fileName)):
            msg = "Database Path Set"
            self.LE_DB_Path.setText(fileName)
            self.path_DB = fileName

        self.statusBar().showMessage(msg,GUI_STATUS_TOUT_MS)

    ##
    # @brief set table query with Table Query combobox
    #     
    def set_table_wt_combobox(self):
        timeout_ms= 1000
        text = str(self.CB_Table_Name.currentText())
        msg = "Selected Table: " + text
        self.kicad_db.curr_table = text
        self.statusBar().showMessage(msg,timeout_ms)

    ##
    # @brief set field query with Field Query combobox
    #        
    def set_field_query_wt_combobox(self):
        timeout_ms= 1000
        text = str(self.CB_Field_Query.currentText())
        msg = "Selected Field Query: " + text
        self.kicad_db.field_query = text
        self.statusBar().showMessage(msg,timeout_ms)

    ##
    # @brief set config file path using file dialog
    #    
    def set_config_file_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"SELECT INI FILE" , __file__,"Config File (*.ini);;All Files (*)", options=options)
        if(fileName):
            extension = fileName[-3:]
            print(extension)
            if(extension == "ini"):
                self.LE_Config_Path.setText(fileName)
                msg = "CONFIG FILE PATH SET: " + fileName
            else:
                msg = "INVALID FILE EXTENSION"
            self.statusBar().showMessage(msg,GUI_STATUS_TOUT_MS)

        else:
            msg = "CONFIG PATH NOT SELECTED" 

        self.statusBar().showMessage(msg,GUI_STATUS_TOUT_MS)
  
    ##
    # @brief load config file using LE_Config_Path line edit
    #
    def load_config_file(self):   
        fileName = self.LE_Config_Path.text()
        
        if fileName:

            is_config_file = self.kicad_db_config.set_config_file_path(fileName)
            if(is_config_file == True):
                msg = self.kicad_db_config.get_all_paths() 
                self.statusBar().showMessage(msg,GUI_STATUS_TOUT_MS)
        
        else:
            msg = "Invalid File Name"
            self.statusBar().showMessage(msg,GUI_STATUS_TOUT_MS)

        return None    

    ##
    # @brief reset form text
    #
    def reset_form(self):

        self.LE_Field_Symbol.setText("")
        self.LE_Field_Footprint.setText("")
        self.LE_Field_Value.setText("")
        self.LE_Field_Manufacturer.setText("")
        self.LE_Field_MPN.setText("")
        self.LE_Field_Digikey_PN.setText("")
        self.LE_Field_Mouser_PN.setText("")
        self.LE_Field_LCSC_PN.setText("")
        self.LE_Field_Distributor.setText("")
        self.LE_Field_Misc_PN.setText("")
        self.LE_Field_Tolerance.setText("")
        self.LE_Field_Rating.setText("")
        self.LE_Field_Package.setText("")
        self.LE_Link_Datasheet.setText("")
        self.LE_DB_query.setText("")
        self.TE_Field_Description.setText("")
        self.TE_Field_Notes.setText("")
    
        
    ##
    # @brief initialize slots
    #
    def init_slots(self):

        #add table names to combo box
        field_list = self.kicad_db.get_DB_field_list()
        table_list = self.kicad_db.get_DB_table_list()

        self.CB_Table_Name.addItems(table_list)
        self.CB_Field_Query.addItems(field_list)
        
        self.set_table_wt_combobox()
        self.set_field_query_wt_combobox()

        self.CB_Table_Name.activated.connect(self.set_table_wt_combobox)
        self.CB_Field_Query.activated.connect(self.set_field_query_wt_combobox)

        self.PB_Reset_Form.clicked.connect(self.reset_form)
        self.PB_DB_Path.clicked.connect(self.setDatabasePath)
        self.PB_Load_Config.clicked.connect(self.load_config_file)
        self.PB_Config_Path.clicked.connect(self.set_config_file_path)

        self.PB_DB_Connect.clicked.connect(self.PB_DB_conn_press)
        
    ##
    # @brief Find local config file path 
    #
    def find_local_config_path(self):
        local_config_list = glob2.glob(LOCAL_CONFIG_FILTER)
        if(local_config_list):
          local_config_path =  local_config_list[0]
        else:
          local_config_path = ""
        return local_config_path
    
    def test(self):
        print(self.find_local_config_path())
    
    def PB_query_database(self):
        print("working")
    

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    kicad_db_gui = Kicad_DB_GUI()
    kicad_db_gui.show()
    sys.exit(app.exec())