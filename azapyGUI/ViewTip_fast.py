import tkinter as tk
from tkinter import ttk
from typing import Union

Widget = Union[tk.Widget, ttk.Widget]


class ViewTip_fast(tk.Toplevel):
    def __init__(self, master, fade_inc=0.07, fade_ms=20, **kwargs):
        tk.Toplevel.__init__(self, master)
        self._fade_inc = fade_inc
        self._fade_ms = fade_ms

        self.attributes('-alpha', 0, '-topmost', True)
        self.overrideredirect(True)

        style = dict(bd=2, relief='raised', font='Ariel 10', bg='#D4D4D4', 
                     anchor='w', justify='left')
        self._label = tk.Label(self, **{**style, **kwargs})
        self._label.grid(row=0, column=0, sticky='w')

        
    def bind(self, target:Widget, text:str, **kwargs):
        target.bind('<Enter>', lambda e: self._goin(text, e), add="+")
        target.bind('<Leave>', lambda e: self._goout(), add="+")
        
        
    def _goin(self, text:str=None, event:tk.Event=None):
        if text is None: return
        
        self._label.configure(text=f'{text:^{len(text) + 2}}')
        self.update()

        offset_x = event.widget.winfo_width() + 2
        offset_y = int((event.widget.winfo_height() - self._label.winfo_height()) / 2)

        w = self._label.winfo_width()
        h = self._label.winfo_height()
        x = event.widget.winfo_rootx() + offset_x
        y = event.widget.winfo_rooty() + offset_y

        self.geometry(f'{w}x{h}+{x}+{y}')

        self.attributes('-alpha', 1)


    def _goout(self):
        self.attributes('-alpha', 0)
                
                
    def turned(self, on=True):
        if on:
            self.deiconify()
        else:
            self.withdraw()
