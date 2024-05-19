import tkinter as tk
from copy import deepcopy

import azapyGUI.config as config
import azapyGUI.configSettings as configSettings
from azapyGUI.serviceMasterUserConfig import _saveMasterUserConfig

class AppSettingsPageMisc(tk.Frame):
    def __init__(self, master):
        self._master = master
        super().__init__(self._master)
        
        self._window = self
        self._category = "Miscellaneous"
        
        title = "Miscellaneous"
        frm_set = tk.LabelFrame(master=self._window, text=title, font=("Forte", 10))
        frm_set.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self._window.rowconfigure(0, weight=1)
        self._window.columnconfigure(0, weight=1)
        frm_set.columnconfigure(0, weight=1)
        frm_set.columnconfigure(1, weight=1)
        
        frm_btn = tk.Frame(master=self._window)
        frm_btn.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)
        
        # on frm
        self._setDef = configSettings.settings_model[self._category]
        #self.settings = deepcopy(configSettings.MasterApplicationSettings)
        self.settings = {key: configSettings.MasterApplicationSettings[key] for key in self._setDef.keys()}
        row = 0
        self._chk_val = {}
        self._chk_btn = {}
        for param, value in self._setDef.items():
            match value["type"]:
                case 'Checkbutton':
                    lbl = tk.Label(master=frm_set, text=value["field"], anchor=tk.W)
                    lbl.grid(row=row, column=0, padx=5, pady=5, sticky=tk.EW)
                    chk_var = tk.BooleanVar(master=frm_set, value=self.settings[param])
                    chk_btn = tk.Checkbutton(master=frm_set, variable = chk_var, 
                                             onvalue = True, offvalue = False, 
                                             height=2, width=18, anchor=tk.W)
                    chk_btn.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                    self._chk_val[param] = chk_var
                    self._chk_btn[param] = chk_btn
                    config.tiptil.bind(chk_btn, value["tip"])
                    row += 1
                case 'Entry':
                    lbl = tk.Label(master=frm_set, text=value["field"], anchor=tk.W)
                    lbl.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
                    ent_var = tk.StringVar(master=frm_set, value=self.settings[param])
                    ent = tk.Entry(master=frm_set, textvariable=ent_var, validate='key', width=10)
                    ent['validatecommand'] = (ent.register(value["validate"]),'%S','%d','%P')
                    ent.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
                    self._chk_val[param] = ent_var
                    config.tiptil.bind(ent, value["tip"])
                    row += 1
                case _:
                    # you should not be here
                    raise ValueError("Error: Unknown configSetting type")
                    
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
        
        
    def _btn_cancel_func(self):
        if self._master.winfo_exists():
            self._master.grab_release()
        self._master.destroy()
        
        
    def _btn_reset_func(self):
        for kk, vv in self._setDef.items():
            self.settings[kk] = deepcopy(vv["default"])
            match vv["type"]:
                case "Checkbutton":
                    if self.settings[kk]:
                        self._chk_btn[kk].select()
                    else:
                        self._chk_btn[kk].deselect()
                case "Entry":
                    self._chk_val[kk].set(self.settings[kk])
        
        
    def _btn_save_func(self):
        self.settings.update({key: self._chk_val[key].get() for key in self._chk_val.keys()})
        configSettings.MasterApplicationSettings.update(self.settings)
        _saveMasterUserConfig(configSettings.MasterApplicationSettings)
        config.tiptil.turned(on=configSettings.MasterApplicationSettings["ShowTips"])

                    