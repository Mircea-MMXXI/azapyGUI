import tkinter as tk

import azapyGUI.config as config
from azapyGUI.SelectOneWindow import SelectOneWindow


class RemoveMenuPortfolioWindow(SelectOneWindow):
    def __init__(self, master=None):
        values = [kk for kk, vv in config.PortDataDict.items() if vv.status == 'Set']
        title = "Remove Portfolio"
        text = "Choose portfolio to remove"
        tip_text = "Only portfolios with status=Set can be removed."
        btn_text = "Remove"
        super().__init__(master=master, title=title, text=text, values=values, 
                         tip_text=tip_text, btn_text=btn_text)

    
    def _btn_action(self):
        port_name = self._ent.get()
        if not config.PortDataDict[port_name].saved:
            filepath = tk.filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Json Files", "*.json")],
                initialfile=port_name,
            )
            if filepath: 
                config.PortDataDict[port_name].saved = True
                config.PortDataDict[port_name].writeFile(filepath)
        if config.PortDataDict[port_name].status == 'Set': 
            del config.PortDataDict[port_name]
        self._btn_cancel()
        config.appPortfolioFrame.refresh()
        