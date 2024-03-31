import tkinter as tk
from tkinter import ttk
import re
import pandas as pd

import azapyGUI.config as config
from azapyGUI.TimeSeriesViewWindow import TimeSeriesViewWindow, WIDTH_CBX
from azapyGUI.DF_Window import DF_Window


class PortAnalyseWindow(TimeSeriesViewWindow):
    def __init__(self, master, ports):
        self._ports = ports
        
        self._rep_show = {}
        data = {pname: self._ports[pname].get_port() for pname in self._ports.keys()}
        ll = 0
        for pname, vv in data.items():
            if vv.shape[0] > ll:
                ll = vv.shape[0]
                ref_name = pname
        col_name = data[ref_name].columns[0]
        name = 'Performance'
        
        super().__init__(master=master, name=name, data=data, 
                         ref_name=ref_name, col_name=col_name)
        
        frm_specrep = tk.LabelFrame(master=self.frm_btn, text='Specific')
        frm_specrep.pack(side=tk.TOP, fill=tk.X)
        
        self._cbx_sprot = ttk.Combobox(master=frm_specrep, width=WIDTH_CBX, state='readonly')
        self._cbx_sprot.pack(pady=5, padx=5, side=tk.TOP,)
        self._cbx_sprot['values'] = tuple(data.keys())
        self._cbx_sprot.current(0)
        
        self._specific_rep = {'Summary': self._spec_rep_summary,
                              'Weights': self._spec_rep_weights,
                              'Nr. Shares': self._spec_rep_nshares,
                              'Annual': self._spec_rep_annula,
                              'Quarterly': self._spec_rep_quarterly,
                              'Monthly': self._spec_rep_monthly,
                              'Reinv. Ret.': self._spec_rep_reinvret,
                              'Drawdowns': self._spec_rep_drawdown,
                              'Reinv. Perf.': self._spec_rep_reinvperf,
                              'Account': self._spec_rep_account,
                              }
        self._cbx_srep = ttk.Combobox(master=frm_specrep, width=WIDTH_CBX, state='readonly')
        self._cbx_srep.pack(pady=5, padx=5, side=tk.TOP,)
        self._cbx_srep['values'] = tuple(self._specific_rep.keys())
        self._cbx_srep.set('Summary')
        self._cbx_srep.bind("<<ComboboxSelected>>",  self._cbx_srep_func)
        
    
    def _spec_rep_summary(self, pname):
        pp = self._ports[pname]
        rep = pp.port_perf()
        cols = ['RR', 'DD', 'RoMaD']
        rep[cols] = (rep[cols] * 100).round(2)
        
        return rep, f'{pname} Summary', '400x200'
    
    
    def _spec_rep_weights(self, pname):
        pp = self._ports[pname]
        rep = pp.get_weights().set_index(['Droll', 'Dfix'])
        rep = (rep * 100).round(2)

        return rep, f'{pname} Weights', '400x400'
    
    
    def _spec_rep_nshares(self, pname):
        pp = self._ports[pname]
        rep = pp.get_nshares()
        
        return rep, f'{pname} Number of shares', '400x300'


    def _spec_rep_annula(self, pname):
        pp = self._ports[pname]
        rep = pp.port_annual_returns(withcomp=True)
        rep = (rep * 100).round(2)
        rep.rename(columns={'close': pname}, inplace=True)
        
        return rep, f'{pname} Annual Returns (portfolio and components)', '400x300'


    def _spec_rep_quarterly(self, pname):
        pp = self._ports[pname]
        rep = pp.port_quarterly_returns(withcomp=True)
        rep = (rep * 100).round(2)
        rep.rename(columns={'close': pname}, inplace=True)
        rep.columns.name = 'Symbols'
        
        rep.index = pd.MultiIndex.from_arrays(
                                [rep.index.year.to_list(),
                                 ['Q' + str(k) for k in rep.index.quarter]],
                                 names= ['year', 'quarter'])
 
        rep = rep.stack().unstack('quarter')
        
        return rep, f'{pname} Quarterly Returns (portfolio and components)', '300x400'
    
    
    def _spec_rep_monthly(self, pname):
        pp = self._ports[pname]
        rep = pp.port_monthly_returns(withcomp=True)
        rep = (rep * 100).round(2)
        rep.rename(columns={'close': pname}, inplace=True)
        rep.columns.name = 'Symbols'
        
        rep.index = pd.MultiIndex.from_arrays(
                                [rep.index.year.to_list(),
                                 rep.index.month_name().to_list()],
                                 names= ['year', 'month'])
 
        rep = rep.stack().unstack('month')
        rep.columns = pd.Series(rep.columns).apply(lambda x: x[:3])
        rep.columns = pd.Categorical(rep.columns, categories=config._months_name, ordered=True)
        rep.sort_index(axis=1, inplace=True)
        
        return rep, f'{pname} Monthly Returns (portfolio and components)', '500x400'
  
    
    def _spec_rep_reinvret(self, pname):
        pp = self._ports[pname]
        rep = pp.port_period_returns().set_index(['Droll', 'Dfix'])
        rep = (rep * 100).round(2)
        
        return rep, f'{pname} Reinvestment Returns', '400x400'
 
    
    def _spec_rep_drawdown(self, pname):
        pp = self._ports[pname]
        rep = pp.port_drawdown(withcomp=True)
        rep['DD'] = (rep['DD'] * 100).round(2)
        
        return rep, f'{pname} Drawdown (portfolio and component)', '400x400'
 
    
    def _spec_rep_reinvperf(self, pname):
        pp = self._ports[pname]
        rep = pp.port_period_perf().set_index('Droll')
        rep.iloc[:, :4] = (rep.iloc[:, :4] * 100).round(2)
        
        return rep, f'{pname} Performance per reinvestment', '520x400'
 
    
    def _spec_rep_account(self, pname):
        pp = self._ports[pname]
        rep = pp.get_account()
        
        rep.iloc[:,-3:] = rep.iloc[:, -3:].round(2)
        
        return rep, f'{pname} Account Info.', '500x400'
    
    
    def _cbx_srep_func(self, event):
        pname = self._cbx_sprot.get()
        srep = self._cbx_srep.get()
        
        if pname not in self._rep_show.keys():
            self._rep_show[pname] = {}
        if ((srep in self._rep_show[pname].keys()) and
            self._rep_show[pname][srep].winfo_exists()):
            self._rep_show[pname][srep].lift()
            return
        
        df, title, geometry = self._specific_rep[srep](pname)
        fname = pname + '_' + re.sub('[. ]', '', srep)
        
        dfw = DF_Window(master=self._window, df=df, title=title, geometry=geometry, fname=fname)
        self._rep_show[pname][srep] = dfw
        
        
    def _btn_quit_func(self):
        for pp in self._rep_show.values(): 
            for vv in pp.values():
                if vv.winfo_exists(): vv.destroy()
        super()._btn_quit_func()
