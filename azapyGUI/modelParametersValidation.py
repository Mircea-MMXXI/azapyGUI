import string
from functools import reduce

import azapyGUI.configMSG as configMSG


def _validate_nothing(param):
    return True, param


def _validate_hlength(param):
    msg = configMSG._validate_hlength_msg
    field = 'hlength'
    try:
        vv = float(param[field])
    except:
        return False, msg
            
    if vv >= 0.5: 
        param[field] = vv
        return True, vv
    return False, msg


def _validate_mu0(param):
    msg = configMSG._validate_mu0_msg
    field = 'mu0'
    try:
        vv = float(param[field])
    except:
        return False, msg
            
    if vv >= 0: 
        param[field] = vv
        return True, vv
    return False, msg


def _validate_mu(param):
    msg = configMSG._validate_mu_msg
    field = 'mu'
    try:
        vv = float(param[field])
    except:
        return False, msg
            
    if vv >= 0: 
        param[field] = vv
        return True, vv
    return False, msg


def _validate_aversion(param):
    msg = configMSG._validate_aversion_msg
    field = 'aversion'
    try:
        vv = float(param[field])
    except:
        return False, msg
            
    if vv > 0: 
        param[field] = vv
        return True, vv
    return False, msg
   
    
def _validate_ww0(param, ns):
    msg = configMSG._validate_ww0_msg
    field = 'ww0'
    try:
        ww0 = [float(x) for x in param[field].strip(string.whitespace + '[]{}()').split(",")]
    except:
        return False, msg
    
    if len(ww0) < ns:
        ww0 += [1.] * (ns - len(ww0))
    ww0 = ww0[:ns]
    if all([(x >= 0) for x in ww0]) & (sum(ww0) > 0):
        param[field] = ww0
        return True, ww0
    return False, msg


def _validate_diver(param):
    msg = configMSG._validate_diver_msg
    field = 'diver'
    try:
        vv = float(param[field])
    except:
        return False, msg
            
    if vv > 0: 
        param[field] = vv
        return True, vv
    return False, msg


def _validate_alpha_mCVaR(param):
    msg = configMSG._validate_alpha_mCVaR_msg
    field = 'alpha'
    try:
        alpha = [float(x) for x in param[field].strip(string.whitespace + '[]{}()').split(",")]
    except:
        return False, msg
    
    if all([(0.99 >= x) & (x >= 0.5) for x in alpha]):
        param[field] = alpha
        return True, alpha
    return False, msg


def _validate_alpha_mSMCR(param):
    msg = configMSG._validate_alpha_mSMCR_msg
    field = 'alpha'
    try:
        alpha = [float(x) for x in param[field].strip(string.whitespace + '[]{}()').split(",")]
    except:
        return False, msg
    
    if all([(0.99 >= x) & (x >= 0.5) for x in alpha]):
        param[field] = alpha
        return True, alpha
    return False, msg


def _validate_alpha_mEVaR(param):
    msg = configMSG._validate_alpha_mEVaR_msg
    field = 'alpha'
    try:
        alpha = [float(x) for x in param[field].strip(string.whitespace + '[]{}()').split(",")]
    except:
        return False, msg
    
    if all([(0.99 >= x) & (x >= 0.5) for x in alpha]):
        param[field] = alpha
        return True, alpha
    return False, msg


def _validate_alpha_mBTAD(param):
    msg = configMSG._validate_alpha_mBTAD_msg
    field = 'alpha'
    try:
        alpha = [float(x) for x in param[field].strip(string.whitespace + '[]{}()').split(",")]
        param[field] = alpha
        return True, alpha
    except:
        return False, msg

    
def _validate_alpha_mBTSD(param):
    msg = configMSG._validate_alpha_mBTSD_msg
    field = 'alpha'
    try:
        alpha = [float(x) for x in param[field].strip(string.whitespace + '[]{}()').split(",")]
        param[field] = alpha
        return True, alpha
    except:
        return False, msg
    
    
def _validate_coef(param):
    msg = configMSG._validate_coef_msg
    field = 'coef'
    try:
        coef = [float(x) for x in param[field].strip(string.whitespace + '[]{}()').split(",")]
    except:
        return False, msg
    
    if all([(x > 0) for x in coef]):
        coef += [1.0] * (len(param['alpha']) - len(coef))
        param[field] = coef[:len(param['alpha'])]
        return True, coef
    return False, msg


