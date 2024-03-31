import tkinter as tk 
from copy import deepcopy

import azapyGUI.config as config
import azapyGUI.configMSG as configMSG
from azapyGUI.modelParametersValidation import _validate_portfolio_name
from azapyGUI.EntryNameWindow import EntryNameWindow

class EntryClonePortfolioWindow(EntryNameWindow):
    def __init__(self, master, pname):
        self._pname = pname
        
        title = "Portfolio Clone"
        text = f"Target portfolio: {pname}\nNew name:"
        tip_text = "Unique portfolio name (letters + digits + .-_)"
        super().__init__(master=master, title=title, text=text, tip_text=tip_text)
        
        
    def _btn_save(self):
        nname = self._ent.get()
        status, val = _validate_portfolio_name(nname)
        if status:
            if val in config.PortDataDict.keys():
                tk.messagebox.showwarning("Warning", configMSG._validate_portfolio_name_exist_msg, 
                                          parent=self._window)
                return
            port = deepcopy(config.PortDataDict[self._pname])
            port.name = val
            port.saved = False
            port.status = 'Set'
            config.PortDataDict[val] = port
            config.appPortfolioFrame.refresh()
            self._btn_cancel()
            return
        tk.messagebox.showwarning("Warning", val, parent=self._window)
