
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QTableWidget,QTableView,QTableWidgetItem

import glob2
import sys
import os
import pathlib
from termcolor import colored
import pandas as pd
from Kicad_DB_Table_Model import DB_TableModel
DB_SEARCH_UI_NAME = "DB_Search.ui"
DB_SEARCH_UI_DIR = os.path.dirname(__file__)
DB_SEARCH_UI_PATH = os.path.join(DB_SEARCH_UI_DIR,DB_SEARCH_UI_NAME)

test_data = pd.DataFrame([
          [1, 9, 2],
          [1, 0, -1],
          [3, 5, 2],
          [3, 3, 2],
          [5, 8, 9],
        ], columns = ['A', 'B', 'C'])


class Kicad_DB_Search(QtWidgets.QMainWindow):
    def __init__(self):
        super(Kicad_DB_Search,self).__init__()
        uic.loadUi(DB_SEARCH_UI_PATH,self)

        self.link_widgets()
        self.init_slots()
       
        self.TV_model = DB_TableModel()
        

        

    def link_widgets(self):

        self.PB_Run = self.findChild(QtWidgets.QPushButton,'PB_Run')
        self.TV_DB_Search = self.findChild(QtWidgets.QTableView,'TV_DB_Search')

    def init_slots(self):
        self.PB_Run.clicked.connect(self.table_view_test)
    
    def table_view_test(self):
        self.TV_model.set_pandas_data(data=test_data)
        self.TV_DB_Search.setModel(self.TV_model)

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    kicad_db_gui = Kicad_DB_Search()
    kicad_db_gui.show()
    sys.exit(app.exec())