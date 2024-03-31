
_validate_portfolio_name_msg = \
"Invalid portfolio name.\nPortfolio names must contain only letters, \
digits, ., _, and - characters."

_validate_portfolio_name_exist_msg = \
"Portfolio name already in use. Please choose another name."

_validate_symbols_nr_msg = \
"Not enough portfolio components were selected. It must be >1."

_validate_symbols_name_msg = \
"Wrong entries among symbols.\nA valid symbol name contains only uppercase \
letters, digits, '.', and '^' characters."

_validate_symbols_final_msg = \
"The following symbols were dropped. \
No market data available from the provider."

_validate_portfolio_optimizer_msg = \
"No optimizer was set. Please select one."

_validate_hlength_msg = \
"hlength - history length (length of historical data) \
used in the optimization procedure). It is measured in years. A fractional \
number will be rounded to an integer number of months. hlength must be a \
positive integer >= 0.5. A typical value is around 1 \
(to be statistically significant) and usually not \
greater than 3 (beyond which the historical data may not be relevant for \
a model calibration)."
    
_validate_mu0_msg = \
"mu0 - risk-free rate accessible to the investor, i.e. \
the fixed rate of return (zero risk) for an investment that can be made \
at any time. Therefore, holding risker assets is justified only if the \
expected rate of return is higher than this threshold (of certainty). \
It is required in the evaluation of Sharpe type of ratios. It must be >=0.\
Most of the time a value of 0 is realistic."

_validate_mu_msg = \
"mu - targeted portfolio expected rate of return. It must be >=0. \
It is effective if its value is between max(0, muk_min) and muk_max, where \
muk_min and muk_max is the minimum and maximum expected rate of returns of \
individual portfolio components. If mu is >muk_max then the optimization \
procedure will return the single asset portfolio containing the best \
performant component of the portfolio."

_validate_aversion_msg = \
"aversion - risk-aversion coefficient lambda. It must be >0. \
A value of 0 will define the single asset portfolio containing the best \
performant component of the portfolio. On the other hand, a value \
approaching infinity will define minimum risk portfolio (same  as \
rtype=MinRisk)."
    
_validate_ww0_msg = \
"ww0 - targeted portfolio weights. They must be >=0 with at least \
one >0. The number of weights should match the number of portfolio \
components (in alphabetical order of the components symbol name). If the \
size of ww0 is smaller than the number of portfolio components, the \
missing weights will be set to 1, and if greater, then ww0 will be \
truncated. ww0 are relative weights (the normalization will be done \
internally). Therefore, a single value of 1 will designate an equal \
weighted portfolio."

_validate_diver_msg = \
"diver - targeted diversification factor. It must be in (0, 1). \
A value of 0 implies no diversification at all - the portfolio risk is \
equal to the sum of the portfolio component risks. A value of 1  implies \
an ideal diversification where the portfolio risk is 0. Any  given \
portfolio has less than 1 maximum diversification factor. If diver is set \
higher than this maximum value, the optimization returns the  portfolio \
with maximum diversification (same a rtype=MaxDiverse)."

_validate_alpha_mCVaR_msg = \
"alpha - list of distinct confidence levels (percentiles). All \
components must be between (0.5, 0.99]. A typical value is between 0.975 \
and 0.85. Higher values may not be statistically relevant and lower values \
may not be impactful. The recommended size of alpha is between 1 and 3. \
More confidence levels may not refine the computation but will add to the \
computation time. A typical choice may be [0.95, 0.90]."

_validate_alpha_mSMCR_msg = \
"alpha - list of distinct confidence levels (percentiles). All \
components must be between (0.5, 0.99]. A typical value is between 0.85 \
and 0.65. Higher values may not be statistically relevant and lower values \
may not be impactful. The recommended size of alpha is between 1 and 3. \
More confidence levels may not refine the computation but will add to the \
computation time. A typical choice may be [0.85, 0.75]."

_validate_alpha_mEVaR_msg = \
"alpha - list of distinct confidence levels (percentiles). All \
components must be between (0.5, 0.99]. A typical value is between 0.80 \
and 0.60. Higher values may not be statistically relevant and lower values \
may not be impactful. The recommended size of alpha is between 1 and 3. \
More confidence levels may not refine the computation but will add to the \
computation time. A typical choice may be [0.75, 0.65]."

