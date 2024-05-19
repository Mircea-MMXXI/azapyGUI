import tkinter as tk
from tkinter import ttk
from copy import deepcopy
import webbrowser

import azapyGUI.config as config
import azapyGUI.configMSG as configMSG
import azapyGUI.configModels as configModels
import azapyGUI.configSettings as configSettings
import azapyGUI.configTips as configTips
import azapyGUI.configHelps as configHelps
import azapyGUI.modelParametersValidation as mpv
from azapyGUI.SymbTableEntry import SymbTableEntry
from azapyGUI.ModelParamEditWindow import ModelParamEditWindow
from azapyGUI.PortDataNode import PortDataNode
from azapyGUI.SymbExtractWindow import SymbExtractWindow
from azapyGUI.mktDataValidation import sdate_edate_validate
from azapyGUI.GetMktData import GetMktData


class EditPortfolioWindow:
    def __init__(self, master=None, portfolio=None):
        self._master = master
        if portfolio is not None:
            portfolio.status = 'Edit'
            config.appPortfolioFrame.refresh()
        self._initial_portfolio_name = None if portfolio is None else portfolio.name
        self.portfolio = deepcopy(portfolio) if portfolio is not None else PortDataNode()
        
        self._window = tk.Toplevel() 
        self._window.geometry("800x400")
        self._window.focus_set()
        self._window.title("Portfolio Edit")
        self._window.protocol("WM_DELETE_WINDOW", self._btn_cancel)
        
        menubar = tk.Menu(self._window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Help', command=self._menu_help_func)
        menubar.add_cascade(label='Help', menu=filemenu)
        self._window.config(menu=menubar)
         
        self._build()
        
        self._window.update()
        self._master.wait_window(self._window)
        
        
    def _build(self):
        frm_name = tk.Frame(master=self._window)
        frm_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        lbl_text = "Edit Portfolio: " 
        lbl_port = tk.Label(master=frm_name, text=lbl_text, justify='left', font=("Harlow Solid Italic", 12))
        lbl_port.pack(side='left', pady=5, padx=2)
        self._ent_name = tk.Entry(master=frm_name, width=30)
        self._ent_name.pack(side='right', pady=5, padx=2)
        self._ent_name.insert(0, self.portfolio.name)
        config.tiptil.bind(self._ent_name, configTips._epw_portfolio_name_tip)
        
        self._build_symbPanel()
        self._build_modelPanel()
        
        frm_btn_done = tk.Frame(master=self._window)
        frm_btn_done.grid(row=2, columnspan=2, padx=5, pady=5, sticky=tk.EW)
        
        btn_set = tk.Button(master=frm_btn_done, text=" Set ", width=10, command=self._btn_set)
        btn_set.pack(side=tk.RIGHT, padx=10, pady=5)
        btn_cancel = tk.Button(master=frm_btn_done, text="Cancel", width=10, command=self._btn_cancel)
        btn_cancel.pack(side=tk.LEFT, padx=10, pady=5)
        
        
    def _build_symbPanel(self):
        # -- symb panel
        symbPanel = tk.LabelFrame(master=self._window, width=300, text="Portfolio components", font=("Forte", 10))  
        symbPanel.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        
        self._window.rowconfigure(1, weight=1)
        self._window.columnconfigure(0, weight=1)
        
        frm_symb_btn = tk.Frame(master=symbPanel)
        frm_symb_btn.grid(row=0, column=0, sticky=tk.EW)
        
        btn_refresh = tk.Button(master=frm_symb_btn, text="Refresh", width=8, command=self._btn_refresh)
        btn_refresh.pack(side=tk.LEFT, padx=2, pady=5)

        btn_validate = tk.Button(master=frm_symb_btn, text="Validate", width=8, command=self._btn_symb_validate)
        btn_validate.pack(side=tk.RIGHT, padx=2, pady=5)
        
        self._symb_table = SymbTableEntry(master=symbPanel, )
        self._symb_table.grid(row=1, column=0, sticky=tk.NSEW)
        symbPanel.rowconfigure(1, weight=1)
        symbPanel.columnconfigure(0, weight=1)
        self._symb_table.write_order(self.portfolio.symbols)
        
        self._window.bind('<KeyPress>', self._symb_table.key_press)
        
        
    def _build_modelPanel(self):
        # -- model panel
        modelPanel = tk.LabelFrame(master=self._window, text="Optimization model", width=400, font=("Forte", 10))
        modelPanel.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)
        self._window.columnconfigure(1, weight=1)
        
        frm_choice = tk.Frame(master=modelPanel)
        frm_choice.pack(side='left', pady=2, expand=True, fill=tk.Y)
        
        tk.Label(master=frm_choice, text="Selector:").pack(padx=2, pady=2, side='top', anchor="w")
        self._cbx_selector = ttk.Combobox(master=frm_choice, width=20, state='readonly')
        self._cbx_selector['values'] = tuple(configModels.selector_models.keys())
        self._cbx_selector.current(0)
        self._cbx_selector.pack(pady=5, padx=5, side='top',)
        self._cbx_selector.bind("<<ComboboxSelected>>", self._cbx_selector_func)
        
        tk.Label(master=frm_choice, text="Optimization type:").pack(padx=2, pady=2, side='top', anchor="w")
        self._cbx_optim_type = ttk.Combobox(master=frm_choice, width=20, state='readonly')
        self._cbx_optim_type['values'] = tuple(configModels.optim_model_types)
        self._cbx_optim_type.current(0)
        self._cbx_optim_type.pack(pady=5, padx=5, side='top',)
        self._cbx_optim_type.bind("<<ComboboxSelected>>", self._cbx_optim_type_func)
        
        tk.Label(master=frm_choice, text="Optimization model:").pack(padx=2, pady=2, side='top', anchor="w")
        self._cbx_optim_model = ttk.Combobox(master=frm_choice, width=20, state='readonly')
        self._cbx_optim_model['values'] = tuple(configModels.risk_based_models.keys())
        self._cbx_optim_model.current(0)
        self._cbx_optim_model.pack(pady=5, padx=5, side='top',)
        self._cbx_optim_model.bind("<<ComboboxSelected>>", self._cbx_optim_model_func)
        
        frm_view = tk.Frame(master=modelPanel, width=150)
        frm_view.pack(side='right', expand=True, pady=2, fill=tk.BOTH)
        
        self._tree_model = ttk.Treeview(master=frm_view, selectmode="browse", show="tree")
        self._tree_model.pack(padx=0, pady=0, expand=True, side=tk.LEFT, fill=tk.BOTH)
        self._tree_model.tag_bind("m_selector", "<<TreeviewSelect>>", self._tree_model_item_selector_func)
        self._tree_model.tag_bind("m_optimizer", "<<TreeviewSelect>>", self._tree_model_item_optimizer_func)
        
        vscrlb = ttk.Scrollbar(master=frm_view, 
                               orient ="vertical", 
                               command = self._tree_model.yview)
        vscrlb.pack(padx=0, pady=2, side=tk.RIGHT, fill=tk.Y)
        self._tree_model.configure(yscrollcommand = vscrlb.set)
        self._tree_model_write()
        
        self._set_tree_menu_selector()
        self._set_tree_menu_optimizer()
        
        
    def _tree_model_write(self):
        for name, selector in self.portfolio.selectors.items():
            item = self._tree_model.insert("", selector['index'], text=name, tags=("m_selector",))
            invisible = configModels.param_default(name, visible=False)
            for kk, vv in selector['param'].items():
                if kk in invisible: continue
                self._tree_model.insert(item, tk.END, text=kk +" = "+ str(vv)) 
                
        for name, optimizer in self.portfolio.optimizer.items():
            item = self._tree_model.insert("", tk.END, text=name, tags=("m_optimizer",)) 
            invisible = configModels.param_default(name, visible=False)
            for kk, vv in optimizer['param'].items():
                if kk in invisible: continue
                self._tree_model.insert(item, tk.END, text=kk +" = "+ str(vv))
        
        
    def _set_tree_menu_selector(self):
        self._tree_menu_selector = tk.Menu(self._tree_model, tearoff = 0) 
        self._tree_menu_selector.add_command(label ="Edit", command=self._tree_menu_selector_edit_func) 
        self._tree_menu_selector.add_command(label ="Move Up", command=self._tree_menu_selector_moveup_func) 
        self._tree_menu_selector.add_command(label ="Move Down", command=self._tree_menu_selector_movedown_func) 
        self._tree_menu_selector.add_separator() 
        self._tree_menu_selector.add_command(label ="Delete", command=self._tree_menu_selector_delete_func) 
        
        
    def _tree_menu_selector_edit_func(self):
        iid = self._tree_model.selection()[0]
        model = self._tree_model.item(iid)['text']

        selw = ModelParamEditWindow(model_name=model, 
                                    param=self.portfolio.get_selector(model)['param'],
                                    master=self._window)
        param = selw.param
        if param is None: return
        
        self.portfolio.update_selector(model, param)
        
        for child in self._tree_model.get_children(iid):
            self._tree_model.delete(child)
            
        invisible = configModels.param_default(model, visible=False)
        for kk, vv in param.items():
            if kk in invisible: continue
            self._tree_model.insert(iid, tk.END, text=kk +" = "+ str(vv))
    
    
    def _tree_menu_selector_moveup_func(self):
        item = self._tree_model.selection()[0]
        loc = self._tree_model.index(item)
        item_name = self._tree_model.item(item)['text']
        
        self.portfolio.moveUp_selector(item_name)
        self._tree_model.move(item, self._tree_model.parent(item), loc - 1)
    
    
    def _tree_menu_selector_movedown_func(self):
        item = self._tree_model.selection()[0]
        loc = self._tree_model.index(item)
        new_loc = loc + 1
        
        if new_loc >= self.portfolio.number_selector(): return
        item_name = self._tree_model.item(item)['text']
        self.portfolio.moveDown_selector(item_name)
        self._tree_model.move(item, self._tree_model.parent(item), new_loc)
    
    
    def _tree_menu_selector_delete_func(self):
        item = self._tree_model.selection()[0]
        item_name = self._tree_model.item(item)['text']
        self.portfolio.remove_selector(item_name)
        self._tree_model.delete(item)
        
        
    def _set_tree_menu_optimizer(self):
        self._tree_menu_optimizer = tk.Menu(self._tree_model, tearoff = 0) 
        self._tree_menu_optimizer.add_command(label ="Edit", command=self._tree_menu_optimizer_edit_func) 
        self._tree_menu_optimizer.add_separator() 
        self._tree_menu_optimizer.add_command(label ="Delete", command=self._tree_menu_optimizer_delete_func) 
        

    def _tree_menu_optimizer_edit_func(self):
        iid = self._tree_model.selection()[0]
        model = self._tree_model.item(iid)['text']
        
        selw = ModelParamEditWindow(model_name=model, 
                                    param=self.portfolio.get_optimizer()['param'],
                                    master=self._window)
        param = selw.param
        if param is None: return
        
        self.portfolio.update_optimizer(param)
        
        for child in self._tree_model.get_children(iid):
            self._tree_model.delete(child)
            
        invisible = configModels.param_default(model, visible=False)
        for kk, vv in param.items():
            if kk in invisible: continue
            self._tree_model.insert(iid, tk.END, text=kk +" = "+ str(vv))
            
    
    def _tree_menu_optimizer_delete_func(self):
        item = self._tree_model.selection()[0]
        self.portfolio.remove_optimizer()
        self._tree_model.delete(item)


    def _tree_model_item_selector_func(self, event):
        try: 
            self._tree_menu_selector.tk_popup(self._tree_menu_selector.winfo_pointerx(), 
                                              self._tree_menu_selector.winfo_pointery()) 
        finally: 
            self._tree_menu_selector.grab_release() 
        
        
    def _tree_model_item_optimizer_func(self, event):
        try: 
            self._tree_menu_optimizer.tk_popup(self._tree_menu_optimizer.winfo_pointerx(), 
                                               self._tree_menu_optimizer.winfo_pointery()) 
        finally: 
            self._tree_menu_optimizer.grab_release() 
        
        
    def _cbx_selector_func(self, event):
        selo = self._cbx_selector.get()
        if selo == 'Null': return
        
        for kk in self.portfolio.optimizer.keys():
            if configModels.get_comptype(kk) == 'standalone':
                msg = f"The optimizer {kk} doesn't accept selectors. "
                tk.messagebox.showwarning("Warning", message=msg, parent=self._window)
                return
        
        if self.portfolio.is_set_selector(selo):
            tk.messagebox.showwarning("warning", "Already selected", parent=self._window)
            return
        
        selw = ModelParamEditWindow(master=self._window, model_name=selo)
        param = selw.param
        if param is None: return
        
        self.portfolio.add_selector(name=selo, param=param)
 
        loc = self.portfolio.number_selector() - 1
        item = self._tree_model.insert("", loc, text=selo, tags=("m_selector",))
        invisible = configModels.param_default(selo, visible=False)
        for kk, vv in param.items():
            if kk in invisible: continue
            self._tree_model.insert(item, tk.END, text=kk +" = "+ str(vv))
        
        
    def _cbx_optim_type_func(self, event):
        selo = self._cbx_optim_type.get()
        
        if selo == 'Risk based':
            self._cbx_optim_model['values'] = list(configModels.risk_based_models.keys())
            self._cbx_optim_model.current(0)
        elif selo == 'Naive':
            self._cbx_optim_model['values'] = list(configModels.naive_models.keys())
            self._cbx_optim_model.current(0)
        elif selo == 'Greedy':
            self._cbx_optim_model['values'] = list(configModels.greedy_models.keys())
            self._cbx_optim_model.current(0)
            
            
    def _cbx_optim_model_func(self, event):
        selo = self._cbx_optim_model.get()

        if self.portfolio.is_set_optimizer():
            msg = "The optimizer is already set. Only one optimizer is allowed."
            tk.messagebox.showwarning("warning", message=msg, parent=self._window)
            return
        
        if len(self.portfolio.selectors.keys()) > 0:
            if configModels.get_comptype(selo) == 'standalone':
                msg = (f"The optimizer {selo} doesn’t accept selectors.\n"
                       "Do you want to remove the selectors?")
                ans = tk.messagebox.askyesno("Warning", message=msg, parent=self._window)
                if not ans: return
                self._tree_model.delete(*self._tree_model.get_children())
                self.portfolio.selectors = {}
        
        selw = ModelParamEditWindow(master=self._window, model_name=selo)
        param = selw.param
        if param is None: return

        self.portfolio.add_optimizer(name=selo, param=param)

        item = self._tree_model.insert("", tk.END, text=selo, tags=("m_optimizer",))
        invisible = configModels.param_default(selo, visible=False)
        for kk, vv in param.items():
            if kk in invisible.keys(): continue
            self._tree_model.insert(item, tk.END, text=kk +" = "+ str(vv))
        
        
    def _btn_refresh(self):
        _, tx = self._symb_table.get()
        self._symb_table.write_order(tx)
        
    
    def _btn_cancel(self):
        if self._initial_portfolio_name is not None:
            config.PortDataDict[self._initial_portfolio_name].status = 'Set'
            config.appPortfolioFrame.refresh()
            
        self._window.grab_release()
        if (self._master is not None) and self._master.winfo_exists():
            self._master.focus_set()
        self._window.destroy()
        self.portfolio = None
        
        
    def _on_exit(self):
        self._btn_cancel()

        
    def _btn_set(self):
        # portfolio name
        pname = self._ent_name.get()
        status, val = mpv._validate_portfolio_name(pname)
        if not status:
            tk.messagebox.showwarning("Warning", val, parent=self._window)
            return
        
        if ((val != self._initial_portfolio_name) and (val in config.PortDataDict.keys())):
            tk.messagebox.showwarning("Warning", configMSG._validate_portfolio_name_exist_msg, 
                                      parent=self._window)
            return       
        
        self.portfolio.name = val
        
        # symbols
        status, tx = self._symb_table.get()   
        if (not status) or (len(tx) < 1):
            tk.messagebox.showwarning("Warning", configMSG._validate_symbols_name_msg, 
                                      parent=self._window)
            return

        # validate symbols
        source = list(configSettings.MasterApplicationSettings["Provider"].keys())[0]
        _, sd, ed = sdate_edate_validate('', 'today')
 
        gmd = GetMktData(source, force=False, validate=True)
        gmd.getMkTDataSymb(tx, sd, ed)
        symbols = gmd.symbols
        error_symbols = gmd.errorsymb
 
        self._symb_table.write_order(symbols)
        if len(error_symbols) > 0:
            msg = configMSG._validate_symbols_final_msg + '\n' + str(error_symbols)
            tk.messagebox.showwarning("Warning", msg, parent=self._window)
        
        if len(symbols) == 0:
            tk.messagebox.showwarning("Warning", configMSG._validate_symbols_nr_msg, 
                                      parent=self._window)
            return

        self.portfolio.set_symbol(symbols)
        nsymb = self.portfolio.number_symmbols()

        # selectors
        selectors = self.portfolio.to_list_selector()
        for sel in selectors:          
            model_name = sel['name']
            for fun in configModels.selector_models[model_name]['validate']:
                param_name = list(fun.keys())[0]
                if param_name not in sel['param'].keys(): continue
                status, val = list(fun.values())[0](sel['param'], nsymb)
                if not status:
                    msg = f"In {model_name}::{param_name}\n{val}"
                    tk.messagebox.showwarning("Warning", msg, parent = self._window)
                    return
                sel['param'][param_name] = val
            self.portfolio.update_selector(model_name, sel['param'])
          
        # optimizer
        optimizer = self.portfolio.get_optimizer()
        if optimizer is None:
            tk.messagebox.showwarning("Warning", configMSG._validate_portfolio_optimizer_msg, 
                                      parent=self._window)
            return
        
        model_name = optimizer['name']
        model_family = configModels.get_model_family(model_name)
        for fun in configModels.portfolio_model_family[model_family][model_name]['validate']:
            param_name = list(fun.keys())[0]
            if param_name not in optimizer['param'].keys(): continue
            status, val = list(fun.values())[0](optimizer['param'], nsymb)
            if not status:
                msg = "In " + model_name + "::" + param_name + "\n" + val
                tk.messagebox.showwarning("Warning", msg, parent = self._window)
                return
            optimizer['param'][param_name] = val
        self.portfolio.update_optimizer(optimizer['param'])
         
        # set
        self.portfolio.status = "Set"
        self.portfolio.saved = False
        config.PortDataDict[self.portfolio.name] = self.portfolio
        if ((self._initial_portfolio_name is not None) and
            (self._initial_portfolio_name != self.portfolio.name)):
            del config.PortDataDict[self._initial_portfolio_name]
            
        config.appPortfolioFrame.refresh()

        self._window.grab_release()
        if (self._master is not None) and self._master.winfo_exists(): 
            self._master.focus_set()
        self._window.destroy()
            
    
    def _menu_help_func(self):
        webbrowser.open_new_tab(configHelps._Portfolio_Edit_help)
    
    
    def _btn_symb_validate(self):
        _, tx = self._symb_table.get()
        if len(tx) < 1: return True
        
        title = "Symbols validation"
        btn_text = "Validate"
        svw = SymbExtractWindow(master=self._window, 
                                title=title, symbols=tx, btn_text=btn_text,
                                validate=True)
        
        if len(svw.errorSymb) < 1:
            self._symb_table.write_order(tx)
            return
        
        msg = f"These symbols cannot be retrieved.\n{svw.errorSymb}\nDo you want to delete them?"
        askr = tk.messagebox.askyesno("Validation Failed", msg, parent=self._window)
        self._symb_table.write_order(svw.symbols if askr else tx)
    