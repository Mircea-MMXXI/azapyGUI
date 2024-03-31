import tkinter as tk
from tkinter import ttk
from typing import Union

Widget = Union[tk.Widget, ttk.Widget]

class ViewTip(tk.Toplevel):
    _FADE_INC:float = .07
    _FADE_MS :int   = 20
    
    def __init__(self, master, **kwargs):
        tk.Toplevel.__init__(self, master)

        self.attributes('-alpha', 0, '-topmost', True)
        self.overrideredirect(1)

        style = dict(bd=2, relief='raised', font='Ariel 10', bg='#D4D4D4', 
                     anchor='w', justify='left')
        self.label = tk.Label(self, **{**style, **kwargs})
        self.label.grid(row=0, column=0, sticky='w')
        
        self.fout:bool = False
        
        
    def bind(self, target:Widget, text:str, **kwargs):
        target.bind('<Enter>', lambda e: self._fadein(0, text, e))
        target.bind('<Leave>', lambda e: self._fadeout(1 - ViewTip._FADE_INC, e))
        
        
    def _fadein(self, alpha:float, text:str=None, event:tk.Event=None):
        if event and text:
            if self.fout:
                self.attributes('-alpha', 0)
                self.fout = False
            self.label.configure(text=f'{text:^{len(text)+2}}')
            self.update()

            offset_x = event.widget.winfo_width()+2
            offset_y = int((event.widget.winfo_height() - self.label.winfo_height()) / 2)

            w = self.label.winfo_width()
            h = self.label.winfo_height()
            x = event.widget.winfo_rootx()+offset_x
            y = event.widget.winfo_rooty()+offset_y

            self.geometry(f'{w}x{h}+{x}+{y}')
               
        if not self.fout:
            self.attributes('-alpha', alpha)
        
            if alpha < 1:
                self.after(ViewTip._FADE_MS, 
                           lambda: self._fadein(min(alpha + ViewTip._FADE_INC, 1)))


    def _fadeout(self, alpha:float, event:tk.Event=None):
        if event:
            self.fout = True
        
        if self.fout:
            self.attributes('-alpha', alpha)
        
            if alpha > 0:
                self.after(ViewTip._FADE_MS, 
                           lambda: self._fadeout(max(alpha - ViewTip._FADE_INC, 0)))
                
                
    def turned(self, on=True):
        if on:
            self.deiconify()
        else:
            self.withdraw()
