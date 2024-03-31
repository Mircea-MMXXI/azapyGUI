import os
import azapyGUI.configTips as configTips
from azapyGUI.modelParametersValidation import _validDateMMDDYYYY, _validInt, _validIntNegative, _validIntPositive

Version = '0.0.1'

settings_model = {"Directors": {"UserPortfolioDirectory": {"default": None,
                                                           "type": 'ButtonDir',
                                                           "field": 'Portfolios Directory',
                                                           "tip": configTips._settings_UserPortfolioDirectory_tip,
                                                           "title": 'Portfolios Directory',
                                                          },
                                "UserMktDataDirectory": {"default": None,
                                                         "type": 'ButtonDir',
                                                         "field": 'Market Data Directory',
                                                         "tip": configTips._settings_UserMktDataDirectory_tip,
                                                         "title": 'Market Data Directory',
                                                         },
                                "UserOutputDirectory": {"default": None,
                                                        "type": 'ButtonDir',
                                                        "field": 'Data Output Directory',
                                                        "tip": configTips._settings_UserOutputDirectory_tip,
                                                        "title": 'Data Output Directory'
                                                        },
                                },
                  "MkTData": {"Provider": {"default": {'yahoo': {}},
                                           "type": 'MCheckbutton',
                                           "field": "Market data provider",
                                           "tip": configTips._settings_MkTDataProvider_tip,
                                           "values": {"yahoo": {},
                                                      "alphavantage": {"key": {"default": None,
                                                                               "type": 'str',
                                                                               "field": 'Provider Access Key',
                                                                               "tip": configTips._settings_porviderKey_tip,
                                                                               "envkey": 'ALPHAVANTAGE_API_KEY',
                                                                               },
                                                                       "max_req_per_min": {"default": 50,
                                                                                           "type": 'int',
                                                                                           "field": 'Max Requests / minute',
                                                                                           "tip": configTips._settings_max_req_per_min_tip,
                                                                                           },
                                                                       },
                                                      "eofhistoricaldata": {"key": {"default": None,
                                                                                    "type": 'str',
                                                                                    "field": 'Provider Access Key',
                                                                                    "tip": configTips._settings_porviderKey_tip,
                                                                                    "envkey": 'EODHISTORICALDATA_API_KEY',
                                                                                    },
                                                                            },
                                                      "marketstack": {"key": {"default": None,
                                                                              "type": 'str',
                                                                              "field": 'Provider Access Key',
                                                                              "tip": configTips._settings_porviderKey_tip,
                                                                              "envkey": 'MARKETSTACK_API_KEY',
                                                                              },
                                                                      },
                                                      },
                                           },
                                "force": {"default": False,
                                          "type": 'Checkbutton',
                                          "field": 'force',
                                          "tip": configTips._settings_force_default_tip,
                                          },
                              },
                               
                  "Miscellaneous": {"edate": {"default": 'today',
                                              "type": 'Entry',
                                              "field": '"edate" default value',
                                              "tip": configTips._settings_edate_default_tip,
                                              "validate": _validDateMMDDYYYY,
                                              },
                                    "sdate": {"default": '1/1/2012',
                                              "type": 'Entry',
                                              "field": '"sdate" default value',
                                              "tip": configTips._settings_sdate_default_tip,
                                              "validate": _validDateMMDDYYYY,
                                              },
                                    "noffset": {"default": -3,
                                                "type": 'Entry',
                                                "field": '"noffset" default value',
                                                "tip": configTips._settings_noffset_default_tip,
                                                "validate": _validInt,
                                                },
                                    "fixoffset": {"default": -1,
                                                  "type": 'Entry',
                                                  "field": '"fixoffset" default value',
                                                  "tip": configTips._settings_fixoffset_default_tip,
                                                  "validate": _validIntNegative,
                                                  },
                                    "capital": {"default": 100000,
                                                "type": 'Entry',
                                                "field": 'Capital default value',
                                                "tip": configTips._settings_capital_default_tip,
                                                "validate": _validIntPositive,
                                                },
                                    "nsh_round": {"default": True,
                                                  "type": 'Checkbutton',
                                                  "field": 'Int. nr. shares',
                                                  "tip": configTips._settings_nsh_round_default_tip,
                                                  },
                                    "OpenExcel": {"default": False,
                                                  "type": 'Checkbutton',
                                                  "field": 'Open Excel',
                                                  "tip": configTips._settings_OpenExcel_tip,
                                                  },
                                    "ShowTips": {"default": True,
                                                 "type": 'Checkbutton',
                                                 "field": 'Show Tips',
                                                 "tip": configTips._settings_ShowTips_tip,
                                                 },
                                                      
                                    },
                  }

 

def get_settings_default(category):
    rout = {kk:  vv["default"] for kk, vv in settings_model[category].items()}
    return rout


def get_settings_default_all():
    rout = {}
    rout["Version"] = Version
    for category in settings_model.keys():
        rout.update(get_settings_default(category))
    return rout
    

def get_envkey_valriable_name(provider):
    return settings_model["MkTData"]["Provider"]["values"][provider]["key"]["envkey"]


def get_envkey(provider):
    return os.getenv(get_envkey_valriable_name(provider))


MasterApplicationSettings = None
