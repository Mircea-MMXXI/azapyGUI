import platform

from azapyGUI.ViewTip_Ubuntu import ViewTip_Ubuntu
from azapyGUI.ViewTip_fade import ViewTip_fade
from azapyGUI.ViewTip_fast import ViewTip_fast


def ViewTip(master, **kwargs):
    if platform.system() == 'Windows':
        return ViewTip_fade(master, **kwargs)
    else:
        return ViewTip_Ubuntu(master, **kwargs)
