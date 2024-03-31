import tkinter as tk 
import pandas as pd
import base64
import azapy as az 

import azapyGUI.config as config
import azapyGUI.configSettings as configSettings
from azapyGUI.serviceMasterUserConfig import _readMasterUserConfig
from azapyGUI.ViewTip import ViewTip
from azapyGUI.PortfolioFrame import PortfolioFrame
from azapyGUI.MktDataFrame import MktDataFrame
from azapyGUI.MenuApp import MenuApp

class app:
    def __init__(self):
        self._root = tk.Tk()
        self._on_start()
        self._root.iconphoto(True, config.photo)
        self._root.title("azapy")
        self._root.rowconfigure(0, minsize=300, weight=1)
        self._root.columnconfigure(0, minsize=100, weight=1)
        self._root.protocol("WM_DELETE_WINDOW", self._on_exit)
        
        MenuApp(self._root)
        config.appPortfolioFrame = PortfolioFrame(self._root, text="Active Projects", font=("Forte", 10))
        config.appPortfolioFrame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        config.appMktDataFrame = MktDataFrame(self._root, text="Active Market Data", font=("Forte", 10))
        config.appMktDataFrame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
    
    
    def run(self):
        self._root.mainloop()
        
        
    def _on_start(self):
        configSettings.MasterApplicationSettings = _readMasterUserConfig()
        config.MktDataDict = {}
        config.PortDataDict = {}
        config.count_SymbTableEntry = -1
        config.calendar = az.NYSEgen()
        config._bday = pd.offsets.CustomBusinessDay(calendar=config.calendar)
        img = base64.b64decode(config.iconimgdata)
        config.photo = tk.PhotoImage(data=img, master=self._root)
        config.tiptil = ViewTip(self._root)
        config.tiptil.turned(on=configSettings.MasterApplicationSettings["ShowTips"])
        
        
    def _on_exit(self):
        port_path = configSettings.MasterApplicationSettings["UserPortfolioDirectory"]
        for kk in config.PortDataDict.keys():
            if not config.PortDataDict[kk].saved:
                msg = "There are unsaved portfolios.\nDo you want to save them?"
                res = tk.messagebox.askquestion("Quit", message=msg, parent=self._root)
                if res == 'no': 
                    self._root.destroy()
                    return
                break
        
        for kk, port in config.PortDataDict.items():
            if port.saved: continue
            filepath = tk.filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Json Files", "*.json")],
                initialdir=port_path,
                initialfile=port.name,
                parent=self._root,
            )
            if filepath: 
                port.saved = True
                config.PortDataDict[port.name].writeFile(filepath)
        
        self._destroy_all_windows()
        self._root.destroy()
        
        
    def _destroy_all_windows(self):
        for widget in self._root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        

def start():
    """Starts azapyGUI application"""
    app().run()


#==============================================================================
# if __name__ == "__main__":
#     start()
