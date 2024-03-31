import azapyGUI.config as config
from azapyGUI.SelectOneWindow import SelectOneWindow

class BacktestMenuPortfolioWindow(SelectOneWindow):
    def __init__(self, master=None):
        values = [kk for kk, vv in config.PortDataDict.items() if vv.status != 'Edit']
        if len(values) == 0:
            self.selection = None
            return
        title = "Backtesting Portfolio"
        text = "Choose portfolio"
        tip_text = "Only portfolios with status=Set or Active can be backtested."
        btn_text = "Backtest"
        super().__init__(master=master, title=title, text=text, values=values, 
                         tip_text=tip_text, btn_text=btn_text)
        
    
    def _btn_action(self):
        self.selection = self._ent.get()
        self._btn_cancel()