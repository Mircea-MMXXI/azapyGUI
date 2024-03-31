import tkinter as tk 
from tkinter import ttk
import string
from copy import deepcopy

import azapyGUI.config as config
import azapyGUI.configMSG as configMSG

class CloneMenuPortfolioWindow:
    def __init__(self, master=None):
        self._master = master
        values = list(config.PortDataDict.keys())
        if len(values) == 0: return
        
        btn_text = "Save"
        self._end_values = False
        title = "Clone Portfolio"
        self._window = tk.Toplevel()
        self._window.title(title)
        self._window.geometry("230x130")      
        self._window.protocol("WM_DELETE_WINDOW", self._btn_cancel)
        
        frm = tk.LabelFrame(master=self._window, text=title, font=("Forte", 10) )
        frm.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        frm.columnconfigure(0, weight=1)
        frm.columnconfigure(1, weight=1)
        
        row = 0
        frm.rowconfigure(row, weight=1)
        lbl_text = "Target Portfolio:"
        lbl = tk.Label(master=frm, text=lbl_text)
        lbl.grid(row=row, column=0, pady=5, padx=5, sticky=tk.W)
        
        self._cbx = ttk.Combobox(master=frm, width=12, state='readonly')
        self._cbx['values'] = values
        self._cbx.current(0)
        self._cbx.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
        
        row += 1
        frm.rowconfigure(row, weight=1)
        lbl_text = "New name:"
        lbl = tk.Label(master=frm, text=lbl_text)
        lbl.grid(row=row, column=0, pady=5, padx=5, sticky=tk.W)
        
        self._ent = tk.Entry(master=frm, width=12,)
        self._ent.grid(row=row, column=1, pady=5, padx=5, sticky=tk.W)
        self._ent.bind('<Return>', lambda event: self._btn_action())
        self._ent.focus()
        
        row += 1 
        frm.rowconfigure(row, weight=1)
        btn_cancel = tk.Button(master=frm, text="Cancel", width=8, command=self._btn_cancel)
        btn_cancel.grid(row=row, column=0, pady=5, padx=5, sticky=tk.W)
        
        btn_action = tk.Button(master=frm, text=btn_text, width=8, command=self._btn_action)
        btn_action.grid(row=row, column=1, pady=5, padx=5, sticky=tk.E)

        self._window.update()
        if (self._master is not None) and self._master.winfo_exists():
            self._master.wait_window(self._window)
            
            
    def _btn_cancel(self):
        self._window.grab_release()
        if (self._master is not None) and self._master.winfo_exists():
            self._master.focus_set()
        self._window.destroy()
        
        
    def _btn_action(self):
        if self._end_values:
           self._btn_cancel()
           return
       
        tname = self._cbx.get()
        nname = self._ent.get().strip(string.whitespace)
        allowed_char = set(string.ascii_letters + string.digits + ".-_")
        if (len(nname) > 0) and (set(nname) < allowed_char):
            if nname in config.PortDataDict.keys():
                tk.messagebox.showwarning("Warning", configMSG._validate_portfolio_name_exist_msg, 
                                          parent=self._window)
                return
            port = deepcopy((config.PortDataDict[tname]))
            port.name = nname
            port.status = 'Set'
            port.saved = False
            config.PortDataDict[nname] = port
            self._btn_cancel()
            config.appPortfolioFrame.refresh()
            return
        tk.messagebox.showwarning("Warning", configMSG._validate_portfolio_name_msg, 
                                  parent=self._window)
            