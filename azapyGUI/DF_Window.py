import tkinter as tk 
import pandas as pd
import os

import azapyGUI.configSettings as configSettings
from azapyGUI.DF_table import DF_table

class DF_Window(tk.Toplevel):
    def __init__(self, master, df, title, geometry, fname):
        self._master = master
        self._fname = fname

        super().__init__()
        self._window = self
        self._window.geometry(geometry)
        self._window.title(title)
        self._window.protocol("WM_DELETE_WINDOW", self.destroy)
        
        menubar = tk.Menu(self._window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='To csv', command=self._save_df)
        filemenu.add_command(label='To Excel', command=self._to_excel_df)
        menubar.add_cascade(label="Save", menu=filemenu)
        self._window.config(menu=menubar)
        
        self._dft = DF_table(df, master=self._window)
        self._dft.pack(fill=tk.BOTH, expand=True, ipadx=5, ipady=5)


    def _save_df(self):
        port_path = configSettings.MasterApplicationSettings["UserOutputDirectory"]
        path = tk.filedialog.asksaveasfilename(
                                    defaultextension=".csv",
                                    filetypes=[("Excel Files", "*.csv")],
                                    initialdir=port_path,
                                    initialfile=str(self._fname) + '.csv',
                                    parent=self._window
                                    )
        if path:
            self._dft.get_df().to_csv(path)
        
        
    def _to_excel_df(self):
        port_path = configSettings.MasterApplicationSettings["UserOutputDirectory"]
        path = tk.filedialog.asksaveasfilename(
                                    defaultextension=".xlsx",
                                    filetypes=[("Excel Files", "*.xlsx")],
                                    initialdir=port_path,
                                    initialfile=str(self._fname) + '.xlsx',
                                    parent=self._window
                                    )
        if path:
            with pd.ExcelWriter(path, mode='w', engine='xlsxwriter', 
                                date_format="YYYY-MM-DD", 
                                datetime_format="YYYY-MM-DD") as writer:
                #self._dft.get_df().reset_index().to_excel(writer, index=False)
                self._dft.get_df().to_excel(writer)
            if configSettings.MasterApplicationSettings["OpenExcel"]:
                try:
                    os.system('start EXCEL.EXE ' + path)
                except:
                    pass
        