import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from copy import deepcopy

import azapyGUI.configSettings as configSettings
import azapyGUI.config as config
import azapyGUI.configMSG as configMSG
from azapyGUI.serviceMasterUserConfig import _saveMasterUserConfig

class AppSettingsPage(tk.Frame):
    def __init__(self, master, category, title):
        self._master = master
        self._category = category
        super().__init__(self._master)
        
        self._window = self
        
        frm = tk.LabelFrame(master=self._window, text=title, font=("Forte", 10))
        frm.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self._window.rowconfigure(0, weight=1)
        self._window.columnconfigure(0, weight=1)
        
        frm_btn = tk.Frame(master=self._window)
        frm_btn.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)
        
        # on frm
        frm_set = tk.Frame(master=frm)
        frm_set.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NS)
        frm.rowconfigure(0, weight=1)
        
        frm_view = tk.Frame(master=frm, width=150)
        frm_view.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
        frm.columnconfigure(1, weight=1)
        
        # on frm_set
        self._setDef = configSettings.settings_model[self._category]
        #self.settings = deepcopy(configSettings.MasterApplicationSettings)
        self.settings = {key: configSettings.MasterApplicationSettings[key] for key in self._setDef.keys()}
        row = 0
        self._chk_val = {}
        self._chk_btn = {}
        for param, value in self._setDef.items():
            match value["type"]:
                case 'ButtonDir':
                    btn = tk.Button(master=frm_set, text=value['field'], width=18, 
                                    command=lambda pp=param: self._get_directory_func(pp))
                    btn.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
                    config.tiptil.bind(btn, value["tip"])
                    row += 1
                case 'Checkbutton':
                    chk_var = tk.BooleanVar(master=frm_set, value=self.settings[param])
                    chk_btn = tk.Checkbutton(master=frm_set, text=value["field"],
                                             variable = chk_var, 
                                             onvalue = True, offvalue = False, 
                                             height=2, width=18,
                                             command=lambda pp=param: self._chk_btn_func(pp),
                                             anchor=tk.W)
                    chk_btn.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
                    self._chk_val[param] = chk_var
                    self._chk_btn[param] = chk_btn
                    config.tiptil.bind(chk_btn, value["tip"])
                    row += 1
                case 'MCheckbutton':
                    frm_chk = tk.LabelFrame(master=frm_set, text=value["field"])
                    frm_chk.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
                    row += 1
                    row_chk = 0
                    self._chk_val[param] = {}
                    self._chk_btn[param] = {}
                    for param_chk, value_chk in value["values"].items():
                        chk_var = tk.BooleanVar(master=frm_chk,
                            value=True if param_chk in self.settings[param].keys() else False)
                        chk_btn = tk.Checkbutton(master=frm_chk, text=param_chk,
                                                 variable = chk_var, 
                                                 onvalue = True, offvalue = False, 
                                                 height=2, width=18,
                                                 command=lambda param=param, pp=param_chk: self._mchk_btn_func(param, pp),
                                                 anchor=tk.W)
                        chk_btn.grid(row=row_chk, column=0, padx=5, pady=0, sticky=tk.W)
                        self._chk_val[param][param_chk] = chk_var
                        self._chk_btn[param][param_chk] = chk_btn
                        row_chk += 1
                case _:
                    # you should not be here
                    raise ValueError("Error: Unknown configSetting type")

        # on frm_view
        self._stv = ttk.Treeview(master=frm_view, selectmode="browse", show="tree")
        self._stv.pack(padx=0, pady=0, expand=True, side=tk.LEFT, fill=tk.BOTH)
        self._stv_write()
                
        vscrlb = ttk.Scrollbar(master=frm_view, 
                               orient ="vertical", 
                               command = self._stv.yview)
        vscrlb.pack(padx=0, pady=2, side=tk.RIGHT, fill=tk.Y)
        self._stv.configure(yscrollcommand = vscrlb.set)
        
        # on frm_btn
        btn_cancel = tk.Button(master=frm_btn, text="Cancel/Exit", width=12, 
                               command=self._btn_cancel_func)
        btn_cancel.pack(padx=5, pady=5, side=tk.LEFT)
        
        btn_save = tk.Button(master=frm_btn, text="Save", width=12, 
                             command=self._btn_save_func)
        btn_save.pack(padx=5, pady=5, side=tk.RIGHT)
        
        btn_reset = tk.Button(master=frm_btn, text="Default Values", width=12, 
                              command=self._btn_reset_func)
        btn_reset.pack(padx=5, pady=5, side=tk.LEFT)
    

    def _stv_write(self):
        for kk in self._setDef.keys():
            val = self.settings[kk]
            item = self._stv.insert("", tk.END, text=self._setDef[kk]["field"] + ":", open=True)
            if isinstance(val, dict):
                for subkk, subval in val.items():
                    subitem = self._stv.insert(item, tk.END, text=subkk, open=True)
                    for subsubkk, subsubval in subval.items():
                        self._stv.insert(subitem, tk.END, text=subsubkk +" = "+ str(subsubval))
            else:
                self._stv.insert(item, tk.END, text=str(val))   
                
                
    def _stv_refresh(self):
        for item in self._stv.get_children():
            self._stv.delete(item)
        self._stv_write()


    def _get_directory_func(self, param=None):
        title = self._setDef[param]["title"]
        folder_selected = filedialog.askdirectory(parent=self._window, title=title)
        if folder_selected:
            self.settings[param] = folder_selected
        self._stv_refresh()
        
        
    def _chk_btn_func(self, param):
        self.settings[param] = self._chk_val[param].get()
        self._stv_refresh()
 
        
    def _mchk_btn_func(self, param, pp):
        if self._chk_val[param][pp].get():
            self.settings[param][pp] = {}
            for kk, vv in self._setDef[param]["values"][pp].items():
                match vv['type']:
                    case 'str':
                        vpar = tk.simpledialog.askstring(pp, vv["field"], 
                                                         parent=self._window, 
                                                         initialvalue=vv["default"])
                        if vpar == '':
                            vpar = configSettings.get_envkey(pp)
                            if vpar is None:
                                msg = (configMSG._validate_provider_key_msg
                                       +'\n' 
                                       + configSettings.get_envkey_vriable_name(pp))
                                tk.messagebox.showwarning(title="Warning", message=msg, parent=self._window)
                                del self.settings[param][pp]
                                self._chk_btn[param][pp].deselect()
                                return
                        self.settings[param][pp][kk] = vpar
                    case 'int':
                        vpar = tk.simpledialog.askinteger(pp, vv["field"], 
                                                          parent=self._window, 
                                                          initialvalue=vv["default"], 
                                                          minvalue=1)
                        self.settings[param][pp][kk] = vpar
                    case 'float':
                        vpar = tk.simpledialog.askfloat(pp, vv["field"], 
                                                        parent=self._window, 
                                                        initialvalue=vv["default"], 
                                                        minvalue=1)
                        self.settings[param][pp][kk] = vpar
                    case _:
                       # you should not be here
                       raise ValueError("Error: in AppSettingWindow::_chk_bth_func wrong type") 
        else:
            del self.settings[param][pp]
        self._stv_refresh()
        
        
    def _btn_cancel_func(self):
        if self._master.winfo_exists():
            self._master.grab_release()
        self._master.destroy()
        
        
    def _btn_save_func(self):
        configSettings.MasterApplicationSettings.update(self.settings)
        _saveMasterUserConfig(configSettings.MasterApplicationSettings) 

        
    def _btn_reset_func(self):
        for kk, vv in self._setDef.items():
            self.settings[kk] = deepcopy(vv["default"])
            match vv["type"]:
                case "Checkbutton":
                    if self.settings[kk]:
                        self._chk_btn[kk].select()
                    else:
                        self._chk_btn[kk].deselect()
                case "MCheckbutton":
                    for ll in self._setDef[kk]["values"].keys():
                        if ll in self.settings[kk].keys():
                            self._chk_btn[kk][ll].select()
                        else:
                            self._chk_btn[kk][ll].deselect()
        self._stv_refresh()
        