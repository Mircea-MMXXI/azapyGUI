import pathlib
import json

import azapyGUI.configSettings as configSettings


def _fileMasterUserConfig():
    return pathlib.Path.home().joinpath(".azapyGUI/MasterUserConfig.json")


def _readMasterUserConfig():
    out_file = _fileMasterUserConfig()
    try:
        with open(out_file, 'r') as fp:
            data = json.load(fp)    
    except FileNotFoundError:
        data = configSettings.get_settings_default_all()
        out_file.parent.mkdir(exist_ok=True, parents=True)
        with open(out_file, 'w') as fp:
            json.dump(data, fp)
    return data


def _saveMasterUserConfig(data):
    out_file = _fileMasterUserConfig()
    out_file.parent.mkdir(exist_ok=True, parents=True)
    with open(out_file, 'w') as fp:
        json.dump(data, fp)
