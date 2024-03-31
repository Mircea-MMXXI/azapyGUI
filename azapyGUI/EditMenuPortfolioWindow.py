import azapyGUI.config as config
from azapyGUI.SelectOneWindow import SelectOneWindow

class EditMenuPortfolioWindow(SelectOneWindow):
    def __init__(self, master=None):
        self.selection = None
        values =[kk for kk, vv in config.PortDataDict.items() if vv.status == 'Set']
        if len(values) == 0: return
        
        title = "Select Portfolio"
        text = "Choose portfolio for editing"
        tip_text = "Only portfolios with status=Set can be edited."
        btn_text = "Edit"
        super().__init__(master=master, title=title, text=text, values=values, 
                         tip_text=tip_text, btn_text=btn_text)

