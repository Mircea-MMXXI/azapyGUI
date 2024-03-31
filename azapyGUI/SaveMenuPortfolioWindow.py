import tkinter as tk 
 
import azapyGUI.config as config
import azapyGUI.configSettings as configSettings
from azapyGUI.SelectOneWindow import SelectOneWindow


class SaveMenuPortfolioWindow(SelectOneWindow):
    def __init__(self, master=None):
        values = [kk for kk, vv in config.PortDataDict.items() if not vv.saved]
        if len(values) == 0: return
        
        title = 'Save Portfolio'
        text = 'Choose portfolio to save'
        tip_text = 'Only unsaved portfolios are listed.'
        btn_text = 'Save'
        super().__init__(master=master, title=title, text=text, values=values, 
                         tip_text=tip_text, btn_text=btn_text)

    
    def _btn_action(self):
        port = self._ent.get()
        port_path = configSettings.MasterApplicationSettings["UserPortfolioDirectory"]
        filepath = tk.filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Json Files", "*.json")],
            initialdir=port_path,
            initialfile=port,
            parent=self._window
        )
        if not filepath: return
        
        config.PortDataDict[port].saved = True
        config.PortDataDict[port].writeFile(filepath)
        config.appPortfolioFrame.refresh()
        self._btn_cancel()
