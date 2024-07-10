import tkinter as tk
from tkinter import ttk
from typing import Union

Widget = Union[tk.Widget, ttk.Widget]


class ViewTip_fade(tk.Toplevel):
    def __init__(self, master, fade_inc=0.07, fade_ms=20, **kwargs):
        tk.Toplevel.__init__(self, master)
        self._fade_inc = fade_inc
        self._fade_ms = fade_ms

        self.attributes('-alpha', 0, '-topmost', True)
        self.overrideredirect(1)

        style = dict(bd=2, relief='raised', font='Ariel 10', bg='#D4D4D4', 
                     anchor='w', justify='left')
        self._label = tk.Label(self, **{**style, **kwargs})
        self._label.grid(row=0, column=0, sticky='w')
        
        self._fout:bool = False
        
        
    def bind(self, target:Widget, text:str, **kwargs):
        target.bind('<Enter>', lambda e: self._fadein(0, text, e), add="+")
        target.bind('<Leave>', lambda e: self._fadeout(1 - self._fade_inc, e), add="+")
        
        
    def _fadein(self, alpha:float, text:str=None, event:tk.Event=None):
        if event and text:
            if self._fout:
                self.attributes('-alpha', 0)
                self._fout = False

            self._label.configure(text=f'{text:^{len(text) + 2}}')
            self.update()

            offset_x = event.widget.winfo_width() + 2
            offset_y = int((event.widget.winfo_height() - self._label.winfo_height()) / 2)

            w = self._label.winfo_width()
            h = self._label.winfo_height()
            x = event.widget.winfo_rootx() + offset_x
            y = event.widget.winfo_rooty() + offset_y

            self.geometry(f'{w}x{h}+{x}+{y}')
               
        if not self._fout:
            self.attributes('-alpha', alpha)
        
            if alpha < 1:
                self.after(self._fade_ms, 
                           lambda: self._fadein(min(alpha + self._fade_inc, 1)))


    def _fadeout(self, alpha:float, event:tk.Event=None):
        if event:
            self._fout = True
        
        if self._fout:
            self.attributes('-alpha', alpha)
            
            if alpha > 0:
                self.after(self._fade_ms, 
                           lambda: self._fadeout(max(alpha - self._fade_inc, 0)))
                
                
    def turned(self, on=True):
        if on:
            self.deiconify()
        else:
            self.withdraw()
