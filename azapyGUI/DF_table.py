import tkinter as  tk 
import pandas as pd
import numpy as np
import platform
import numbers


class DF_table(tk.Frame):
    def __init__(self, df, master=None, **args):
        self._master = master if master is not None else tk.Toplevel()
        self._df = df
        
        self._bwidth = 2               #border width of each cell
        self._relife = "raised"        #cell style
        self._bg = 'white'             #background of regular header cells
        self._bg_data = 'white'        #background of data cells
        self._fg = 'black'             #foreground header cells
        self._fg_data_normal = 'black' #foreground of positive numerical data
        self._fg_data_mark = 'red'     #foreground ofr negative numerical data 
        self._bg_select = 'gray85'     #background of selectable header cells
        
        self._index_sort_ascending = True
        self._columns_sort_ascending = True
        
        super().__init__(master=self._master, **args)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
  
        self._canvas = tk.Canvas(master=self)
        self._canvas.grid(row=0, column=0, sticky=tk.NSEW)

        sv = tk.Scrollbar(master=self, orient=tk.VERTICAL, command=self._canvas.yview)
        sv.grid(row=0, column=1, sticky=tk.NS)
        self._canvas.configure(yscrollcommand=sv.set)  
        
        sh = tk.Scrollbar(master=self, orient=tk.HORIZONTAL, command=self._canvas.xview)
        sh.grid(row=1, column=0, sticky=tk.EW)
        self._canvas.configure(xscrollcommand=sh.set) 

        self._frm = tk.Frame(master=self._canvas, borderwidth=2, bg="black")
        self._frm.pack(fill=tk.BOTH, expand=True)
        
        self._canvas_window = self._canvas.create_window(0, 0, window=self._frm, anchor=tk.NW,)

        self._frm.bind("<Configure>", self._onFrameConfigure)
        self._canvas.bind("<Configure>", self._onCanvasConfigure)
            
        self._frm.bind('<Enter>', self._onEnter)
        self._frm.bind('<Leave>', self._onLeave)

        self._onFrameConfigure(None)      
   
        self._first_time= True
        self._draw(self._df)

        
    def _onFrameConfigure(self, event):                                              
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))


    def _onCanvasConfigure(self, event):
        if self._first_time:
            self._hh0 = self._frm.winfo_height()
            self._ww0 = self._frm.winfo_width()
            self._first_time = False
        canvas_width = max(event.width, self._ww0)
        canvas_heigth = max(event.height, self._hh0)
        self._canvas.itemconfig(self._canvas_window, width=canvas_width, height=canvas_heigth) 


    def _onMouseWheel(self, event):
        if platform.system() == 'Windows':
            self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == 'Darwin':
            self._canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self._canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self._canvas.yview_scroll(1, "units")


    def _onEnter(self, event):
        if platform.system() == 'Linux':
            self._canvas.bind_all("<Button-4>", self._onMouseWheel)
            self._canvas.bind_all("<Button-5>", self._onMouseWheel)
        else:
            self._canvas.bind_all("<MouseWheel>", self._onMouseWheel)
    
    
    def _onLeave(self, event):
        if platform.system() == 'Linux':
            self._canvas.unbind_all("<Button-4>")
            self._canvas.unbind_all("<Button-5>")
        else:
            self._canvas.unbind_all("<MouseWheel>")
        
        
    def _draw(self, df):
        tb_rows, tb_cols = df.shape
        nr_cnames = len(df.columns.names)
        nr_rnames = len(df.index.names)
 
        # header corner
        if (nr_cnames == 1) and (df.columns.names[0] is None):
            row = 0
            for col, rname in enumerate(df.index.names):
                lbl = tk.Label(master=self._frm, text=rname, justify=tk.LEFT, 
                               borderwidth=self._bwidth, relief=self._relife, anchor=tk.NW, 
                               bg=self._bg_select, fg=self._fg)
                lbl.grid(row=row, column=col, sticky=tk.EW, ipadx=2, ipady=2)
                lbl.bind("<Button-1>", self._swap_rows)
            col += 1
            sv = tk.Frame(master=self._frm, bg="black", width=1, bd=0)
            sv.grid(row = 0, column=col, rowspan=nr_cnames + 2 + tb_rows, sticky=tk.NS)
            for col in range(nr_rnames, nr_rnames + tb_cols):
                lbl = tk.Label(master=self._frm, text=df.columns[col - nr_rnames], justify=tk.LEFT, 
                               borderwidth=self._bwidth, relief=self._relife, anchor=tk.NW, 
                               bg=self._bg, fg=self._fg)
                lbl.grid(row=row, column=col + 1, sticky=tk.EW)
            row += 1
            sh = tk.Frame(master=self._frm, bg="black", height=1, bd=0)
            sh.grid(row=row, column=0, columnspan=nr_rnames + 1 + tb_cols, sticky=tk.EW)

            row_data = row + 1
            col_data = nr_rnames + 1
        else:
            columnspan = len(df.index.names)
            for row, cname in enumerate(df.columns.names):
                lbl = tk.Label(master=self._frm, text=cname, justify=tk.LEFT, 
                               borderwidth=self._bwidth, relief=self._relife, anchor=tk.NW, 
                               bg=self._bg_select, fg=self._fg)
                lbl.grid(row=row, columnspan=columnspan, sticky=tk.EW, ipadx=2, ipady=2)
                lbl.bind("<Button-1>", self._swap_cols)
                
            for name in df.index.names:
                if name is not None:
                    row += 1
                    for col, rname in enumerate(df.index.names):
                        lbl = tk.Label(master=self._frm, text=rname, justify=tk.LEFT, 
                                       borderwidth=self._bwidth, relief=self._relife, 
                                       anchor=tk.NW, bg=self._bg_select, fg=self._fg)
                        lbl.grid(row=row, column=col, sticky=tk.EW, ipadx=2, ipady=2)
                        lbl.bind("<Button-1>", self._swap_rows)
                    break
            row += 1
            sh = tk.Frame(master=self._frm, bg="black", height=1, bd=0)
            sh.grid(row=row, column=0, columnspan=nr_rnames + 1 + tb_cols, sticky=tk.EW)
            col = nr_rnames
            sv = tk.Frame(master=self._frm, bg="black", width=1, bd=0)
            sv.grid(row = 0, column=col, rowspan=nr_cnames + 2 + tb_rows, sticky=tk.NS)
            row_data = row + 1
            col_data = nr_rnames + 1
            # pad
            for col in range(row_data, row_data + tb_cols):
                lbl = tk.Label(master=self._frm, text="",
                               borderwidth=self._bwidth, relief=self._relife, anchor=tk.NW, 
                               bg=self._bg, fg=self._fg)
                lbl.grid(row=row_data - 2, column=col, sticky=tk.EW, ipadx=2, ipady=2)

            # header columns
            cspan = np.ones(nr_cnames, dtype=int)
            ent = [None for _ in range(nr_cnames)]
            for col, cname in enumerate(df.columns):
                cname = cname if isinstance(cname, tuple) else (cname, )
                if col == 0:
                    for kk in range(nr_cnames):
                        ent[kk] = tk.Label(master=self._frm, text=cname[kk], 
                                           borderwidth=self._bwidth, relief=self._relife, 
                                           anchor=tk.NW, bg=self._bg, fg=self._fg)
                        cname_ = cname
                    continue
                for j in range(nr_cnames):
                    if cname[j] == cname_[j]:
                        cspan[j] += 1
                    else:
                        for kk in range(j, nr_cnames):
                            column = col - cspan[kk] + col_data
                            ent[kk].grid(row=kk, column=column, columnspan=cspan[kk], 
                                         sticky=tk.EW, ipadx=2, ipady=2)
                            ent[kk] = tk.Label(master=self._frm, text=cname[kk], 
                                               borderwidth=self._bwidth, relief=self._relife, 
                                               anchor=tk.NW, bg=self._bg, fg=self._fg)
                            cspan[kk] = 1
                        break
                cname_ = cname     
            for kk in range(nr_cnames):
                ent[kk].grid(row=kk, column=col - cspan[kk] + col_data + 1, 
                             columnspan=cspan[kk], sticky=tk.EW, ipadx=2, ipady=2)
            
        # header index
        rspan = np.ones(nr_rnames, dtype=int)
        ent = [None for _ in range(nr_rnames)]
        for row, rname in enumerate(df.index):
            rname = rname if isinstance(rname, tuple) else (rname,)
            if row == 0:
                for kk in range(nr_rnames):
                    ent[kk] = tk.Label(master=self._frm, text=self._tr2str(rname[kk]), 
                                       borderwidth=self._bwidth, relief=self._relife, 
                                       anchor=tk.NW, bg=self._bg, fg=self._fg)
                    rname_ = rname
                continue
            for j in range(nr_rnames):
                if rname[j] == rname_[j]:
                    rspan[j] += 1
                else:
                    for kk in range(j, nr_rnames):
                        prow = row - rspan[kk] + row_data
                        ent[kk].grid(row=prow, column=kk, rowspan=rspan[kk], sticky=tk.NSEW)
                        ent[kk] = tk.Label(master=self._frm, text=self._tr2str(rname[kk]), 
                                           borderwidth=self._bwidth, relief=self._relife, 
                                           anchor=tk.NW, bg=self._bg, fg=self._fg)
                        rspan[kk] = 1
                    break
            rname_ = rname
        for kk in range(nr_rnames):
            ent[kk].grid(row=row - rspan[kk] + 1 + row_data, column=kk, 
                         rowspan=rspan[kk], sticky=tk.NSEW, ipadx=2, ipady=2)
            
        # data
        for col in range(df.shape[1]):
            self._frm.columnconfigure(col + col_data, weight=1)
            for row in range(df.shape[0]):
                ldata = df.iloc[row, col]
                if (pd.isna(ldata) or 
                    (isinstance(ldata, numbers.Number) and ldata < 0)):
                    fg_data = self._fg_data_mark
                else:
                    fg_data = self._fg_data_normal
                ent = tk.Label(master=self._frm, text=self._tr2str(ldata), borderwidth=self._bwidth, 
                               relief=self._relife, fg=fg_data, bg=self._bg_data)
                ent.grid(row = row_data + row, column=col + col_data, sticky=tk.NSEW)
                self._frm.rowconfigure(row_data + row, weight=1)
            
            
    def _swap_rows(self, event):
        wname = event.widget.cget("text")
        if wname == self._df.index.names[0]:
            self._index_sort_ascending = not self._index_sort_ascending
            self._df.sort_index(level=wname, 
                                ascending=self._index_sort_ascending, 
                                inplace=True)
            self._draw(self._df)
            return
        if isinstance(self._df.index, pd.MultiIndex): 
            self._index_sort_ascending = True
            self._df = self._df.swaplevel(0, wname)\
                           .sort_index(ascending=self._index_sort_ascending)
            self._draw(self._df)
        
        
    def _swap_cols(self, event):
        wname = event.widget.cget("text")
        if wname == self._df.columns.names[0]:
            self._columns_sort_ascending = not self._columns_sort_ascending
            self._df.sort_index(axis=1, level=wname, 
                                ascending=self._columns_sort_ascending, 
                                inplace=True)
            self._draw(self._df)
            return
        if isinstance(self._df.columns, pd.MultiIndex): 
            self._columns_sort_ascending = True
            self._df = self._df.swaplevel(0, wname, axis=1)\
                           .sort_index(axis=1, ascending=self._columns_sort_ascending)
            self._draw(self._df)
        
        
    def get_df(self):
        return self._df
    
    
    def _tr2str(self, name):
        if pd.isna(name):
            sname = ''
        elif isinstance(name, str):
            sname = name
        elif isinstance(name, numbers.Number):
            sname = str(name)
        else: #date
            sname = name.strftime('%Y-%m-%d')
            
        return sname