def _validate_coef_mMAD(param):
    msg = configMSG._validate_coef_mMAD_msg
    field = 'coef'
    try:
        coef = [float(x) for x in param[field].strip(string.whitespace + '[]{}()').split(",")]
    except:
        return False, msg
    
    if bool(reduce(lambda a, b: (b > 0) and (a >= b) and a or False, coef)):
        param[field] = coef
        return True, coef
    return False, msg


def _validate_coef_mLSD(param):
    msg = configMSG._validate_coef_mLSD_msg
    field = 'coef'
    try:
        coef = [float(x) for x in param[field].strip(string.whitespace + '[]{}()').split(",")]
    except:
        return False, msg
    
    if bool(reduce(lambda a, b: (b > 0) and (a >= b) and a or False, coef)):
        param[field] = coef
        return True, coef
    return False, msg


def _validate_fw(param):
    msg = configMSG._validate_fw_msg
    field = 'fw'
    try:
        fw = [float(x) for x in param[field].strip(string.whitespace + '[]{}()').split(",")]
    except:
        return False, msg

    if all([(x >= 0) for x in fw]) & (len(fw) == 4):
        param[field] = fw
        return True, fw
    return False, msg
    

def _validate_nw(param, ns=1000):
    msg = configMSG._validate_nw_msg
    field = 'nw'
    try:
        vv = int(param[field])
    except:
        return False, msg
            
    if (vv > 0) & (vv <= ns): 
        param[field] = vv
        return True, vv
    return False, msg


def _validate_threshold(param, ns=1000):
    msg = configMSG._validate_threshold_msg
    field = 'threshold'
    try:
        vv = int(param[field])
    except:
        return False, msg
    
    if (vv >= param['nw']) & (vv <= ns): 
        param[field] = vv
        return True, vv
    return False, msg


def _validate_corr_threshold(param):
    msg = configMSG._validate_corr_threshold_msg
    field = 'corr_threshold'
    try:
        vv = float(param[field])
    except:
        return False, msg
    
    if (vv >= 0) & (vv < 1): 
        param[field] = vv
        return True, vv
    return False, msg


def _validate_dirichlet_alpha(param, ns):
    msg = configMSG._validate_dirichlet_alpha_msg
    field = 'dirichlet_alpha'
    if isinstance(param[field], str):
        try:         
            da = [float(x) for x in param[field].strip(string.whitespace + '[]{}()').split(",")]
        except:
            return False, msg
    else:
        da = param[field]
    
    if len(da) < ns:
        da += [1.] * (ns - len(da))
    da = da[:ns]
    if all([(x > 0) for x in da]):
        param[field] = da
        return True, da
    return False, msg


def _validate_variance_reduction(param):
    field = 'variance_reduction'
    param[field] = int(param[field])
    return True, param[field]
    

def _validate_nr_batches(param):
    msg = configMSG._validate_nr_batches_msg
    field = 'nr_batches'
    try:
        mcb = int(param[field])
        if mcb > 0:
            param[field] = mcb
            return True, mcb
        else:
            return False, msg
    except:
        return False, msg
    
    
def _validate_mc_paths(param):
    msg = configMSG._validate_mc_paths_msg
    field = 'mc_paths'
    try:
        mcp = int(param[field])
        if mcp > 0:
            param[field] = mcp
            return True, mcp
        else:
            return False, msg
    except:
        return False, msg


def _validate_mc_seed(param):
    msg = configMSG._validate_mc_seed_msg
    field = 'mc_seed'
    try:
        mc_seed = int(param[field].strip(string.whitespace))
        param[field] = mc_seed
        return True, mc_seed
    except:
        return False, msg
    

def _validate_symbols(symbols):
    sout = []
    if len(symbols) < 1: return True, sout
    allowed_char = set(string.ascii_uppercase + string.digits + '.^-')
    for symb in symbols:
        symb = symb.strip(string.whitespace).upper()
        if (len(symb) > 0) & (set(symb) < allowed_char):
            sout.append(symb)
    return len(symbols) == len(sout), sout       


def _validate_portfolio_name(name):
    name = name.strip(string.whitespace)
    allowed_char = set(string.ascii_letters + string.digits + "._-")
    if (len(name) != 0) & (set(name) < allowed_char):
        return True, name
    return False, configMSG._validate_portfolio_name_msg


