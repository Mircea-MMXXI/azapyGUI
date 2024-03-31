import tkinter as tk 
from tkinter import filedialog
import glob
import os
import webbrowser
import azapy as az

import azapyGUI.config as config
import azapyGUI.configSettings as configSettings
import azapyGUI.configHelps as configHelps
from azapyGUI.PortDataNode import PortDataNode
from azapyGUI.EditPortfolioWindow import EditPortfolioWindow
from azapyGUI.SaveMenuPortfolioWindow import SaveMenuPortfolioWindow
from azapyGUI.CloneMenuPortfolioWindow import CloneMenuPortfolioWindow
from azapyGUI.RemoveMenuPortfolioWindow import RemoveMenuPortfolioWindow
from azapyGUI.EditMenuPortfolioWindow import EditMenuPortfolioWindow
from azapyGUI.AppSettingsWindow import AppSettingsWindow
from azapyGUI.SymbExtractWindow import SymbExtractWindow
from azapyGUI.BacktestMenuPortfolioWindow import BacktestMenuPortfolioWindow
from azapyGUI.BacktestEntryWindow import BacktestEntryWindow
from azapyGUI.RebalanceMenuPortfolioWindow import RebalanceMenuPortfolioWindow
from azapyGUI.WeightsWindow import WeightsWindow


class MenuApp:
    def __init__(self, window):
        self._window = window
        
        menubar = tk.Menu(self._window)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self._new_port)
        filemenu.add_command(label="Open", command=self._load_port)
        filemenu.add_command(label="Clone", command=self._clone_port)
        filemenu.add_command(label="Edit", command=self._edit_port)
        filemenu.add_separator()
        filemenu.add_command(label="Backtest", command=self._backtest_port)
        filemenu.add_command(label="Rebalance", command=self._rebalance_port)
        filemenu.add_separator()
        filemenu.add_command(label="Save", command=self._save_port)
        filemenu.add_command(label="Save all",  command=self._save_all_port)
        filemenu.add_command(label="Remove", command=self._remove_port)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self._quit)
        
        menubar.add_cascade(label="Portfolio", menu=filemenu)
        
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Load", command=self._load_symbols)
        editmenu.add_separator()
        editmenu.add_command(label="Clear", command=self._clear_symbols)

        menubar.add_cascade(label="Mkt Data", menu=editmenu)
        
        setingsmenu = tk.Menu(menubar, tearoff=0)
        setingsmenu.add_command(label="Application Settings", command=self._application_settings)
        
        menubar.add_cascade(label="Settings", menu=setingsmenu)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self._help_index)
        helpmenu.add_command(label="Quick Start", command=self._help_quick_start)
        helpmenu.add_separator()
        helpmenu.add_command(label="About...", command=self._help_about)
        
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self._window.config(menu=menubar)
        

    def _new_port(self):
        npw = EditPortfolioWindow(master=self._window)
        portfolio = npw.portfolio
        if portfolio is None: return
        
        
    def _save_port(self):
        SaveMenuPortfolioWindow(master=self._window)
        
        
    def _save_all_port(self):
        port_path = configSettings.MasterApplicationSettings["UserPortfolioDirectory"]
        for kk, port in config.PortDataDict.items():
            if port.saved: continue
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Json Files", "*.json")],
                initialdir=port_path,
                initialfile=port.name,
            )
            if not filepath: return
            
            port.saved = True
            config.PortDataDict[port.name].writeFile(filepath)
            
        config.appPortfolioFrame.refresh()

        
    def _load_port(self):
        port_path = configSettings.MasterApplicationSettings["UserPortfolioDirectory"]
        filepaths = tk.filedialog.askopenfilename(
            filetypes=[("Json Files", "*.json")],
            initialdir=port_path,
            title='Portfolio loading',
            multiple=True,
            parent=self._window
        )
        for filepath in filepaths:
            sport = PortDataNode().loadFile(filepath)
            if sport.name in config.PortDataDict.keys():
                tk.messagebox.showwarning(
                    "Warning", 
                    f"Name {sport.name} already in use!\nAbort opening.")
                continue
            sport.status = 'Set'
            config.PortDataDict[sport.name] = sport
            config.appPortfolioFrame.refresh()
        
        
    def _clone_port(self):
        CloneMenuPortfolioWindow(self._window)
        
        
    def _remove_port(self):
        RemoveMenuPortfolioWindow(self._window)
        
        
    def _edit_port(self):
        empw = EditMenuPortfolioWindow(master=self._window)
        if empw.selection is None: return
        EditPortfolioWindow(self._window, portfolio=config.PortDataDict[empw.selection])


    def _quit(self):
        for kk in config.PortDataDict.keys():
            if not config.PortDataDict[kk].saved:
                res = tk.messagebox.askquestion(
                    "Save portfolio", 
                    "There are unsaved portfolios.\nDo you want to save them?",
                    parent=self._window)
                if res == 'yes': self._save_all_port()
                break
                    
        self._window.quit()
        self._window.destroy()
        
    def _application_settings(self):
        AppSettingsWindow(master=self._window)
        
    
    def _load_symbols(self):
        SymbExtractWindow(master=self._window, title="Download Market Data", entry=True)


    def _clear_symbols(self):
        path_mkt = configSettings.MasterApplicationSettings["UserMktDataDirectory"]
        if  path_mkt is None: return
        title = "Clear Market Data directory?"
        msg = f"Delete all market data files from\n{path_mkt}"
        res = tk.messagebox.askyesno(title, message=msg, parent=self._window)
        if not res: return
        for ff in glob.iglob(path_mkt + '/*'):
            os.remove(ff)
            
    
    def _backtest_port(self):
        bmpw = BacktestMenuPortfolioWindow(master=self._window)
        if bmpw.selection is None:
            return
        config.PortDataDict[bmpw.selection].setActive(True)
        config.appPortfolioFrame.refresh()
        BacktestEntryWindow(master=self._window, pnames=[bmpw.selection])
    
    
    def _rebalance_port(self):
        rmpw = RebalanceMenuPortfolioWindow(master=self._window)
        if rmpw.selection is None:
            return
        config.PortDataDict[rmpw.selection].setActive(True)
        config.appPortfolioFrame.refresh()
        WeightsWindow(master=self._window, pname=rmpw.selection)
        
    
    def _help_about(self):
        msg = configHelps._About_help.format(vgui=config.__version__, v=az.__version__)
        tk.messagebox.showinfo('About', msg) 


    def _help_index(self):
        webbrowser.open_new_tab(configHelps._index_help)


    def _help_quick_start(self):
        webbrowser.open_new_tab(configHelps._Quick_Start_help)
