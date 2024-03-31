import tkinter as tk 
from tkinter import ttk
import webbrowser

import azapyGUI.configModels as configModels
import azapyGUI.config as config


class ModelParamEditWindow:
    def __init__(self, model_name, param=None, model_family=None, master=None):
        self._master = master
        self._model_name = model_name
        self._model_family = model_family if model_family is not None else configModels.get_model_family(self._model_name)
        
        pdefault = configModels.param_default(model_name)
        self.param = pdefault if param is None else (pdefault.update(param) or pdefault)      
        self._param_invisible = configModels.param_default(model_name, visible=False)
        
        self._window = tk.Toplevel() 
        str_title = self._model_name + " - Parameters"
        self._window.title(str_title)
        self._window.focus_set()
        self._window.grab_set()

        menubar = tk.Menu(self._window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Help', command=self._menu_help_func)
        menubar.add_cascade(label='Help', menu=filemenu)
        self._window.config(menu=menubar)
        
        frm_model = tk.LabelFrame(master=self._window, text=str_title, font=("Forte", 10))
        frm_model.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        
        self._frm = tk.Frame(master=frm_model)
        self._frm.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        self._frm.columnconfigure(1, weight=1)
        
        config_param = configModels.portfolio_model_family[self._model_family][self._model_name]['param']
        row = 0
        self._ent_dict = {}
        for kk, vv in config_param.items():
            row = self._insert_item(kk, vv, row)
                
        frm_btn = tk.Frame(master=frm_model)
        frm_btn.pack(fill=tk.BOTH, padx=5, pady=5)
        
        btn_cancel = tk.Button(master=frm_btn, text="Cancel", width=10, command=self._btn_cancel)
        btn_cancel.pack(side="left", padx=5, pady=5)
        
        btn_save = tk.Button(master=frm_btn, text="Save", width=10, command=self._btn_save)
        btn_save.pack(side="right", padx=5, pady=5)
        
        self._window.update()
        self._master.wait_window(self._window)
        
        
    def _insert_item(self, kk, vv, row):
        if not vv['visible']: return row
        
        lbl = tk.Label(master=self._frm, text=kk, width=10, anchor='w')
        lbl.grid(row=row, column=0, padx=2, pady=0, sticky=tk.W )
        
        if 'values' not in vv.keys():
            ent = tk.Entry(master=self._frm, width=15)
            ent.grid(row=row, column=1, padx=2, pady=0, sticky=tk.EW)
            ent.insert(0, str(self.param[kk]))
            config.tiptil.bind(ent, vv['tip'])
            self._ent_dict[kk] = ent
 
            self._frm.rowconfigure(row, weight=1)
        else:
            ent = ttk.Combobox(master=self._frm, width=12, state='readonly')
            ent['values'] = vv['values']
            ent.set(str(self.param[kk]))
            ent.grid(row=row, column=1, padx=2, pady=0, sticky=tk.EW )
            config.tiptil.bind(ent, vv['tip'])
            self._ent_dict[kk] = ent
 
            self._frm.rowconfigure(row, weight=1)

            if 'param' in vv.keys():
                row += 1
                ent.bind("<<ComboboxSelected>>", lambda event: self._switch_item(kk=kk, vv=vv, row=row))
                for kkk, vvv in vv['param'].items():
                    self._insert_item(kkk, vvv, row)
                self._switch_item(kk, vv, row)
        
        return row + 1
                
    
    def _switch_item(self, kk, vv, row):
        sol = self._ent_dict[kk].get()
        
        lbl = tk.Label(master=self._frm, text="", width=10, anchor='w')
        lbl.grid(row=row, column=0, padx=2, pady=0, sticky=tk.W )
        for kkk, vvv in vv['param'].items():
            self._ent_dict[kkk].grid_forget()
            if sol in vvv['conditional']:
                lbl.config(text=kkk)
                self._ent_dict[kkk].grid(row=row, column=1, padx=2, pady=0, sticky=tk.EW)


    def _btn_cancel(self):
        self._window.grab_release()
        if (self._master is not None) and self._master.winfo_exists(): 
            self._master.focus_set()
        self._window.destroy()
        self.param = None
    
    
    def _btn_save(self):
        wparam = {}
        for kk in self._ent_dict.keys():
            if self._ent_dict[kk].winfo_ismapped():
                wparam[kk] = self._ent_dict[kk].get()

        status = self._validate(wparam)
        if not status: return
        
        self._param_invisible.update(wparam)
        self.param = self._param_invisible
        self._window.grab_release()
        if (self._master is not None) and self._master.winfo_exists():
            self._master.focus_set()
        self._window.destroy()


    def _validate(self, param):
        dparam = configModels.flat_param_default(self._model_family, self._model_name)
        lmodel = configModels.portfolio_model_family[self._model_family][self._model_name]['val_priority']
        lmodel += [kk for kk in param.keys() if kk not in lmodel]
        rout = {}
        for kk in lmodel:
            status, rout = dparam[kk]['validate'](param)
            if not status:
                tk.messagebox.showwarning("Warning", rout, parent=self._window)
                return False
        return True


    def _menu_help_func(self):
        webbrowser.open_new_tab(configModels.portfolio_model_family[self._model_family][self._model_name]['help'])
    