def _validFloat(inp, acttyp, val):      
    # '%S','%d','%P'
    if acttyp != '1': return True
    if (inp.isdigit() and ((len(val) == 1) or (val[0] != '0') or ('.' in val))): return True
    elif (inp == '.') and (val.count('.') <= 1): return True
    elif (inp == '-') and (val.count('-') <= 1) and (val[0] == '-'): return True
    return False


def _validIntPositive(inp, acttyp, val):
    # '%S','%d','%P'
    if acttyp != '1': return True
    if (inp.isdigit() and ((len(val) == 1) or (val[0] != '0'))): return True
    return False


def _validInt(inp, acttyp, val):
    # '%S','%d','%P
    if acttyp != '1': return True
    match len(val):
        case 1: 
            return inp.isdigit() or (inp == '-')
        case 2: 
            match val[0]:
                case '-': return inp in list('123456789')
                case '0': return False
                case _: return inp.isdigit()
        case _: return (val[0] != '0') and inp.isdigit()


def _validIntNegative(inp, acttyp, val):
    # '%S','%d','%P'
    if acttyp != '1': return True
    match len(val):
        case 1: return (inp in list('0-'))
        case 2: return (val[0] == '-') and (inp in list('123456789'))
        case 3: return (val[0] == '-') and inp.isdigit()


def _validDateMMDDYYYY(inp, acttype, val):
    # '%S','%d','%P'
    if acttype != '1': return True
    match len(val):
        case 1: 
            return inp in list('0123456789tn')
        case 2:
            match val[0]:
                case '0': return inp in list('123456789')
                case '1': return inp in list('012/.-')
                case 't': return inp == 'o'
                case 'n': return inp == 'o'
                case _: return inp in '/.-'
        case 3:
            return ((val[1].isdigit() and (inp in list('/.-'))) or 
                    ((val[0] == 't') and (inp == 'd')) or
                    ((val[0] == 'n') and(inp == 'w')) or
                    ((not val[1].isdigit()) and (inp.isdigit())))        
        case 4:
            return (((val[2] in list('/.-')) and inp.isdigit()) or
                    ((val[2] == '0') and (inp in list('123456789'))) or
                    ((val[2] in list('12')) and (inp in list('0123456789/.-'))) or
                    ((val[2] == '3') and (inp == '0') and (val[0] != '2')) or
                    ((val[2] == '3') and (inp == '1') and (val[0] in list('13578'))) or
                    ((val[2] in list('3456789')) and (inp in list('/.-'))) or
                    ((val[2] == 'd') and (inp == 'a')))
        case 5:
            return (((val[3] == '0') and (inp in list('123456789'))) or
                    ((val[3] in list('12')) and (inp in list('0123456789/.-'))) or
                    ((val[3] == '3') and (inp == '0') and (int(val[:2]) != 2)) or
                    ((val[3] == '3') and (inp == '1') and (int(val[:2]) in [1, 3, 5, 7, 8, 10, 12])) or
                    ((val[3] in list('3456789')) and (inp in list('/.-'))) or
                    ((val[3] in list('/.-')) and (inp == '2')) or
                    ((val[3] == 'a') and (inp == 'y')))
        case 6:
            return ((val[4].isdigit() and (inp in list('/.-'))) or
                    ((val[4] in list('/.-')) and (inp == '2')) or
                    ((val[4] == '2') and (inp == '0')))
        case 7:
            return (((val[5] in list('/.-')) and (inp == '2')) or
                    ((val[5] == '2') and (inp == '0')) or
                    ((val[5] == '0') and inp.isdigit()))
        case 8:
            return (((val[5] in list('/.-')) and (inp == '0')) or
                    ((val[4] in list('/._')) and inp.isdigit()) or
                    ((val[3] in list('/._')) and inp.isdigit()))
        case 9:
            return (((val[5] in list('/.-')) and inp.isdigit()) or
                    ((val[4] in list('/.-')) and inp.isdigit()) and
                     (((inp != '0') and (int(val[7:]) % 4 == 0)) or (val[0] != '2') or (int(val[2:4]) != 29)))
        case 10:
            return ((val[5] in list('/.-')) and inp.isdigit() and 
                    (((inp != '0') and (int(val[8:]) % 4 == 0)) or (int(val[:2]) != 2) or (int(val[3:5]) != 29)))
        case _: return False
                    
   
def _list2string(lnames, bk=10):
    return '\n'.join([', '.join(lnames[k : (k + bk)]) for k in range(0, len(lnames), bk)])
