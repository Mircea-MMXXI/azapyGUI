import tkinter as tk 
from tkinter import ttk

import azapyGUI.config as config


class SelectOneWindow:
    def __init__(self, master=None, title=None, text=None, values=None, 
                 tip_text=None, btn_text="Save"):
        if (values is None) or (len(values) == 0): return
        self._master = master
        
        self._window = tk.Toplevel()
        self._window.geometry("200x130")
        self._window.title(title)
        self._window.protocol("WM_DELETE_WINDOW", self._btn_cancel)
        self._window.focus_set()
        
        self.selection = None
        
        frm = tk.LabelFrame(master=self._window, text=title, font=("Forte", 10))
        frm.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        row = 0
        lbl = tk.Label(master=frm, text=text)
        lbl.grid(row=row, columnspan=2, pady=5, padx=5, sticky=tk.EW)
        frm.rowconfigure(row, weight=1)
                   
        row += 1         
        self._ent = ttk.Combobox(master=frm, width=15, state='readonly')
        self._ent['values'] = values
        self._ent.current(0)
        self._ent.grid(row=row, columnspan=2, padx=5, pady=5)
        if tip_text is not None:
            config.tiptil.bind(self._ent, tip_text)
        frm.rowconfigure(row, weight=1)
        
        row += 1
        btn_calcel = tk.Button(master=frm, text="Cancel", 
                               command=self._btn_cancel, width=8)
        btn_calcel.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        frm.columnconfigure(0, weight=1)
        
        btn_action = tk.Button(master=frm, text=btn_text, 
                               command=self._btn_action, width=8)
        btn_action.grid(row=row, column=1, padx=5, pady=5, sticky=tk.E)
        frm.columnconfigure(1, weight=1)
        frm.rowconfigure(row, weight=1)
        
        self._window.grab_set()
        self._window.update()
        if (self._master is not None) and self._master.winfo_exists():
            self._master.wait_window(self._window)
            

    def _btn_cancel(self):
        self._window.grab_release()
        if (self._master is not None) and self._master.winfo_exists():
            self._master.focus_set()
        self._window.destroy()
        
        
    def _btn_action(self):
        # to be implemented by the derived class
        pass