_validate_alpha_mBTAD_msg = \
"alpha - list of distinct rate thresholds. Although theoretically \
they may take any values, from a practical point of view, they must be in \
the range of asset return rate values. Moreover, if detrended rates are \
considered (detrended=True), then the threshold must be in range of \
absolute deviation of the asset return rate values. \
A typical value could be [-0.01, 0.0, 0.01]."

_validate_alpha_mBTSD_msg = \
"alpha - list of distinct rate thresholds. Although theoretically \
they may take any values, from a practical point of view, they must be in \
the range of asset return rate values. Moreover, if detrended rates are \
considered (detrended=True), then the threshold must be in range of \
standard deviation of the asset return rate values. \
A typical value could be [-0.01, 0.0, 0.01]."

_validate_coef_msg = \
"coef - list of weights coefficients for risk measures mixture. \
All coefficients, one for each alpha, must be >0. If the size of coef is \
smaller than the size of alpha, the missing values will be set to 1, and \
if greater, then coef will be truncated. coef are relative weights \
(the normalization will be done internally). Therefore, a single value \
of 1 will designate an equal weighted risk measures mixture."

_validate_coef_mMAD_msg = \
"coef - list of non-increasing values of MAD levels weights \
coefficients. All coefficients must be >0. All weights are relative \
(the normalization will be done internally). \
A typical value could be [1, 1, 1]."

_validate_coef_mLSD_msg = \
"coef - list of non-increasing values of MAD levels weights \
coefficients. All coefficients must be >0. All weights are relative \
(the normalization will be done internally). \
A typical value could be [1, 1, 1]."

_validate_fw_msg = \
"fw - Weights for f13612w filter. It is a list of 4 \
coefficient >=0 with at least one >0. All weights are relative \
(the normalization will be done internally). \
Typical value is [1, 1, 1, 1]." 

_validate_nw_msg = \
"nw - Maximum number of selected symbols. It is an integer >=1 \
and <= number of portfolio components. A typical value is between 3 and 5."

_validate_threshold_msg = \
"threshold - Minimum number of symbols with positive momentum for a full \
capital allocation. It is an integer >=nw (maximum number of selected symbols) \
and <= number of portfolio components. A typical value is between 8 and 10."

_validate_corr_threshold_msg = \
"corr_threshold - cluster correlation threshold (i.e., a cluster contains only \
symbols with inter-correlation higher than corr_threshold). It must be >=0 \
and <1. A typical value could be 0.98."

_validate_dirichlet_alpha_msg = \
"List of Dirichlet alpha coefficients (to be used by the Dirichlet random \
number generator). All coefficients must be >0. The number of \
coefficients must be equal to the number of symbols in the portfolio. \
A list with smaller number will be pad with 1, while a larger list will \
be truncated. For example, a single value of 1 will aet a symmetric Dirichlet \
distribution (equivalent to a uniform distribution over the open \
standard (ns-1)-simplex, where ns is the \
number of portfolio components). A typical value is 1."

_validate_nr_batches_msg = \
"Number of Monte Carlo batches must be >0. The Monte Carlo simulation is \
parallelized in batches. Each batches holds mc_paths number of simulations. \
nr_baches isa small integer >0 (e.g. a multiple of number of CPU cores). \
The default value is 16."

_validate_mc_paths_msg = \
"Number of Monte Carlo simulations per batch per variance reduction mode \
must be an integer >0. The total number of simulations is given by \
n! x mc_batches x mc_paths where the first term is present only if the \
variance reduction procedure is triggered. Here n is the number of portfolio \
components and n! its factorial. For example, if n=7, nr_paths=16 and \
mc_paths=100, the total number of MC simulations is 8,064,000."

_validate_mc_seed_msg = \
"mc_seed (Monte Carlo engine seed) must be an integer."
    
_validate_application_settings_msg = \
"At least one market data provider must be chosen. Note: yahoo is free."

_validate_provider_key_msg = \
"No provider key was set explicitly or as environment variable."

_validate_noffset_msg = \
"Wrong value for Bday offset. Must be an integer (e.g. -3)."

_validate_fixoffset_msg = \
"Wrong value for Fixing offset. Must be an integer <=0."

_validate_capital_msg = \
"Wrong value for initial capital. Must be a real number >=10000."
