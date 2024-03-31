import tkinter as tk 


def enable_children(parent, enabled=True):
    for child in parent.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ('Frame', 'Labelframe', 'TFrame', 'TLabelframe'):
            child.configure(state=tk.NORMAL if enabled else tk.DISABLED)
        else:
            enable_children(child, enabled)


def enable_widget(widget, enabled=True):
    wtype = widget.winfo_class()
    if wtype not in ('Frame', 'Labelframe', 'TFrame', 'TLabelframe'):
        widget.configure(state=tk.NORMAL if enabled else tk.DISABLED)
    else:
        enable_children(widget, enabled)
