import azapy as az

class MktDataNode:
    def __init__(self):
        self.name = None
        self.mktdata = None
        self.stats = None
        self.status = False
        self._summary = None
        
        
    def sdate(self):
        if self._summary is None: self._summary = az.summary_MkTdata(self.mktdata)
        return self._summary.begin[0]
    
    
    def edate(self):
        if self._summary is None: self._summary = az.summary_MkTdata(self.mktdata)
        return self._summary.end[0]
    
    
    def nrow(self):
        if self._summary is None: self._summary = az.summary_MkTdata(self.mktdata)
        return self._summary.length[0]
    
    
    def iserror(self):
        if self._summary is None: self._summary = az.summary_MkTdata(self.mktdata)
        return (self._summary.na_total[0] + self._summary.cont[0]) > 0
    
    
    def get_mktdata(self, edate=None):
        return self.mktdata if edate is None else self.mktdata[self.mktdata.index <= edate]
    