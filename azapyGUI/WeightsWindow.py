import tkinter as tk 
from tkinter import ttk
import pandas as pd 
import numpy as np
from copy import deepcopy
import webbrowser
import azapy as az

import azapyGUI.config as config
import azapyGUI.configSettings as configSettings
import azapyGUI.configModels as configModels
import azapyGUI.configTips as configTips
import azapyGUI.configHelps as configHelps
from azapyGUI.NrShares_table import NrShares_table
from azapyGUI.modelParametersValidation import _validDateMMDDYYYY, _validFloat
from azapyGUI.GetMktData import GetMktData
from azapyGUI.mktDataValidation import mkt_today
from azapyGUI.DF_Window import DF_Window
import azapyGUI.azHelper as azHelper


class WeightsWindow():
    def __init__(self, master, pname):
        self._master = master
        self._pname = pname
        
        self._rep_show = []
        self._dfw = None
        self._dfts = None
        self._old_param = None
        
        self._window = tk.Toplevel()
        self._window.geometry('320x340')
        title = f'Rebalance - {self._pname}'
        self._window.title(title)
        self._window.focus_set()
        self._window.protocol("WM_DELETE_WINDOW", self._btn_cancel)
        self._window.columnconfigure(0, weight=1)

        menubar = tk.Menu(self._window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Help', command=self._menu_help_func)
        menubar.add_cascade(label='Help', menu=filemenu)
        self._window.config(menu=menubar)
        
        wwi = 300
        row = 0
        self._window.rowconfigure(row, weight=0)
        frm_port = tk.Frame(master=self._window, width=wwi)
        frm_port.grid(row=row, column=0, sticky=tk.EW, padx=10, pady=10)
        
        row += 1
        self._window.rowconfigure(row, weight=1)
        frm_data = tk.Frame(master=self._window, width=wwi)
        frm_data.grid(row=row, column=0, sticky=tk.NSEW, padx=5, pady=5)
        
        row += 1
        self._window.rowconfigure(row, weight=0)
        frm_btn = tk.Frame(master=self._window, width=wwi)
        frm_btn.grid(row=row, column=0, sticky=tk.EW, padx=5, pady=5)
        
        # on frm_port
        lbl = tk.Label(master=frm_port, text='Portfolio', anchor=tk.W, font=("Forte", 10), width=8)
        lbl.pack(side=tk.LEFT)
        
        lbl = tk.Label(master=frm_port, text=self._pname, anchor=tk.W, width=10)
        lbl.pack(side=tk.LEFT)

        self._ent_asof = tk.StringVar(master=frm_port, value='today')
        ent = tk.Entry(master=frm_port, textvariable=self._ent_asof, validate='key', width=10)
        ent.pack(side=tk.RIGHT)
        ent['validatecommand'] = (ent.register(_validDateMMDDYYYY),'%S','%d','%P')
        config.tiptil.bind(ent, configTips._reb_as_of_tip)

        lbl = tk.Label(master=frm_port, text='As of', anchor=tk.W, font=("Forte", 10), width=5)
        lbl.pack(side=tk.RIGHT)
        
        # on frm_data
        frm_data.rowconfigure(0, weight=1)
        frm_data.columnconfigure(0, weight=1)
        frm_data.columnconfigure(1, weight=0)
        
        frm_left = tk.LabelFrame(master=frm_data, text='Reinv. Capital', font=("Forte", 10))
        frm_left.grid(row=0, column=0, sticky=tk.NSEW)
        
        frm_right = tk.LabelFrame(master=frm_data, text='Settings', font=("Forte", 10))
        frm_right.grid(row=0, column=1, sticky=tk.NSEW)
        
        # on frm_left
        frm_left.columnconfigure(0, weight=1)
        frm_left.columnconfigure(1, weight=1)
        
        row = 0
        frm_left.rowconfigure(row, weight=0)
        lbl = tk.Label(master=frm_left, text='Cash', width=5, anchor=tk.W)
        lbl.grid(row=row, column=0, padx=0, pady=5, sticky=tk.W)
        
        self._ent_cash = tk.DoubleVar(master=frm_left, 
                                      value=configSettings.MasterApplicationSettings['capital'])
        ent = tk.Entry(master=frm_left, textvariable=self._ent_cash, validate='key', width=8)
        ent.grid(row=row, column=1, padx=0, pady=5, sticky=tk.W, ipadx=3)
        ent['validatecommand'] = (ent.register(_validFloat),'%S','%d','%P')
        config.tiptil.bind(ent, configTips._reb_cash_tip)
        
        row += 1
        frm_left.rowconfigure(row, weight=0)
        lbl = tk.Label(master=frm_left, text='Symbol', width=6, anchor=tk.W)
        lbl.grid(row=row, column=0, padx=0, pady=5, sticky=tk.W)
        
        lbl = tk.Label(master=frm_left, text='Nr. Shares', width=8, anchor=tk.W)
        lbl.grid(row=row, column=1, padx=0, pady=5, sticky=tk.W)
        
        row += 1
        frm_left.rowconfigure(row, weight=1)
        self._symbols = config.PortDataDict[self._pname].symbols
        data = pd.Series(0, index=self._symbols)
        frm_sls = tk.Frame(master=frm_left)
        frm_sls.grid(row=row, column=0, columnspan=2, padx=0, pady=5, sticky=tk.NSEW)
        frm_sls.rowconfigure(0, weight=1)
        frm_sls.columnconfigure(0, weight=1)
        self._frm_symb = NrShares_table(master=frm_sls, data=data)
        self._frm_symb.grid(row=0, column=0, sticky=tk.NSEW)
        frm_sls.update()
        
        row += 1
        self._ent_nsh_round = tk.BooleanVar(master=frm_left, value=True)
        cbx = tk.Checkbutton(frm_left, text='NSh Int', variable=self._ent_nsh_round,
                             onvalue=True, offvalue=False, width=5, anchor=tk.W)
        cbx.grid(row=row, column=0, padx=0, pady=5, sticky=tk.W)
        config.tiptil.bind(cbx, configTips._reb_nsh_round_tip)
        
        btn = tk.Button(master=frm_left, text='Refresh', width=8, command=self._btn_refresh_func)
        btn.grid(row=row, column=1, padx=2, pady=5, sticky=tk.E)
        
        # on frm_right
        frm_right.columnconfigure(0, weight=0)
        frm_right.columnconfigure(1, weight=0)
        
        row = 0
        lbl = tk.Label(master=frm_right, text="Provider", anchor=tk.W, width=6)
        lbl.grid(row=row, column=0, padx=0, pady=5, sticky=tk.W)
        
        pval = list(configSettings.MasterApplicationSettings["Provider"].keys())
        self._ent_provider = ttk.Combobox(master=frm_right, width=12)
        self._ent_provider["values"] = pval
        self._ent_provider.current(0)
        self._ent_provider.grid(row=row, column=1, pady=5, padx=5, sticky=tk.EW)
        config.tiptil.bind(self._ent_provider, configTips._reb_provider_tip)
        
        row += 1
        lbl = tk.Label(master=frm_right, text="Force", anchor=tk.W, width=6)
        lbl.grid(row=row, column=0, padx=0, pady=5, sticky=tk.W)
        
        self._ent_force = tk.BooleanVar(value=configSettings.MasterApplicationSettings['force'])
        chk_force = tk.Checkbutton(master=frm_right, onvalue=True, offvalue=False, variable=self._ent_force)
        chk_force.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
        config.tiptil.bind(chk_force, configTips._reb_force_tip)
        
        row += 1
        btn = tk.Button(master=frm_right, text='Weights', width=10, command=self._btn_weights_func)
        btn.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
        
        # on frm_btn
        frm_btn.rowconfigure(0, weight=1)
        frm_btn.columnconfigure(0, weight=1)
        frm_btn.columnconfigure(1, weight=1)
        
        btn = tk.Button(master=frm_btn, text='Close', width=10, command=self._btn_cancel)
        btn.grid(row=0, column=0, sticky=tk.W)
        
        btn = tk.Button(master=frm_btn, text="Trading Sheet", width=14, command=self._btn_traiding_sheet_func)
        btn.grid(row=0, column=1, sticky=tk.E)
        
     
    def _mktdata_info(self):
        # edate
        asof = self._ent_asof.get()
        edate = pd.Timestamp(asof).normalize().tz_localize(None)
        edate = config._bday.rollback(edate).normalize().tz_localize(None)
        mkttoday = mkt_today()
        self._edate = edate if edate < mkttoday else mkttoday
        
        # sdate
        model = config.PortDataDict[self._pname]
        hlength = 0 
        for mo in model.selectors.values():
            if 'hlength' in mo['param'].keys():
                hlength = max(hlength, mo['param']['hlength'])
        for mo in model.optimizer.values():
            if 'hlength' in mo['param'].keys():
                hlength = max(hlength, mo['param']['hlength'])       
        sdate = self._edate - pd.DateOffset(days=np.ceil(hlength * 365.25) + 10)
        self._sdate = config._bday.rollback(sdate).normalize().tz_localize(None)
        
        # provider, force
        self._provider = self._ent_provider.get()
        self._force = self._ent_force.get()
        
        if self._old_param is not None:
            if [self._edate, self._provider, self._force] == self._old_param:
                return False
        if (self._dfw is not None) and self._dfw.winfo_exists():
            self._dfw.destroy()
        self._old_param = [self._edate, self._provider, self._force]
        return True
            

    def _collectMktData(self):
        gmd = GetMktData(self._provider, self._force)
        gmd.getMkTDataSymb(self._symbols, self._sdate, self._edate)
        
        if len(gmd.errorsymb) == 0: return True
        
        msg = (f"The following symbols, {gmd.errorsymb},\n"
               f"cannot be retrieved from the provider {self._provider}\n"
               f"Abort the computation.")
        tk.messagebox.showwarning("Warning", message=msg, parent=self._window)
        return False
    
    
    def _computeWeights(self):
        portdata = config.PortDataDict[self._pname]
        mktdata = {symb: config.MktDataDict[symb].get_mktdata(self._edate).copy() for symb in portdata.symbols}

        optname = list(portdata.optimizer.keys())[0]
        if configModels.get_comptype(optname) == 'standalone':
            fmname = configModels.get_model_family(optname)
            mname = configModels.portfolio_model_family[fmname][optname]['azapy'][0]
            eff_param = deepcopy(portdata.optimizer[optname]['param'])
            eff_param['sdate'] = self._sdate
            eff_param['edate'] = self._edate
            exec(f"self._pipe = {mname}(**eff_param)")
        else:
            model = []
            sel_list = [None] * len(portdata.selectors.keys())
            for vv in portdata.selectors.values():
                sel_list[vv['index']] = vv
            for vv in sel_list:
                mname = configModels.selector_models[vv['name']]['azapy']
                oo = getattr(az, mname)
                moo = oo(**vv['param'])
                model.append(moo)
                
            for vv in portdata.optimizer.values():
                fmname = configModels.get_model_family(vv['name'])
                mname = configModels.portfolio_model_family[fmname][vv['name']]['azapy']
                if mname == 'EWPEngine':
                    model.append('EWP')
                else:
                    oo = getattr(az, mname)
                    moo = oo(**vv['param'])
                    model.append(moo)
            
            self._pipe = az.ModelPipeline(model)

        self._weights = self._pipe.getWeights(mktdata, verbose=False)
        if self._pipe.status == 0: return True
    
        msg = 'Numerical errors in weights computation. Abort!'
        tk.messagebox.showwarning("Warning", message=msg, parent=self._window)
        return False


    def _btn_refresh_func(self):
        self._frm_symb.sort()
    
    
    def _btn_weights_func(self):
        if self._mktdata_info():
            if not self._collectMktData():
                return
            if not self._computeWeights():
                return

        df = (pd.DataFrame(self._weights) * 100).round(2)
        df.columns = ['weight']
        df.index.name = 'symbol'
        df.sort_values('weight', ascending=False, inplace=True)
        if '_CASH_' in df.index:
            ix = list(df.index)
            ix.remove('_CASH_')
            df = df.reindex(['_CASH_'] + ix)
        title = self._pname + ' weights as of ' + self._edate.strftime('%Y%m%d')
        geometry = '100x200'
        fname = self._pname + '_ww_' + self._edate.strftime('%Y%m%d')
        
        if (self._dfw is not None) and self._dfw.winfo_exists():
            self._dfw.destroy()
        self._dfw = DF_Window(master=self._window, 
                        df=df, 
                        title=title, 
                        geometry=geometry, 
                        fname=fname)
        self._rep_show.append(self._dfw)
        
        
    def _ww_destroy(self):
        for ww in self._rep_show:
            if ww.winfo_exists(): ww.destroy()


    def  _btn_cancel(self):
        self._ww_destroy()
        config.PortDataDict[self._pname].setActive(False)
        config.appPortfolioFrame.refresh()
        self._window.destroy()
        
        
    def _capital_info(self):
        self._cash = self._ent_cash.get()
        self._nshares = self._frm_symb.get_data()
        self._nsh_round = self._ent_nsh_round.get()
        
    
    def _btn_traiding_sheet_func(self):
        if self._mktdata_info():
            if not self._collectMktData():
                return
            if not self._computeWeights():
                return
            
        self._capital_info()
        tsheet = self._pipe.getPositions(nshares=self._nshares, cash=self._cash, 
                                         nsh_round=self._nsh_round, verbose=False)
        cap = (tsheet['old_nsh'] * tsheet['prices']).sum()
        if cap <= 0:
            msg = "Total calipta, i.e. cash + cash values of shares, must be >0."
            tk.messagebox.showwarning("Woarning", message=msg, parent=self._window)
            return
        tsheet['Allocation'] = (tsheet['new_nsh'] * tsheet['prices']).round(2)
        tsheet.rename(columns={'old_nsh': 'Initial', 'new_nsh': 'Final', 
                               'diff_nsh': 'Delta', 'weights': 'Weights',
                               'prices': 'Prices'}, inplace=True)
        tsheet.index.name = 'Symbols'
        title = 'Trading Sheet'
        geometry = '400x200'
        fname = self._pname + '_TS_' + self._edate.strftime('%Y%m%d')
        
        
        if (self._dfts is not None) and self._dfts.winfo_exists():
            self._dfts.destroy()
        self._dfts = DF_Window(master=self._window, 
                        df=tsheet, 
                        title=title, 
                        geometry=geometry, 
                        fname=fname)
        self._rep_show.append(self._dfts)


    def _menu_help_func(self):
        webbrowser.open_new_tab(configHelps._Rebalance_panel_help)
        