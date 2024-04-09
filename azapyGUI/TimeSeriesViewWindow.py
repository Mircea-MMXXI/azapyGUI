import tkinter as tk 
from tkinter import ttk
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as  pd
import os
import webbrowser
import azapy as az

import azapyGUI.config as config
import azapyGUI.configPlot as configPlot
import azapyGUI.configSettings as configSettings
import azapyGUI.configHelps as configHelps
from azapyGUI.CrossHairBCursor import CrossHairBCursor
from azapyGUI.DF_Window import DF_Window

WIDTH_CBX = 11
SCALE_OFFSET = 0

class TimeSeriesViewWindow(tk.Toplevel):
    def __init__(self, master=None, name=None, data=None, ref_name=None, col_name=None):
        super().__init__()
        self._scale_refresh = True
        self._fig_legend_refresh = True
        self._ref_name_refresh = True
        
        self._plot_lines_dict = {}
        self._tops_ww = {}
        
        self._master = master
        self._name = name
        self._data = data
        self._ref_name = ref_name
        self._col_name = col_name
        self._report_names = ['Summary', 'Annual', 'Quarterly', 'Monthly', 'Drawdowns']
        
        self._visible = {kk: True for kk in self._data.keys()}
 
        self._window = self
        self._window.title("Statistics")
        self._window.focus_set()
        self._window.protocol("WM_DELETE_WINDOW", self._btn_quit_func)

        menubar = tk.Menu(self._window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Help', command=self._menu_help_func)
        menubar.add_cascade(label='Help', menu=filemenu)
        self._window.config(menu=menubar)

        self._data_info()
        
        # frames: general <- (left-plot, right-btn)
        frm_top = tk.LabelFrame(master=self._window, text='View & Stats')
        frm_top.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        frm_plot_0 = tk.Frame(master=frm_top)
        frm_plot_0.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        self.frm_plot = tk.Frame(master=frm_plot_0)
        self.frm_plot.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        
        self.frm_btn = tk.Frame(master=frm_top, width=100)
        self.frm_btn.pack(fill=tk.Y, expand=False, side=tk.RIGHT)

        # frm_plot - left side plot 
        self._fig = Figure(figsize=(8, 5), dpi=120)
        self._ax = self._fig.add_subplot(111)
        
        self._ax.label_outer()
        self._ax.tick_params(axis='x', labelrotation=35, which='both')
        self._ax.tick_params(axis='both', which='both', labelsize=8)
        
        self._pt_name = 'linear' if len(self._data.keys()) < 2 else "rel-linear"
        self._dstart = self._data[self._ref_name].index[0]
        self._mark = '-'
        #self._dref = pd.Timestamp(mdates.num2date(0)).normalize().tz_localize(None)
        self._dref = self._dstart
        self._from_date = tk.StringVar(master=frm_plot_0)
        self._to_date = tk.StringVar(master=frm_plot_0)
        self._current_mouse_x = tk.StringVar(master=frm_plot_0, value="")
        self._current_mouse_y = tk.DoubleVar(master=frm_plot_0, value=0)
     
        self._scale = tk.Scale(frm_plot_0, orient=tk.HORIZONTAL, length=200, 
                               showvalue=0, sliderlength=20,
                               command=self._scale_func)
        self._scale.pack(fill=tk.X, expand=True, side=tk.TOP)
        
        self._canvas = FigureCanvasTkAgg(figure=self._fig, master=self.frm_plot)  
        self._canvas.draw()
        self._canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5, padx=5)
        self._prep_fig()
        self._CHcursor = CrossHairBCursor(self._ax, 
                                          varx = tk.StringVar(), vary=tk.StringVar(),
                                          transformx=lambda x: mdates.num2date(x).strftime("%Y-%m-%d"),
                                          transformy=lambda y: str(round(y,2))
                                          )
        self._fig.canvas.mpl_connect('motion_notify_event', self._CHcursor.on_mouse_move)
        self._fig.canvas.mpl_connect('button_press_event', self._on_mouse_press)

        self._canvas.draw()
   
        # self.frm_btn - right side buttons etc 
        frm_reference = tk.LabelFrame(master=self.frm_btn, text="Reference")
        frm_reference.pack(side=tk.TOP, fill=tk.X)
        
        self._cbx_ref = tk.StringVar(master=frm_reference, value=self._ref_name)
        if self._isMultiLines and not self._isEqualLines:
            cbx_ref = ttk.Combobox(master=frm_reference, textvariable=self._cbx_ref, 
                                   width=WIDTH_CBX, state='readonly')
            cbx_ref['values'] = tuple(self._data.keys())
            cbx_ref.pack(pady=5, padx=5, side=tk.TOP,)
            cbx_ref.bind("<<ComboboxSelected>>",  self._cbx_ref_func)
        
        lfrm_view = tk.LabelFrame(master=self.frm_btn, text='Set view')
        lfrm_view.pack(side=tk.TOP, fill=tk.X)
        
        self._cbx = tk.StringVar(master=lfrm_view, value=self._col_name)
        if self._isMultiColumns:
            cbx = ttk.Combobox(master=lfrm_view, textvariable=self._cbx, 
                               width=WIDTH_CBX, state='readonly')
            cbx['values'] = tuple(self._data[self._ref_name].columns)
            cbx.pack(pady=5, padx=5, side=tk.TOP,)
            cbx.bind("<<ComboboxSelected>>",  self._cbx_func)
        
        self._cbx_ptype = tk.StringVar(master=lfrm_view, value=self._pt_name)
        cbx_ptype = ttk.Combobox(master=lfrm_view, textvariable=self._cbx_ptype, 
                                 width=WIDTH_CBX, state='readonly')
        cbx_ptype['values'] = tuple(configPlot._plot_types.keys())
        cbx_ptype.pack(pady=5, padx=5, side=tk.TOP,)
        cbx_ptype.bind("<<ComboboxSelected>>",  self._cbx_ptype_func)
        
        self._cbx_length = tk.StringVar(master=lfrm_view, value='Max')
        cbx_length = ttk.Combobox(master=lfrm_view, textvariable=self._cbx_length, 
                                        width=WIDTH_CBX, state='readonly')
        cbx_length['values'] = tuple(configPlot._plot_lengths.keys())
        cbx_length.pack(pady=5, padx=5, side=tk.TOP,)
        cbx_length.bind("<<ComboboxSelected>>",  self._cbx_length_func)
        
        lfrm_reports = tk.LabelFrame(master=self.frm_btn, text='Reports')
        lfrm_reports.pack(side=tk.TOP, fill=tk.X)
        
        self._cbx_reports = tk.StringVar(master=lfrm_reports)
        cbx_reports = ttk.Combobox(master=lfrm_reports, textvariable=self._cbx_reports, 
                                         width=WIDTH_CBX, state='readonly')
        cbx_reports['values'] = self._report_names
        cbx_reports.current(0)
        cbx_reports.pack(pady=5, padx=5, side=tk.TOP,)
        cbx_reports.bind("<<ComboboxSelected>>",  self._cbx_reports_func)
        
        # TOP - BOTTOM
        btn = tk.Button(master=self.frm_btn, text="Exit", width=WIDTH_CBX, command=self._btn_quit_func)
        btn.pack(pady=5, padx=5, side=tk.BOTTOM,)
        
        frm_ts = tk.LabelFrame(master=self.frm_btn, text="In view")
        frm_ts.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(master=frm_ts, text="From:", anchor=tk.W).pack(side=tk.TOP, anchor=tk.W)
        tk.Label(master=frm_ts, textvariable=self._from_date).pack(side=tk.TOP)
        tk.Label(master=frm_ts, text="To:", anchor=tk.W).pack(side=tk.TOP, anchor=tk.W)
        tk.Label(master=frm_ts, textvariable=self._to_date).pack(side=tk.TOP)

        frm_current = tk.LabelFrame(master=self.frm_btn, text="Cross")
        frm_current.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(master=frm_current, textvariable=self._CHcursor.varx).pack(side=tk.TOP)
        tk.Label(master=frm_current, textvariable=self._CHcursor.vary).pack(side=tk.TOP)
        
        lfrm_save = tk.LabelFrame(master=self.frm_btn, text='Save')
        lfrm_save.pack(side=tk.BOTTOM, fill=tk.X)
        
        self._cbx_save = tk.StringVar(master=lfrm_save)
        cbx_save = ttk.Combobox(master=lfrm_save, textvariable=self._cbx_save, 
                                      width=WIDTH_CBX, state='readonly')
        cbx_save['values'] = ('Chart', 'To Excel') + tuple(self._data.keys())
        cbx_save.current(0)
        cbx_save.pack(pady=5, padx=5, side=tk.TOP)
        cbx_save.bind("<<ComboboxSelected>>",  self._cbx_save_func)
        

    def _data_info(self):
        self._isMultiLines = True if len(self._data.keys()) > 1 else False
        self._isMultiColumns = True if len(self._data[self._ref_name].columns) > 1 else False
        self._isEqualLines = True
        if self._isMultiLines:
            sds = self._data[self._ref_name].index[-1]
            ede = self._data[self._ref_name].index[0]
            for dd in self._data.values():
                if (dd.index[-1] != sds) or (dd.index[0] != ede): 
                    self._isEqualLines = False
                    return


    def _prep_fig(self):
        # calc TS
        tref = self._data[self._ref_name].index
        tref = tref[tref >= self._dstart]
        ty = {}
        for kk, vv in self._data.items():
            ty[kk] = {}
            t = vv.index[vv.index >= self._dref]
            ty[kk]['t'] = t
            ty[kk]['y'] =vv[self._col_name].loc[t[0]:]
          
        # relative and percent plots
        if configPlot._plot_types[self._pt_name]['relative']:
            ty[self._ref_name]['y'] = ty[self._ref_name]['y'] / ty[self._ref_name]['y'].iloc[0]
            for kk in ty.keys():
                if kk == self._ref_name: continue
                ty[kk]['y'] = ty[kk]['y'] * (ty[self._ref_name]['y'].loc[ty[kk]['t'][0]] / ty[kk]['y'].iloc[0])
             
            # percent plots
            if configPlot._plot_types[self._pt_name]['percent']:
                for kk in ty.keys():
                    ty[kk]['y'] = (ty[kk]['y'] - 1) * 100
         
        # set from - to for labels
        self._from_date.set(ty[self._ref_name]['t'][0].strftime("%Y-%m-%d"))
        self._to_date.set(ty[self._ref_name]['t'][-1].strftime("%Y-%m-%d"))
        
        # clear and redraw
        self._ax.clear()
        for kk, vv in ty.items():
            self._plot_lines_dict[kk],  = self._ax.plot(vv['t'], vv['y'], 
                                                        self._mark, 
                                                        label=kk, lw=1, 
                                                        visible=self._visible[kk])
        # title choice
        if self._ref_name_refresh:
            if self._name is None:
                self._ax.set_title(self._ref_name +' ('+ self._col_name +')')
            else:
                self._ax.set_title(self._name +' ('+ self._col_name +')')
             
        # format axis
        self._ax.set_yscale(**configPlot._plot_types[self._pt_name]['param'])
        self._ax.grid(**configPlot._plot_types[self._pt_name]['xgrid'])
        self._ax.grid(**configPlot._plot_types[self._pt_name]['ygrid'])
        
        self._ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
        self._ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
        
        # build legend - only first time when this function is called
        if self._fig_legend_refresh:
            self._leg = self._fig.legend(loc='upper left', fontsize = 6)
            self._fig.canvas.mpl_connect('pick_event', self._on_pick)
            for legl in self._leg.get_lines():
                legl.set_picker(5)
            self._leg.set_draggable(True)
            self._fig_legend_refresh = False
         
        # set resolution for scale widget
        if self._scale_refresh:
            lfrom = mdates.date2num(self._dstart)
            self._scale.configure(from_=lfrom, to=mdates.date2num(tref[-2]))
            self._scale.set(mdates.date2num(self._dref))
            self._scale_refresh = False
            
        
    def _on_pick(self, event):
        legend_line = event.artist
        name = legend_line.get_label()
        if name not in self._plot_lines_dict.keys(): return
        
        ax_line = self._plot_lines_dict[name]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        self._visible[name] = visible
        legend_line.set_alpha(1.0 if visible else 0.2)
        self._fig.canvas.draw()
        
        
    def _on_mouse_press(self, event):
        xc = event.xdata
        if xc is None: return
        dl = mdates.date2num(self._dstart)
        dr = mdates.date2num(self._data[self._ref_name].index[-1])
        xc = int(xc)
        if (xc <= dl) or (xc >= dr): return
        self._dref = pd.Timestamp(mdates.num2date(xc)).normalize().tz_localize(None)
        self._scale.set(xc)
        self._cbx_func(1)
        
        
    def _scale_func(self, val):
        ival = int(val)
        self._dref = pd.Timestamp(mdates.num2date(ival)).normalize().tz_localize(None)
        self._cbx_func(1)
              
        
    def _cbx_func(self, event):
        self._col_name = self._cbx.get()
        self._prep_fig()
        self._CHcursor.set_ax(self._ax)
        self._canvas.draw()
        
        
    def _cbx_ptype_func(self, event):
        self._pt_name = self._cbx_ptype.get()
        self._cbx_func(event)

        
    def _cbx_length_func(self, event):
        lt = self._cbx_length.get()
        self._dstart = max(self._data[self._ref_name].index[0],
                           configPlot._plot_lengths[lt]['offset'](self._data[self._ref_name].index[-1]))
        self._mark = configPlot._plot_lengths[lt]['mark']
        self._scale_refresh = True
        self._dref = max(self._dstart, self._dref) if event == 1 else self._dstart
        self._cbx_func(event)
        
        
    def _cbx_ref_func(self, event):
        self._ref_name = self._cbx_ref.get()
        self._ref_name_refresh = True
        self._cbx_length_func(1)
        
        
    def _btn_quit_func(self):
        for vv in self._tops_ww.values(): 
            if vv['ww'] is not None: vv['ww'].destroy()
        if (self._master is not None) and self._master.winfo_exists(): 
            self._master.focus_set()
        self._window.destroy()


    def _btn_save_chart_func(self):
        filesextensions = [("PNG", "*.png"), ("JPG", "*.jpg"), ("PDF", "*.pdf")]
        path = tk.filedialog.asksaveasfilename(
            filetypes=filesextensions,
            defaultextension = filesextensions,
            initialdir=configSettings.MasterApplicationSettings["UserOutputDirectory"],
            initialfile='Fig.png',
        )
        if path:
            self._fig.savefig(path)
            
            
    def _btn_save_excel_func(self):
        port_path = configSettings.MasterApplicationSettings["UserOutputDirectory"]
        path = tk.filedialog.asksaveasfilename(
                                    defaultextension=".xlsx",
                                    filetypes=[("Excel Files", "*.xlsx")],
                                    initialdir=port_path,
                                    initialfile='Data.xlsx',
                                    parent=self._window
                                    )
        if path:
            with pd.ExcelWriter(path, mode='w', engine='xlsxwriter', 
                                date_format="YYYY-MM-DD", 
                                datetime_format="YYYY-MM-DD") as writer:
                for kk, vv in self._data.items():
                    vv.to_excel(writer, sheet_name=kk)
            if configSettings.MasterApplicationSettings["OpenExcel"]:
                try:
                    os.system('start EXCEL.EXE ' + path)
                except:
                    pass
            
    
    def _cbx_save_func(self, event):
        dname = self._cbx_save.get()
        if dname == 'Chart':
            self._btn_save_chart_func()
            return
        if dname == 'To Excel':
            self._btn_save_excel_func()
            return
        
        port_path = configSettings.MasterApplicationSettings["UserOutputDirectory"]
        path = tk.filedialog.asksaveasfilename(
                                    defaultextension=".csv",
                                    filetypes=[("Excel Files", "*.csv")],
                                    initialdir=port_path,
                                    initialfile=dname + '.csv',
                                    parent=self._window
                                    )
        if path:
            self._data[dname].to_csv(path)
            
            
    def _prep_reports(self):       
        obj = az.Port_Simple(self._data, col=self._col_name)
        obj.set_model()
        su = obj.port_perf(componly=True)
        an = obj.port_annual_returns(withcomp=True, componly=True)
        mo = obj.port_monthly_returns(withcomp=True, componly=True)
        qu = obj.port_quarterly_returns(withcomp=True, componly=True)
        dr = obj.port_drawdown(withcomp=True, componly=True)
        
        # monthly
        mo.index = pd.MultiIndex.from_arrays(
                                [mo.index.year.to_list(),
                                 mo.index.month_name().to_list()],
                                 names= ['year', 'month'])
 
        mo = mo.stack().unstack('month')
        mo.columns = pd.Series(mo.columns).apply(lambda x: x[:3])
        mo.columns = pd.Categorical(mo.columns, categories=config._months_name, ordered=True)
        mo.sort_index(axis=1, inplace=True)

        # quarterly
        qu.index = pd.MultiIndex.from_arrays(
                                [qu.index.year.to_list(),
                                 ['Q' + str(k) for k in qu.index.quarter]],
                                 names= ['year', 'quarter'])
 
        qu = qu.stack().unstack('quarter')

        # annual
        an = an.stack()
        an.name = 'Annual'
        
        # summary
        cols = ['RR', 'DD', 'RoMaD']
        su[cols] = (su[cols] * 100).round(2)
        rname = self._report_names[0] + self._col_name
        self._tops_ww[rname] = {}
        self._tops_ww[rname]['report'] = su
        self._tops_ww[rname]['ww'] = None
        self._tops_ww[rname]['geometry'] = '400x200'
        self._tops_ww[rname]['title'] = f'Summary Rep. {self._col_name} prices'
        
        # monthly
        mo = (pd.concat([an, mo], join='outer', axis=1) * 100).round(2).fillna('')
        rname = self._report_names[3] + self._col_name
        self._tops_ww[rname] = {}
        self._tops_ww[rname]['report'] = mo
        self._tops_ww[rname]['ww'] = None
        self._tops_ww[rname]['geometry'] = '600x300'
        self._tops_ww[rname]['title'] = f'Monthly Rep. {self._col_name} prices'

        # quarterly
        qu = (pd.concat([an, qu], join='outer', axis=1) * 100).round(2).fillna('')
        rname = self._report_names[2] + self._col_name
        self._tops_ww[rname] = {}
        self._tops_ww[rname]['report'] = qu
        self._tops_ww[rname]['ww'] = None
        self._tops_ww[rname]['geometry'] = '350x300'
        self._tops_ww[rname]['title'] = f'Quarterly Rep. {self._col_name} prices'
        
        # annual
        an = (pd.DataFrame(an).unstack('symbol').droplevel(0, 1) * 100).round(2).fillna('')
        an.columns.name = None
        rname = self._report_names[1] + self._col_name
        self._tops_ww[rname] = {}
        self._tops_ww[rname]['report'] = an
        self._tops_ww[rname]['ww'] = None
        self._tops_ww[rname]['geometry'] = '300x300'
        self._tops_ww[rname]['title'] = 'Annual Rep. ' + self._col_name + ' prices'
        
        # drawdown
        dr.DD = (dr.DD * 100).round(2)
        dr.fillna('', inplace=True)
        rname = self._report_names[4] + self._col_name
        self._tops_ww[rname] = {}
        self._tops_ww[rname]['report'] = dr
        self._tops_ww[rname]['ww'] = None
        self._tops_ww[rname]['geometry'] = '400x300'
        self._tops_ww[rname]['title'] = 'Drawdown Rep. ' + self._col_name + ' prices'
        
 
    def _cbx_reports_func(self, event):
        rep_name = self._cbx_reports.get()
        rname = rep_name + self._col_name
        
        if rname not in self._tops_ww.keys(): self._prep_reports()
        if ((self._tops_ww[rname]['ww'] is not None) and
            self._tops_ww[rname]['ww'].winfo_exists()):
            self._tops_ww[rname]['ww'].lift()
            return
        
        self._tops_ww[rname]['ww'] = DF_Window(self._window, 
                                               self._tops_ww[rname]['report'],
                                               self._tops_ww[rname]['title'],
                                               self._tops_ww[rname]['geometry'],
                                               rname,
                                               )

    def _menu_help_func(self):
        webbrowser.open_new_tab(configHelps._Statistics_panel_help)
        