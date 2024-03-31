import tkinter as tk
import platform


class Scrollable(tk.Frame):
    def __init__(self, frame, sbwidth=16, canv_width=200, canv_height=200, **kwargs):

        scrollbar = tk.Scrollbar(frame, width=sbwidth)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        
        self._canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set, 
                                width=canv_width, height=canv_height)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self._canvas.yview)
        self._canvas.bind('<Configure>', self._fill_canvas)
        super().__init__(frame, **kwargs)
        
        self.windows_item = self._canvas.create_window(0, 0, window=self, anchor=tk.NW)

        self.bind('<Enter>', self._onEnter)
        self.bind('<Leave>', self._onLeave)


    def _fill_canvas(self, event):
        canvas_width = event.width
        self._canvas.itemconfig(self.windows_item, width=canvas_width)

    
    def update(self):
        self.update_idletasks()
        self._canvas.config(scrollregion=self._canvas.bbox(self.windows_item))


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
