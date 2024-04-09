import pandas as pd
import azapy as az

import azapyGUI.config as config

# need to mode this to azapy 
def schedule_date(sdate, edate, freq='Q', fixoffset=-1, **kwargs):
    qdate = pd.Timestamp(edate).to_period(freq).end_time.normalize().tz_localize(None)
    noffset = -pd.bdate_range(edate, qdate, freq=config._bday).size + 1 - fixoffset
    return az.schedule_simple(sdate=sdate, edate=edate, freq=freq, 
                              noffset=noffset, fixoffset=fixoffset, 
                              calendar=config.calendar)

# need to incorporate into azapy
def UniversalEngineWrap(mktdata=None, colname='adjusted', freq='M', name='Universal',
                 schedule=None, sdate=None, edate='today', noffset=0, 
                 fixoffset=-1, hlength=12, dirichlet_alpha=None, 
                 variance_reduction=True, nr_batches=16, mc_paths=100, 
                 mc_seed=42, verbose=False):
    
    fixing_schedule = schedule_date(sdate, edate, freq=freq, fixoffset=fixoffset)
    return az.UniversalEngine(mktdata=mktdata, colname=colname, freq=freq, 
                              schedule=fixing_schedule,
                              sdate=sdate, edate=edate, noffset=noffset, fixoffset=fixoffset, hlength=hlength,
                              dirichlet_alpha=dirichlet_alpha, variance_reduction=variance_reduction,
                              nr_batches=nr_batches, mc_paths=mc_paths, mc_seed=mc_seed,
                              verbose=verbose)
