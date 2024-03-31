import tkinter as tk 
from tkinter import ttk

import azapyGUI.config as config
import azapyGUI.configSettings as configSettings
from azapyGUI.EntryRenamePortfolioWindow import EntryRenamePortfolioWindow
from azapyGUI.EntryClonePortfolioWindow import EntryClonePortfolioWindow
from azapyGUI.EditPortfolioWindow import EditPortfolioWindow
from azapyGUI.PortDataNode import PortDataNode
from azapyGUI.BacktestEntryWindow import BacktestEntryWindow
from azapyGUI.WeightsWindow import WeightsWindow


class PortfolioFrame(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        self._master = master
        super().__init__(master=self._master, **kwargs)
     
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self._trv = ttk.Treeview(master=self, columns=("#1", "#2"))
        self._trv.grid(row=0, column=0, sticky=tk.NSEW)
        
        self._trv.heading("#0", text="Portfolio", command=self._load_port)
        self._trv.heading("#1", text="Status")
        self._trv.heading("#2", text="Saved")
        
        self._trv.column("#0", minwidth=10, width=120, stretch=True, anchor=tk.W)
        self._trv.column("#1", minwidth=10, width=60, stretch=False, anchor=tk.CENTER)
        self._trv.column("#2", minwidth=10, width=60, stretch=False, anchor=tk.CENTER)
        
        vscrlb = ttk.Scrollbar(master=self, 
                               orient ="vertical", 
                               command = self._trv.yview)
        vscrlb.grid(row=0, column=1, sticky=tk.NS)
        self._trv.configure(yscrollcommand = vscrlb.set)
        self._trv.tag_bind("trv_tag", "<<TreeviewSelect>>", self._item_select)
        
        self.refresh()
        self._set_menu()
        
        
    def _set_menu(self):
        self._mmenu = tk.Menu(self._trv, tearoff = 0) 
        self._mmenu.add_command(label ="Edit", command=self._edit_port) 
        self._mmenu.add_command(label="Backtest", command=self._backtest_port)
        self._mmenu.add_command(label="Rebalance", command=self._rebalance_port)
        self._mmenu.add_command(label ="Clone", command=self._clone_port)  
        self._mmenu.add_command(label ="Rename", command=self._rename_port) 
        self._mmenu.add_command(label ="Save", command=self._save_port)  
        self._mmenu.add_separator() 
        self._mmenu.add_command(label ="Remove", command=self._delete_port) 
        
        
    def refresh(self): 
        for item in self._trv.get_children():
            self._trv.delete(item)
            
        for kk, val in config.PortDataDict.items():
            self._trv.insert(
                "",
                tk.END,
                text=val.name,
                values=(val.status, val.saved),
                tags=("trv_tag",),
            )
        
        
    def _item_select(self, _event: tk.Event):
        iids = self._trv.selection()
        self._port_selected = [self._trv.item(iid,'text') for iid in iids]

        try: 
            self._mmenu.tk_popup(self._trv.winfo_pointerx(), self._trv.winfo_pointery()) 
        finally: 
            self._mmenu.grab_release() 
            
            
    def _save_port(self):
        port_path = configSettings.MasterApplicationSettings["UserPortfolioDirectory"]
        for tport in self._port_selected:
            if config.PortDataDict[tport].saved: continue
            filepath = tk.filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Json Files", "*.json")],
                initialdir=port_path,
                initialfile=tport,
            )
            if filepath: 
                config.PortDataDict[tport].saved = True
                config.PortDataDict[tport].writeFile(filepath)
        self.refresh()
        
        
    def _rename_port(self):
        tport = self._port_selected[0]
        if config.PortDataDict[tport].status != 'Set': return
        EntryRenamePortfolioWindow(master=self._master, pname=tport)
    
        
    def _clone_port(self):
        tport = self._port_selected[0]
        EntryClonePortfolioWindow(master=self._master, pname=tport)

        
    def _delete_port(self):
        for tport in self._port_selected:
            if config.PortDataDict[tport].status != 'Set':
                msg = f"Portfolio {tport} cannot be removed at this time"
                tk.messagebox.showwarning("Warning", message=msg, parent=self._master)
                continue
            if not config.PortDataDict[tport].saved:
                filepath = tk.filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("Json Files", "*.json")],
                    initialfile=tport,
                    parent=self._master
                )
                if filepath: 
                    config.PortDataDict[tport].saved = True
                    config.PortDataDict[tport].writeFile(filepath)
            del config.PortDataDict[tport]
        self.refresh()
        
        
    def _edit_port(self):
        pname = self._port_selected[0]
        if config.PortDataDict[pname].status != 'Set': return
        EditPortfolioWindow(master=self._master, portfolio=config.PortDataDict[pname])


    def _load_port(self):
        port_path = configSettings.MasterApplicationSettings["UserPortfolioDirectory"]
        filepaths = tk.filedialog.askopenfilename(
            filetypes=[("Json Files", "*.json")],
            initialdir=port_path,
            title='Portfolio loading',
            multiple=True,
            parent=self._master,
        )
        for filepath  in list(filepaths):
            sport = PortDataNode().loadFile(filepath)
            if sport.name in config.PortDataDict.keys():
                tk.messagebox.showwarning(
                    "Warning", 
                    f"Name {sport.name} already in use!\nAbort opening.",
                    parent=self._master)
                continue
            sport.status = 'Set'
            config.PortDataDict[sport.name] = sport
            config.appPortfolioFrame.refresh()
        
        
    def _backtest_port(self):
        tport = self._port_selected
        lport = [pp for pp in tport if config.PortDataDict[pp].status != 'Edit']
        port_error = set(tport) - set(lport)

        if len(port_error) > 0:
            msg = (f"The following portfolios {port_error}\n"
                   "are being edited. They cannot be included in the\n" 
                   "computations at this time."
                   )
            if len(lport) == 0:
                msg += "Abort backtesting!"
                tk.messagebox.showwarning("Warning", message=msg, parent=self._master)
                return
            else:
                msg += ("Do you want to continue with the backtesting for\n"
                        f"{lport}"
                        )
                ask = tk.messagebox.askyesno("Warning", message=msg, parent=self._master)
                if ask == 'no':
                    return
        
        for pname in lport:
            config.PortDataDict[pname].setActive(True)
        self.refresh()
        
        BacktestEntryWindow(master=self._master, pnames=lport)
        
        
    def _rebalance_port(self):
        pname = self._port_selected[0]
        if config.PortDataDict[pname].status == 'Edit':
            msg = ("This portfolio is being edited. \n"
                   "It cannot be evaluated at this time."
                   )
            tk.messagebox.showwarning('Warning', message=msg, parent=self._master)
            return
        
        config.PortDataDict[pname].setActive(True)
        self.refresh()
        WeightsWindow(master=self._master, pname=pname)
        