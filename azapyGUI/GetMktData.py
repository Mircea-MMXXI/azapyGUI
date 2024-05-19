import azapy as az 
from copy import deepcopy

import azapyGUI.config as config
import azapyGUI.configSettings as configSettings
from azapyGUI.MktDataNode import MktDataNode


class GetMktData():
    def __init__(self, source, force=False, validate=False):
        self._validate = validate
        
        api_key = None
        param = {}
        for kk, vv in configSettings.MasterApplicationSettings["Provider"][source].items():
            if kk == "key":
                api_key = vv["key"]
            else:
                param[kk] = vv
                
        file_dir = configSettings.MasterApplicationSettings["UserMktDataDirectory"]
        fsave, fforce = (False, True) if file_dir is None else (True, force)
        
        self._symb_req_default = {"symbol": None,
                                  "sdate": None,
                                  "edate": None,
                                  "output_format": 'dict',
                                  "source": source,
                                  "force": fforce,
                                  "save": fsave,
                                  "file_dir": file_dir,
                                  "file_format": 'csv',
                                  "api_key": api_key,
                                  "param": param,
                                  }
        self._mktr = az.MkTreader(verbose=False)
        
        
    def getMkTDataSymb(self, symbols, sdate, edate):
        # sdate and edate are assumed to be validated
        self._symb_req = deepcopy(self._symb_req_default)

        self._symb_req["sdate"] = sdate
        self._symb_req["edate"] = edate
        
        symb = [sy for sy in symbols if not self._checkCollection(sy, sdate, edate)]
        if len(symb) == 0:
            # all symb in the system - OK nothing else to do
            self.symbols = symbols
            self.errorsymb = []
            return
        
        # retrieve symb (not in the system)
        self._symb_req["symbol"] = symb
        mktdata = self._mktr.get(calendar=config.calendar, **self._symb_req)
        if len(mktdata.keys()) == 0:
            # no extraction was possible (all symb are error symbols)
            self.symbols = list(set(symbols) - set(symb))
            self.errorsymb = symb
            return
        
        status = self._mktr.get_request_status()
        error_log = self._mktr.get_error_log()
        self.symbols = list(mktdata.keys())
        self.errorsymb = list(set(symb) - set(self.symbols))
        
        # put in the collection newly extracted symbols
        for sy in self.symbols:
            mktData = MktDataNode()
            mktData.name = sy
            mktData.mktdata = mktdata[sy].copy()
            mktData.stats = status[sy].copy()
            mktData.error_log = error_log[sy].copy() if sy in error_log.keys() else {}
            config.MktDataDict[sy] = mktData
        config.appMktDataFrame.refresh()
        
                
    def _checkCollection(self, symb, sdate, edate):
        if symb not in config.MktDataDict.keys(): return False
        
        if self._validate: return True
        
        if ((self._symb_req["sdate"] >= config.MktDataDict[symb].sdate()) and
            (self._symb_req["edate"] <= config.MktDataDict[symb].edate())): return True

        return False
