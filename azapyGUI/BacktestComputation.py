import tkinter as tk 
import time
import azapy as az 

import azapyGUI.config as config
import azapyGUI.configModels as configModels
from azapyGUI.GetMktData import GetMktData


class BacktestComputation:
    def __init__(self, master, pnames, sdate, edate, noffset, fixoffset, 
                 capital, nsh_round, provider, force):
        self._master = master
        self._pnames = pnames
        self._sdate = sdate
        self._edate = edate
        self._noffset = noffset
        self._fixoffset = fixoffset
        self._capital = capital
        self._nsh_round = nsh_round
        self._provider = provider
        self._force = force
        
        self.backtest = {}
        self.backtest_error = []
        
    def collectMktData(self):
        symbols = set()
        for pname in self._pnames:
            port = config.PortDataDict[pname]
            symbols.update(port.symbols)

        gmd = GetMktData(self._provider, self._force)
        gmd.getMkTDataSymb(list(symbols), self._sdate, self._edate)
        self.symbols = gmd.symbols
        errorsymb = set(gmd.errorsymb)
        
        if len(errorsymb) == 0: return True
        porterror = []
        for pname in self._pnames:
            port = config.PortDataDict[pname]
            res = errorsymb.intersection(port.symbols)
            if len(res) > 0:
                porterror.append(pname)
                config.PortDataDict[pname].status = 'Unset'
        port = set(self._pnames).intersection(porterror)
        msg = (f"The following symbols, {errorsymb},\n"
               f"cannot be retrieved from the provider {self._provider}\n"
               f"Abort the backtesting for portfolios {porterror}.")
        if len(port) == 0:
            msg += "Abort backtesting!"
            tk.messagebox.showwarning("Warning", message=msg, parent=self._master)
            return False
        
        msg += ("Do you want to continue with the \n"
                f"backtesting for {port}?")
        ask = tk.messagebox.askyesno("Warning", message=msg)
        if ask == 'yes':
            self._pnames = list[port]
            return True
        
        return False
    
    
    def compute(self, time_port):
        for pname in self._pnames:
            
            tic = time.perf_counter()
            res = self._computePort(pname)
            toc = time.perf_counter()
            
            msg = str(round(toc - tic, 4)) + 's' if res else 'error'
            time_port[pname].set(msg)
            self._master.update()
            
            if not res:
                self.backtest_error.append(pname)
            else:
                self.backtest[pname] = self._btest
        
        return len(self.backtest_error) == 0
    
    
    def _computePort(self, pname):
        optname = list(config.PortDataDict[pname].optimizer.keys())[0]
        if configModels.get_comptype(optname) == 'pipe':
            return self._computePort_pipe(pname)
        else:
            return self._computePort_standalone(pname)
        
        
    def _computePort_standalone(self, pname):
        portdata = config.PortDataDict[pname]
        mktdata = {symb: config.MktDataDict[symb].mktdata.copy() for symb in portdata.symbols}
        
        optname = list(config.PortDataDict[pname].optimizer.keys())[0]
        fmname = configModels.get_model_family(optname)
        mname = configModels.portfolio_model_family[fmname][optname]['azapy'][1]
        param = portdata.optimizer[optname]['param']
        freq = param['freq']
        hlength = 0
        pp = getattr(az, mname)(mktdata=mktdata, 
                                sdate=self._sdate,
                                edate=self._edate,
                                pname=pname,
                                pcolname='close',
                                capital=self._capital,
                                freq=freq, 
                                noffset=self._noffset,
                                fixoffset=self._fixoffset, 
                                histoffset=hlength,
                                calendar=config.calendar,
                                nsh_round=self._nsh_round,
                                )
        pp.set_model(**param)
        self._btest = pp
        return (pp.status == 0)
    
    
    def _computePort_pipe(self, pname):
        portdata = config.PortDataDict[pname]
        mktdata = {symb: config.MktDataDict[symb].mktdata.copy() for symb in portdata.symbols}
        model = []
        hlength = 0
        
        sel_list = [None] * len(portdata.selectors.keys())
        for name, vv in portdata.selectors.items():
            sel_list[vv['index']] = vv
        for vv in sel_list:           
            mname = configModels.selector_models[vv['name']]['azapy']
            oo = getattr(az, mname)
            moo = oo(**vv['param'])
            model.append(moo)
            if 'hlength' in vv['param'].keys():
                hlength = max(hlength, vv['param']['hlength'])
            
        for mopt, vv in portdata.optimizer.items():
            fmname = configModels.get_model_family(vv['name'])
            mname = configModels.portfolio_model_family[fmname][vv['name']]['azapy']
            if mname == 'EWPEngine':
                model.append('EWP')
            else:
                oo = getattr(az, mname)
                moo = oo(**vv['param'])
                model.append(moo)
                hlength = max(hlength, vv['param']['hlength'])
            freq = vv['param']['freq']
   
        pipe = az.ModelPipeline(model)
        
        pp = az.Port_Generator(mktdata=mktdata, 
                               sdate=self._sdate,
                               edate=self._edate,
                               pname=pname,
                               pcolname='close',
                               capital=self._capital,
                               freq=freq, 
                               noffset=self._noffset,
                               fixoffset=self._fixoffset, 
                               histoffset=hlength,
                               calendar=config.calendar,
                               nsh_round=self._nsh_round,
                               )
        pp.set_model(pipe)
        self._btest = pp
        return (pp.status == 0)
