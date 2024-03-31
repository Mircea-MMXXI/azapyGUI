import tkinter as tk 
from tkinter import ttk

import azapyGUI.config as config
import azapyGUI.configTips as configTips
import azapyGUI.configSettings as configSettings
import azapyGUI.modelParametersValidation as mpv
from azapyGUI.GetMktData import GetMktData
from azapyGUI.mktDataValidation import sdate_edate_validate


class SymbExtractWindow:
    def __init__(self, master=None, title=None, symbols=None, btn_text="OK", validate=False, entry=False):
        self._master = master
        self._symbols = symbols
        self._validate = validate
        self._entry = entry
        
        self.errorSymb = []

        self._window = tk.Toplevel()
        self._window.title(title)
        self._window.focus_set()
        self._window.grab_set()
        self._window.protocol("WM_DELETE_WINDOW", self._btn_cancel_func)
        
        frm = tk.LabelFrame(master=self._window, text=title, font=("Forte", 10))
        frm.pack(fill=tk.BOTH, expand=True)
        
        for i in range(4): frm.columnconfigure(i, weight=1)
        
        row = 0
        frm.rowconfigure(row, weight=1)
        if self._entry:
            tk.Label(master=frm, text="Symbols").grid(row=row, column=0)
            self._ent_symb = tk.Entry(master=frm)
            self._ent_symb.grid(row=row, column=1, columnspan=3, pady=5, padx=5, sticky=tk.EW)
            self._ent_symb.focus()
            config.tiptil.bind(self._ent_symb, configTips._sew_symb_tip)
        else:
            text = mpv._list2string(self._symbols)
            lbl = tk.Label(master=frm, text=text, justify=tk.LEFT)
            lbl.grid(row=row, columnspan=4, pady=5, padx=5, sticky=tk.NSEW)
        
        row += 1
        frm.rowconfigure(row, weight=1)
        lbl = tk.Label(master=frm, text="end date", anchor=tk.W)
        lbl.grid(row=row, column=0, pady=5, padx=5, sticky=tk.EW)
        
        self._ent_edate = tk.StringVar(master=frm, value='today')
        ent_edate = tk.Entry(master=frm, width=12, validate='key', textvariable=self._ent_edate)
        ent_edate['validatecommand'] = (ent_edate.register(mpv._validDateMMDDYYYY),'%S','%d','%P')
        ent_edate.grid(row=row, column=1, pady=5, padx=5, sticky=tk.EW)
        config.tiptil.bind(ent_edate, configTips._sew_edate_tip)
        
        lbl = tk.Label(master=frm, text="Provider", anchor=tk.W)
        lbl.grid(row=row, column=2, pady=5, sticky=tk.EW)
        
        pval = list(configSettings.MasterApplicationSettings["Provider"].keys())
        self._ent_provider = tk.StringVar(master=frm)
        ent_provider = ttk.Combobox(master=frm, width=20, textvariable=self._ent_provider)
        ent_provider["values"] = pval
        ent_provider.current(0) 
        ent_provider.grid(row=row, column=3, pady=5, padx=5, sticky=tk.EW)
        config.tiptil.bind(ent_provider, configTips._sew_provider_tip)
        
        row += 1
        frm.rowconfigure(row, weight=1)
        lbl = tk.Label(master=frm, text="start date", anchor=tk.W)
        lbl.grid(row=row, column=0, pady=5, padx=5, sticky=tk.EW)
        
        self._ent_sdate = tk.StringVar(master=frm, value=None if validate else '1/1/2012')
        ent_sdate = tk.Entry(master=frm, width=12, validate='key', textvariable=self._ent_sdate)
        ent_sdate['validatecommand'] = (ent_sdate.register(mpv._validDateMMDDYYYY),'%S','%d','%P')
        ent_sdate.grid(row=row, column=1, pady=5, padx=5, sticky=tk.EW)
        config.tiptil.bind(ent_sdate, configTips._sew_sdate_tip)
        
        frm_chk = tk.Frame(master=frm)
        frm_chk.grid(row=row, column=3, pady=5, padx=5, sticky=tk.EW)
        
        lbl = tk.Label(master=frm_chk, text="force", anchor=tk.W)
        lbl.pack(padx=5, pady=5, side=tk.LEFT)
        
        self._ent_force = tk.BooleanVar(value=False)
        chk = tk.Checkbutton(master=frm_chk, onvalue=True, offvalue=False, variable=self._ent_force)
        chk.pack(padx=5, pady=5, side=tk.RIGHT)
        config.tiptil.bind(chk, configTips._sew_force_tip)
        
        frm_btn = tk.Frame(master=self._window)
        frm_btn.pack(fill=tk.BOTH, expand=True)
        
        btn = tk.Button(master=frm_btn, text="Cancel", width=12, command=self._btn_cancel_func)
        btn.pack(pady=5, padx=5, side=tk.LEFT)
        
        btn = tk.Button(master=frm_btn, text=btn_text, width=12, command=self._btn_extract_func)
        btn.pack(pady=5, padx=5, side=tk.RIGHT)
        
        self._window.update()
        self._master.wait_window(self._window)
        
        
    def _btn_cancel_func(self):
        self._window.grab_release()
        if (self._master is not None) and self._master.winfo_exists(): 
            self._master.focus_set()
        self._window.destroy()
    
    
    def _btn_extract_func(self):
        if self._entry:
            stat, self._symbols = mpv._validate_symbols(self._ent_symb.get().upper().split(','))
            if len(self._symbols) < 1: return
            
        source = self._ent_provider.get()
        force = self._ent_force.get()
        
        edate = self._ent_edate.get()
        sdate = self._ent_sdate.get()

        state, sd, ed = sdate_edate_validate(sdate, edate)
        if not state:
            tk.messagebox.showwarning("Warning", sd, parent=self._window)
            return
        
        gmd = GetMktData(source, force, validate=self._validate)
        gmd.getMkTDataSymb(self._symbols, sd, ed)
        self.symbols = gmd.symbols
        self.errorSymb = gmd.errorsymb
        self._btn_cancel_func()
