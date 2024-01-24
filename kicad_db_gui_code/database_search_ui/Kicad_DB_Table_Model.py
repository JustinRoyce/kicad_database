"""!

Kicad database model for QtTableView Class

<a href= https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/></a>

"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd



class DB_TableModel(QtCore.QAbstractTableModel):
    
    def __init__(self):
        super(DB_TableModel, self).__init__()
        print("working")

    def set_pandas_data(self,data):
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])