import tkinter as tk 
from tkinter import ttk
import webbrowser

import azapyGUI.configSettings as configSettings
import azapyGUI.configHelps as configHelps
from azapyGUI.AppSettingsPage import AppSettingsPage
from azapyGUI.AppSettingsPageMisc import AppSettingsPageMisc

class AppSettingsWindow:
    def __init__(self, master):
        self._master = master
        
        self._window = tk.Toplevel()
        title = f"User Default Settings v.{configSettings.Version}"
        self._window.title(title)
        self._window.focus_set()
        self._window.grab_set()
        self._window.protocol("WM_DELETE_WINDOW", self._on_exit)

        menubar = tk.Menu(self._window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Help', command=self._menu_help_func)
        menubar.add_cascade(label='Help', menu=filemenu)
        self._window.config(menu=menubar)
        
        ntb = ttk.Notebook(master=self._window)
        ntb.pack(expand=True, fill=tk.BOTH)
        
        category = "Directors"
        title = "Default Directories"
        pg_dirctor = AppSettingsPage(master=self._window, category=category, title=title)
        ntb.add(pg_dirctor, text="Directories")
        
        category = "MkTData"
        title = "Market Data"
        pg_mktdata = AppSettingsPage(master=self._window, category=category, title=title)
        ntb.add(pg_mktdata, text="Market Data")
        
        pg_misc = AppSettingsPageMisc(master=self._window)
        ntb.add(pg_misc, text="Miscellaneous")

        
    def _on_exit(self):
        self._window.grab_release()
        if self._master.winfo_exists():
            self._master.focus_set()
        self._window.destroy()

    
    def _menu_help_func(self):
        webbrowser.open_new_tab(configHelps._Settings_panel_help)
