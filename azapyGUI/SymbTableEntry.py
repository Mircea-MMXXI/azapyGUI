import tkinter as tk

import azapyGUI.config as config
from azapyGUI.Scrollable import Scrollable
from azapyGUI.modelParametersValidation import _validate_symbols


class SymbTableEntry:
    def __init__(self, master, nrows=100, ncols=5, name=None, **kwargs):
        self._name = name if name is not None else self._getName()
        self._frm = tk.Frame(master=master)
        self._nrows = nrows
        self._ncols = ncols

        self._stb = Scrollable(self._frm, **kwargs)
        
        self._table = []
        for i in range(self._nrows):
            rw = []
            for j in range(self._ncols):
                self._stb.rowconfigure(i, weight=1)
                self._stb.columnconfigure(j, weight=1)
                ename = "!" + self._name + "_" + str(i) + "_" + str(j)
                tt = tk.Entry(self._stb, width=5, name=ename)
                tt.grid(row=i, column=j, sticky=tk.NSEW)
                rw.append(tt)
            self._table.append(rw)
            
        self._table[0][0].focus_set()
    

    def grid(self, *args, **kwargs):
        self._frm.grid(*args, **kwargs)
        self._stb.update()
        

    def pack(self, *args, **kwargs):
        self._frm.pack(*args, **kwargs)
        self._stb.update()
        

    def get(self, row=None, column=None):
        if (row is not None) and (column is not None):
            return self._table[row][column]
        
        tx = []
        for i in range(self._nrows):
            for j in range(self._ncols):
                tt = self._table[i][j].get()
                if len(tt) < 1: continue
                tx.append(tt)
        status, sout = _validate_symbols(tx)
        return status, sorted(list(set(sout)))
    
    
    def _getName(self):
        config.count_SymbTableEntry += 1
        return 'SymbTableEntry' + str(config.count_SymbTableEntry)
    
    
    def write_order(self, txt):
        self.empty()
        ic = 0
        jc = 0
        for tt in sorted(txt):
            if tt == "": continue
            self._table[ic][jc].insert(0, tt)
            jc += 1
            if jc >= self._ncols:
                jc = 0 
                ic += 1
            if ic >= self._nrows: 
                self._table[0][0].focus_set()
                return
        self._table[ic][jc].focus_set()
        
        
    def empty(self):
        for i in range(self._nrows):
            for j in range(self._ncols):
                self._table[i][j].delete(0, tk.END)
                
                
    def table_focus_get(self):
        tfx = str(self._table[0][0].focus_get())
        fx = tfx.split("!")[-1].split("_")
        if fx[0] == self._name:
            return tuple(int(x) for x in fx[1:])
        
        return (None, None)
    
    
    def key_press(self, event):
        i, j = self.table_focus_get()

        if i is None: return
        elif event.keysym == 'Up':
            if i == 0: return
            self._table[i-1][j].focus_set()
        elif event.keysym == 'Down':
            if i == self._nrows - 1: return
            self._table[i+1][j].focus_set()
        elif event.keysym == 'Return':
            j += 1
            if j == self._ncols:
                j = 0
                i += 1
                if i == self._nrows: return
            self._table[i][j].focus_set()
