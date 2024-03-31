import tkinter as tk 

import azapyGUI.config as config

class EntryNameWindow:
    def __init__(self, master=None, title=None, text=None, tip_text=None, btn_text="OK"):
        self._master = master

        self._window = tk.Toplevel()
        self._window.geometry("200x150")
        self._window.title(title)
        
        frm = tk.LabelFrame(master=self._window, text=title, font=("Forte", 10) )
        frm.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        row = 0
        frm.rowconfigure(row, weight=1)
        lbl = tk.Label(master=frm, text=text)
        lbl.grid(row=row, columnspan=2, pady=5, padx=5, sticky=tk.EW)
        
        row += 1         
        frm.rowconfigure(row, weight=1)
        self._ent = tk.Entry(master=frm, width=20)
        self._ent.grid(row=row, columnspan=2, padx=10, pady=5, sticky=tk.EW)
        self._ent.bind('<Return>', lambda event: self._btn_save())
        self._ent.focus()
        if tip_text is not None:
            config.tiptil.bind(self._ent, tip_text)
        
        row += 1
        frm.columnconfigure(0, weight=1)
        btn_calcel = tk.Button(master=frm, text="Cancel", command=self._btn_cancel, width=8)
        btn_calcel.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        frm.columnconfigure(0, weight=1)
        
        btn_save = tk.Button(master=frm, text=btn_text, command=self._btn_save, width=8)
        btn_save.grid(row=row, column=1, padx=5, pady=5, sticky=tk.E)
        frm.columnconfigure(1, weight=1)

        self._window.update()
        if (self._master is not None) and self._master.winfo_exists():
            self._master.wait_window(self._window)
            
            
    def _btn_cancel(self):
        self._window.grab_release()
        if (self._master is not None) and self._master.winfo_exists():
            self._master.focus_set()
        self._window.destroy()
        
        
    def _btn_save(self):
        # to be implemented by derived class
        pass

