import pathlib
import json
import tkinter as tk

import azapyGUI.configSettings as configSettings


def _fileMasterUserConfig():
    return pathlib.Path.home().joinpath(".azapyGUI/MasterUserConfig.json")


def _readMasterUserConfig():
    try:
        out_file = _fileMasterUserConfig()
        with open(out_file, 'r') as fp:
            data = json.load(fp)    
        _update_version(data)
    except FileNotFoundError:
        data = configSettings.get_settings_default_all()
        _saveMasterUserConfig(data)

    return data


def _saveMasterUserConfig(data):
    out_file = _fileMasterUserConfig()
    out_file.parent.mkdir(exist_ok=True, parents=True)
    with open(out_file, 'w') as fp:
        json.dump(data, fp)


def _update_version(data):
    d_data = configSettings.get_settings_default_all()
    if data['Version'] == d_data['Version']:
        return 
    
    msg = f"The setting version was updated from {data['Version']} to {d_data['Version']}." + \
          "Please check the Settings for new updated values."
    tk.messagebox.showinfo(title='Setting Version Update', message=msg)
    data = {kk: data.get(kk, vv) for kk, vv in d_data.items()}
    data['Version'] = d_data['Version']
    _saveMasterUserConfig(data)
