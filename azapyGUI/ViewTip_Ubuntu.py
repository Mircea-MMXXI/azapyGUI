import tkinter as tk
from tkinter import ttk
from typing import Union

Widget = Union[tk.Widget, ttk.Widget]


class ViewTip_Ubuntu(tk.Toplevel):
    def __init__(self, master, **kwargs):
        tk.Toplevel.__init__(self, master)

        self.attributes('-alpha', 0, '-topmost', True)
        self.overrideredirect(True)

        style = dict(bd=2, relief='raised', font='Ariel 10', bg='#D4D4D4', 
                     anchor='w', justify='left')
        self._label = tk.Label(self, **{**style, **kwargs})
        self._label.grid(row=0, column=0, sticky='w')

        self._view = True
        
        
    def bind(self, target:Widget, text:str, **kwargs):
        target.bind('<Enter>', lambda e: self._goin(text, e), add="+")
        target.bind('<Leave>', lambda e: self._goout(), add="+")
        
        
    def _goin(self, text:str=None, event:tk.Event=None):
        if not self._view: return
        self.deiconify()
        
        self._label.configure(text=f'{text:^{len(text) + 2}}')
        self.update()

        offset_x = event.widget.winfo_width() + 2
        offset_y = int((event.widget.winfo_height() - self._label.winfo_height()) / 2)

        w = self._label.winfo_width()
        h = self._label.winfo_height()
        x = event.widget.winfo_rootx() + offset_x
        y = event.widget.winfo_rooty() + offset_y

        self.geometry(f'{w}x{h}+{x}+{y}')


    def _goout(self):
        if not self._view: return
        self.withdraw()
                
                
    def turned(self, on:bool=True):
        self._view = on
