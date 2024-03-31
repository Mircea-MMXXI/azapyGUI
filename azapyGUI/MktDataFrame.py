import tkinter as tk 
from tkinter import ttk
import pandas as pd
import os

import azapyGUI.config as config
import azapyGUI.configSettings as configSettings
from azapyGUI.SymbExtractWindow import SymbExtractWindow
from azapyGUI.SymbAnalyseWindow import SymbAnalyseWindow


class MktDataFrame(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        self._master = master
        super().__init__(master=self._master, **kwargs)
        self.grid_rowconfigure(0, weight=1)

        self._trv = ttk.Treeview(master=self, columns=("sdate", "edate", "nrow", "iserror", "status"))
        self._trv.grid(row=0, column=0, sticky=tk.NSEW)
        
        self._trv.heading("#0", text="Symbol", command=self._load_symbols)
        self._trv.heading("#1", text="Start Date")
        self._trv.heading("#2", text="End Date")
        self._trv.heading("#3", text="Nr records")
        self._trv.heading("#4", text="Errors")
        self._trv.heading("#5", text="Status")
        
        self._trv.column("#0", minwidth=10, width=60, stretch=False)
        self._trv.column("#1", minwidth=10, width=80, stretch=False)
        self._trv.column("#2", minwidth=10, width=80, stretch=False)
        self._trv.column("#3", minwidth=10, width=65, stretch=False)
        self._trv.column("#4", minwidth=10, width=40, stretch=False)
        self._trv.column("#5", minwidth=10, width=40, stretch=False)
        
        vscrlb = ttk.Scrollbar(master=self, 
                               orient ="vertical", 
                               command = self._trv.yview)
        vscrlb.grid(row=0, column=1, sticky=tk.NS)
        self._trv.configure(yscrollcommand = vscrlb.set)
        
        self._trv.tag_bind("trv_tag", "<<TreeviewSelect>>", self._trv_model_item_selector_func)
        
        self._set_trv_menu_selector()
        self.refresh()
       

    def refresh(self): 
        for item in self._trv.get_children():
            self._trv.delete(item)

        for kk, val in sorted(config.MktDataDict.items()):
            self._trv.insert(
                "",
                tk.END,
                text=val.name,
                values=(val.sdate().date(), val.edate().date(), val.nrow(), 
                        "Yes" if val.iserror() else "No",
                        "Busy" if val.status else "Free",),
                        tags=("trv_tag",),
            )
            

    def _set_trv_menu_selector(self):
        self._trv_menu_selector = tk.Menu(self._trv, tearoff = 0) 
        self._trv_menu_selector.add_command(label ="Update", command=self._update_func) 
        #self._trv_menu_selector.add_command(label ="Stats", command=self._donothing) 
        self._trv_menu_selector.add_command(label ="View", command=self._view_fun) 
        self._trv_menu_selector.add_command(label ="To Excel", command=self._to_excel_func) 
        self._trv_menu_selector.add_separator() 
        self._trv_menu_selector.add_command(label ="Remove", command=self._delete_func) 
        
        
    def _trv_model_item_selector_func(self, event):
        try: 
            self._trv_menu_selector.tk_popup(self._trv_menu_selector.winfo_pointerx(), 
                                             self._trv_menu_selector.winfo_pointery()) 
        finally: 
            self._trv_menu_selector.grab_release() 

        
    def _delete_func(self):
        items = self._trv.selection()
        for item in items:
            symb = self._trv.item(item, "text")
            del config.MktDataDict[symb]
        self.refresh()
        
    
    def _update_func(self):
        items = self._trv.selection()
        symbols = [self._trv.item(item, "text") for item in items]
        title = "Update Mkt Data"
        btn_text = "Update"
        SymbExtractWindow(master=self._master, title=title, 
                          symbols=symbols, btn_text=btn_text)
        self.refresh()
        
        
    def _view_fun(self):
        items = self._trv.selection()
        symbols = [self._trv.item(item, "text") for item in items]
        SymbAnalyseWindow(master=self._master, symbols=symbols)
        
        
    def _to_excel_func(self):
        items = self._trv.selection()
        port_path = configSettings.MasterApplicationSettings["UserOutputDirectory"]
        path = tk.filedialog.asksaveasfilename(
                                    defaultextension=".xlsx",
                                    filetypes=[("Excel Files", "*.xlsx")],
                                    initialdir=port_path,
                                    initialfile="MktDataBook.xlsx",
                                    parent=self._master,
                                    )
        if path:
            with pd.ExcelWriter(path, mode='w', engine='xlsxwriter', 
                                date_format="YYYY-MM-DD", 
                                datetime_format="YYYY-MM-DD") as writer:
                for item in items:
                    symb = self._trv.item(item, "text")
                    config.MktDataDict[symb].mktdata.to_excel(writer, sheet_name=symb)
            if configSettings.MasterApplicationSettings["OpenExcel"]:
                try:
                    os.system('start EXCEL.EXE ' + path)
                except:
                    pass
            
    def _load_symbols(self):
        SymbExtractWindow(master=self._master, title="Download Market Data", entry=True)
