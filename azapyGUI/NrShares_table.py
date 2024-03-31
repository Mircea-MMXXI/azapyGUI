import tkinter as tk 
import pandas as pd
import numpy as np

from azapyGUI.DF_table import DF_table
from azapyGUI.modelParametersValidation import _validIntPositive

class NrShares_table(DF_table):
    def __init__(self, master, data):
        self._df = pd.DataFrame(data)
        super().__init__(master=master, df=pd.DataFrame(data))
        
    def _draw(self, df):
        self._sent = [ [tk.StringVar(self._frm, value=symb),
                        tk.IntVar(self._frm, value=df.loc[symb][0])] for symb in df.index]
        
        
        self._frm.columnconfigure(0, weight=1)
        self._frm.columnconfigure(1, weight=1)
        for row, ll in enumerate(self._sent):
            self._frm.rowconfigure(row, weight=1)
            lbl = tk.Label(self._frm, textvariable=ll[0], width=5, bg='white', relief=tk.RIDGE, anchor=tk.W)
            lbl.grid(row=row, column=0, sticky=tk.NSEW)
            
            ent = tk.Entry(self._frm, textvariable=ll[1], width=5, validate='key')
            ent['validatecommand'] = (ent.register(_validIntPositive),'%S','%d','%P')
            ent.grid(row=row, column=1, sticky=tk.NSEW)
        
        
    def get_data(self):
        index = pd.Index([self._sent[kk][0].get() for kk in range(len(self._sent))], dtype=str)
        data = pd.Series([self._sent[kk][1].get() for kk in range(len(self._sent))], 
                          index=index, dtype=np.dtype(float))
        return data
    
    
    def set_data(self, data):
        df = pd.DataFrame(data)
        for row, symb in enumerate(df.index):
            self._sent[row][0].set(symb)
            self._sent[row][1].set(df.loc[symb][0])
            
    
    def sort(self, axis=1, ascending=False):
        data = self.get_data()

        if axis == 0:
            self.set_data(data.sort_index(ascending=ascending))
            return

        self.set_data(pd.DataFrame(data)
                        .reset_index()
                        .sort_values(by=[0, 'index'], ascending=[ascending, True])
                        .set_index('index'))
