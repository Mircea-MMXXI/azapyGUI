import pandas as pd

import azapyGUI.config as config


def sdate_edate_validate(sdate, edate):
    try:
        _sdate, _edate = _mkt_sedate(sdate, edate)
    except:
        msg = "Warning: wrong date format"
        return False, msg, False
        
    if _edate < _sdate:
        msg = "Warning: end date smaller than start data"
        return False, msg, False
    
    return True, _sdate, _edate
    

def mkt_today():
    dn = pd.Timestamp.now(tz='America/New_York')
    reftime = dn.replace(hour=16, minute=0, second=0, microsecond=0)
    if dn > reftime: return dn.normalize().tz_localize(None)

    return config._bday.rollback(dn - pd.Timedelta(1, 'day')).normalize().tz_localize(None)


def _mkt_sedate(sdate, edate):
    dn = pd.Timestamp.now(tz='America/New_York')
    refdate = dn.replace(hour=16, minute=0, second=0, microsecond=0)
    if dn > refdate:
        refdate = config._bday.rollback(refdate).normalize().tz_localize(None)
    else:
        refdate = config._bday.rollback(refdate - pd.Timedelta(1, 'day')).normalize().tz_localize(None)
    edate = min(pd.to_datetime(edate).normalize().tz_localize(None), refdate)
    if sdate == '': 
        sdate = edate
    elif sdate.strip('-').isnumeric() and (int(sdate) <= 0):
        sdate = edate + int(sdate) * config._bday
    else:
        sdate = config._bday.rollforward(sdate).normalize().tz_localize(None)
    return sdate, edate
