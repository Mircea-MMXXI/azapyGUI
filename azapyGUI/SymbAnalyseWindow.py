from copy import deepcopy

import azapyGUI.config as config
from azapyGUI.TimeSeriesViewWindow import TimeSeriesViewWindow


class SymbAnalyseWindow(TimeSeriesViewWindow):
    def __init__(self, master=None, symbols=None):
        mktdata = {}
        ref_name = symbols[0]
        nnrr = config.MktDataDict[ref_name].mktdata.shape[0]
        for symb in symbols:
            mktdata[symb] = deepcopy(config.MktDataDict[symb].mktdata.drop(
                columns=['symbol', 'divd', 'split', 'volume']))
            if mktdata[symb].shape[0] > nnrr:
                nnrr = mktdata[symb].shape[0]
                ref_name = symb
        col_name = 'close'   
        title = "Performance"
        super().__init__(master=master, name=title, data=mktdata, 
                         ref_name=ref_name, col_name=col_name)
