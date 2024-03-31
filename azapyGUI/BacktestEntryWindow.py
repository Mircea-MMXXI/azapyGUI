import tkinter as tk 
from tkinter import ttk
import time
import webbrowser

import azapyGUI.configSettings as configSettings
import azapyGUI.configMSG as configMSG
import azapyGUI.config as config
import azapyGUI.configTips as configTips
import azapyGUI.configHelps as configHelps
import azapyGUI.tkHelper as tkHelper
from azapyGUI.mktDataValidation import sdate_edate_validate
from azapyGUI.BacktestComputation import BacktestComputation
from azapyGUI.PortAnalyseWindow import PortAnalyseWindow
from azapyGUI.modelParametersValidation import _validDateMMDDYYYY, _validInt, _validIntNegative, _list2string
from azapyGUI.Scrollable import Scrollable

class BacktestEntryWindow:
    def __init__(self, master, pnames):
        self._master = master
        self._pnames = pnames
        self._paw = None
        
        self._window = tk.Toplevel()
        self._window.title("Backtesting")
        self._window.focus_set()
        self._window.protocol("WM_DELETE_WINDOW", self._btn_cancel_func)

        menubar = tk.Menu(self._window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Help', command=self._menu_help_func)
        menubar.add_cascade(label='Help', menu=filemenu)
        self._window.config(menu=menubar)
        
        text = 'Backtesting simulation parameters'
        self._frm_btp = tk.LabelFrame(master=self._window, text=text, font=("Forte", 10))
        self._frm_btp.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._frm_btp.columnconfigure(1, weight=1)
        
        row = 0
        self._frm_btp.rowconfigure(row, weight=1)
        text = 'Portfolios: ' + _list2string(self._pnames, 5)
        lbl = tk.Label(master=self._frm_btp, text='Portfolios:', anchor=tk.W)
        lbl.grid(row=row, column=0, padx=5, pady=5, sticky=tk.NW)
        lbl = tk.Label(master=self._frm_btp, text=_list2string(self._pnames, 5), 
                       anchor=tk.W, justify=tk.LEFT)
        lbl.grid(row=row, column=1, columnspan=3, padx=5, pady=5, sticky=tk.NW)
        
 
        row += 1
        self._frm_btp.rowconfigure(row, weight=1)
        lbl = tk.Label(master=self._frm_btp, text='End Date')
        lbl.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        
        self._ent_edate = tk.StringVar(master=self._frm_btp,
                                       value=configSettings.MasterApplicationSettings['edate'])
        ent_edate = tk.Entry(master=self._frm_btp, width=10, textvariable=self._ent_edate)
        ent_edate['validatecommand'] = (ent_edate.register(_validDateMMDDYYYY),'%S','%d','%P')
        ent_edate.grid(row=row, column=1, pady=5, padx=5, sticky=tk.W)
        config.tiptil.bind(ent_edate, configTips._bkt_edate_tip)
        
        
        lbl = tk.Label(master=self._frm_btp, text='Bday offset')
        lbl.grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
        
        self._ent_noffset = tk.StringVar(master=self._frm_btp,
                                         value=configSettings.MasterApplicationSettings['noffset'])
        ent_noffset = tk.Entry(master=self._frm_btp, width=3, textvariable=self._ent_noffset)
        ent_noffset['validatecommand'] = (ent_noffset.register(_validInt),'%S','%d','%P')
        ent_noffset.grid(row=row, column=3, pady=5, padx=5, sticky=tk.W)
        config.tiptil.bind(ent_noffset, configTips._bkt_noffset_tip)
 
        row += 1
        self._frm_btp.rowconfigure(row, weight=1)
        lbl = tk.Label(master=self._frm_btp, text='Start Date')
        lbl.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        
        self._ent_sdate = tk.StringVar(master=self._frm_btp,
                                       value=configSettings.MasterApplicationSettings['sdate'])
        ent_sdate = tk.Entry(master=self._frm_btp, width=10, textvariable=self._ent_sdate)
        ent_sdate['validatecommand'] = (ent_sdate.register(_validDateMMDDYYYY),'%S','%d','%P')
        ent_sdate.grid(row=row, column=1, pady=5, padx=5, sticky=tk.W)
        config.tiptil.bind(ent_sdate, configTips._bkt_sdate_tip)
        
        lbl = tk.Label(master=self._frm_btp, text='Fixing offset')
        lbl.grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
        
        self._ent_fixoffset= tk.StringVar(master=self._frm_btp,
                                          value=configSettings.MasterApplicationSettings['fixoffset'])
        ent_fixoffset = tk.Entry(master=self._frm_btp, width=3, textvariable=self._ent_fixoffset)
        ent_fixoffset['validatecommand'] = (ent_fixoffset.register(_validIntNegative),'%S','%d','%P')
        ent_fixoffset.grid(row=row, column=3, pady=5, padx=5, sticky=tk.W)
        config.tiptil.bind(ent_fixoffset, configTips._bkt_fixoffset_tip)
        
        row += 1 
        self._frm_btp.rowconfigure(row, weight=1)
        lbl = tk.Label(master=self._frm_btp, text='Capital')
        lbl.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        
        self._ent_capital = tk.StringVar(master=self._frm_btp,
                                         value=configSettings.MasterApplicationSettings['capital'])
        ent_capital = tk.Entry(master=self._frm_btp, width=10, textvariable=self._ent_capital)
        ent_capital['validatecommand'] = (ent_capital.register(_validInt),'%S','%d','%P')
        ent_capital.grid(row=row, column=1, pady=5, padx=5, sticky=tk.W)
        config.tiptil.bind(ent_capital, configTips._bkt_capital_tip)
        
        
        lbl = tk.Label(master=self._frm_btp, text='Nr Shares int')
        lbl.grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
        
        self._ent_nsh_round = tk.BooleanVar(master=self._frm_btp,
                                            value=configSettings.MasterApplicationSettings['nsh_round'])
        ckb_ent_nsh_round = ttk.Checkbutton(master=self._frm_btp, variable=self._ent_nsh_round, 
                                            onvalue=True, offvalue=False)
        ckb_ent_nsh_round.grid(row=row, column=3, pady=5, padx=5, sticky=tk.W)
        config.tiptil.bind(ckb_ent_nsh_round, configTips._bkt_nsh_round_tip)
            
        text = "Market Data"
        self._frm_mkt = tk.LabelFrame(master=self._window, text=text, font=("Forte", 10))
        self._frm_mkt.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._frm_mkt.columnconfigure(1, weight=1)
        
        row = 0
        self._frm_mkt.rowconfigure(row, weight=1)
        lbl = tk.Label(master=self._frm_mkt, text='Provider')
        lbl.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        
        pval = list(configSettings.MasterApplicationSettings["Provider"].keys())
        self._ent_provider = tk.StringVar(master=self._frm_mkt)
        ent_provider = ttk.Combobox(master=self._frm_mkt, width=12, textvariable=self._ent_provider)
        ent_provider["values"] = pval
        ent_provider.current(0)
        ent_provider.grid(row=row, column=1, pady=5, padx=5, sticky=tk.EW)
        config.tiptil.bind(ent_provider, configTips._bkt_provider_tip)
        
        lbl = tk.Label(master=self._frm_mkt, text="force", anchor=tk.W)
        lbl.grid(row=row, column=2, padx=5, pady=5, sticky=tk.W)
        
        self._ent_force = tk.BooleanVar(value=configSettings.MasterApplicationSettings['force'])
        chk_force = tk.Checkbutton(master=self._frm_mkt, onvalue=True, offvalue=False, variable=self._ent_force)
        chk_force.grid(row=row, column=3, padx=5, pady=5, sticky=tk.W)
        config.tiptil.bind(chk_force, configTips._bkt_force_tip)
        
        
        frm_btn = tk.Frame(master=self._window)
        frm_btn.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self._btn_cancel = tk.Button(master=frm_btn, text='Cancel', width=12, command=self._btn_cancel_func)
        self._btn_cancel.pack(side=tk.LEFT, padx=5, pady=5,)
        
        self._btn_start = tk.Button(master=frm_btn, text='Start', width=12, command=self._btn_start_func)
        self._btn_start.pack(side=tk.RIGHT, padx=5, pady=5,)
        
        # self._frm_progress = tk.LabelFrame(master=self._window, text="Progress", font=("Forte", 10), height=200, width=300)
        # self._frm_progress.pack(fill=tk.X, expand=False, padx=5, pady=5)
 
        
    def _destroy_all_windows(self):
        for widget in self._window.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
    
    
    def _on_exit(self):
        for pname in self._pnames:
            config.PortDataDict[pname].setActive(False)
        config.appPortfolioFrame.refresh()
        
        if self._paw is not None: self._paw._btn_quit_func()
        self._destroy_all_windows()
        self._window.grab_release()
        if self._master.winfo_exists():
            self._master.focus_set()
            self._master.lift()
        self._window.destroy()
        
        
    def _btn_cancel_func(self):
        self.status = False
        self._on_exit()
        
        
    def _validate_entries(self):
        # get inputs
        s_sdate = self._ent_sdate.get()
        s_edate = self._ent_edate.get()
        s_noffset = self._ent_noffset.get()
        s_fixoffset = self._ent_fixoffset.get()
        s_capital = self._ent_capital.get()
        self._nsh_round = self._ent_nsh_round.get()
        self._provider = self._ent_provider.get()
        self._force = self._ent_force.get()
        
        # validate sdate and edate
        state, self.sdate, self.edate = sdate_edate_validate(s_sdate, s_edate)
        if not state:
            tk.messagebox.showwarning("Warning", message=self.sdate, 
                                      parent=self._window)
            return False
        
        # validate noffset
        try:
            self.noffset = int(s_noffset)
        except:
            tk.messagebox.showwarning("Warning", message=configMSG._validate_noffset_msg, 
                                      parent=self._window)
            return False
        
        # validate fixoffset
        try:
            self.fixoffset = int(s_fixoffset)
        except:
            tk.messagebox.showwarning("Warning", message=configMSG._validate_fixoffset_msg, 
                                      parent=self._window)
            return False
        if self.fixoffset > 0:
            tk.messagebox.showwarning("Warning", message=configMSG._validate_fixoffset_msg, 
                                      parent=self._window)
            return False
        
        # capital
        try: 
            self._capital = float(s_capital)
        except:
            tk.messagebox.showerror("Warning", message=configMSG._validate_capital_msg,
                                    parent=self._window)
            return False
        if self._capital < 10000:
            tk.messagebox.showerror("Warning", message=configMSG._validate_capital_msg,
                                    parent=self._window)
            return False
            
        
        return True
    
    
    def _buid_frm_progress(self):
        self._frm_progress = tk.LabelFrame(master=self._window, text="Progress", font=("Forte", 10))
        self._frm_progress.pack(fill=tk.X, expand=False, padx=5, pady=5, ipadx=5, ipady=5)

        onfrm = self._frm_progress if len(self._pnames) <= 5 else Scrollable(self._frm_progress)

        row = 0
        lbl = tk.Label(master=onfrm, text='Collect Mkt Data')
        lbl.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        
        self._time_mktdata = tk.StringVar(master=onfrm, value='-')
        lbl = tk.Label(master=onfrm, textvariable=self._time_mktdata, width=10)
        lbl.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
        
        self._time_port = {}
        for pname in self._pnames:
            row += 1 
            lbl = tk.Label(master=onfrm, text=f'Portfolio {pname}')
            lbl.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
            
            self._time_port[pname] = tk.StringVar(master=onfrm, value='-')
            lbl = tk.Label(master=onfrm, textvariable=self._time_port[pname], width=10)
            lbl.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)

        onfrm.update()    
        self._window.update()
 
    
    def _btn_start_func(self):   
        if not self._validate_entries(): return
        
        tkHelper.enable_widget(self._frm_btp, enabled=False)
        tkHelper.enable_widget(self._frm_mkt, enabled=False)
        self._btn_start.config(state=tk.DISABLED)
        self._btn_cancel.config(text="Close")
        self._window.update()
        
        self.status = True
        
        self._buid_frm_progress()
        
        btc = BacktestComputation(master=self._window, 
                                  pnames=self._pnames,
                                  sdate=self.sdate,
                                  edate=self.edate,
                                  noffset=self.noffset,
                                  fixoffset=self.fixoffset,
                                  capital=self._capital,
                                  nsh_round=self._nsh_round,
                                  provider=self._provider,
                                  force=self._force,
                                  )

        tic = time.perf_counter()
        btc.collectMktData()
        toc = time.perf_counter()
        self._time_mktdata.set(str(round(toc-tic, 4)) + 's')
        self._window.update()
        config.appMktDataFrame.refresh()

        btc.compute(self._time_port)
        
        ports = btc.backtest
        if len(ports) < 1: return
        
        self._paw = PortAnalyseWindow(master=self._window, ports=ports)


    def _menu_help_func(self):
        webbrowser.open_new_tab(configHelps._Backtest_panel_help)
        