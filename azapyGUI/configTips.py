_rtype_param_tip = "Optimization type for risk-based strategies."

_mu_param_tip = "Targeted portfolio expected rate of return."

_mu0_param_tip = "Risk-free rate accessible to the investor."

_aversion_param_tip = "The value of the risk-aversion coefficient."

_ww0_param_tip = \
"Targeted portfolio weights. List of int>=0.\n\
Size = number of port components. Otherwise padded with 1 or right truncated."

_diver_param_tip = "Targeted portfolio diversification factor."

_freq_param_tip = "Rate of return horizon: Q - quarterly, M - monthly."

_method_lin_param_tip = "Liner Programming numerical library."

_method_socp_param_tip = "Second Order Cone Programming numerical library."

_method_exp_param_tip = \
"Exponential Cone Programming numerical library.\n\
excp is using ecos, while ncp and ncp2 are using cvxopt numerical libraries."

_method_quad_param_tip = "Quadratic Programming numerical library."

_hlength_val_param_tip = \
"History length in number of years used for calibration\n\
(rounded to months), float >= 0.5."

_col_calibration_param_tip = \
"Name of the price column from market data used in the weight’s calibration."

_ftype_param_tip = "Filter name."

_fw_param_tip = "Filter weights: list of 4 int >=0."

_nw_param_tip = "Maximum number of selected symbols: int >=1."

_threshold_param_tip = \
"Minimum number of symbols with positive momentum\n\
for a full capital allocation: int >=nw."

_Dual_Momentum_model_tip = "Dual Momentum filter."

_corr_threshold_param_tip = "Cluster correlation threshold': float [-1,1]."

_Correlation_Clustering_model_tip = "Correlation Clustering filter."

_alpha_mCVaR_param_tip = \
"List of distinct confidence levels, float in (0.5, 1)."

_coef_param_tip = \
"Mixture weights, list of float >0, same size as alpha,\n\
otherwise padded with 1 or right truncated."

_mCVaR_model_tip = "Mixture Conditional Value at Risk measure."

_alpha_mSMCR_param_tip = \
"List of distinct confidence levels, float in (0.5, 1)."

_mSMCR_model_tip = "Mixture Second Moment Coherent Risk measure."

_alpha_mEVaR_param_tip = \
"List of distinct confidence levels, float in (0.5, 1)."

_mEVaR_model_tip = "Mixture Entropic Value at Risk measure."

_coef_mMAD_param_tip = \
"Mixture weights.\n\
Positive non-increasing list of mixture coefficients, float in (0, 1]."

_mMAD_model_tip = "m-level Mean Absolute Deviation risk measure."

_mLSD_model_tip = "m-level Lower Semi-Deviation risk measure."

_alpha_mBTAD_param_tip = \
"List of distinct rates threshold levels, float in (-1, 1)."

_coef_BTAD_param_tip = \
"Mixture weights, list of float >0, same size as alpha,\n\
otherwise padded with 1 or right truncated."

_detrended_param_tip = "True - rates of return are detrended (mean=0)."

_mBTAD_model_tip = "Mixture Below Threshold Absolute Deviation measure."

_mBTSD_model_tip = "Mixture Below Target Semi-Deviation measure."

_GINI_model_tip = "Gini risk measure."

_SD_model_tip = "Standard Deviation risk measure."

_MV_model_tip = "Mean Variance measure."

_Equal_Weighted_model_tip = "Equal weighted portfolio."

_Inverse_Volatility_model_tip = "Inverse Volatility model."

_Inverse_Variance_model_tip = "Inverse Variance model."

_Inverse_Drawdown_model_tip = "Inverse Maximum Drawdown model."

_rtype_Kelly_param_tip = \
"Optimization method:\n\
ExpCone - exponential cone programming,\n\
Full - non-linear solver,\n\
Order2 - quadratic programming for second order Taylor approx."

_Kelly_model_tip = "Kelly's portfolio strategy."

_dirichlet_alpha_param_tip = \
"List of Dirichlet alpha coefficients (for Monte-Carlo simulations)\n\
Size = number of port components. Otherwise padded with 1 or right truncated."

_variance_reduction_param_tip = \
"A value of 1 triggers the Monte Carlo variance reduction procedure."

_mc_seed_param_tip = \
"Random number generator seed."

_nr_batches_param_tip = \
"Number of Monte Carlo batches."

_mc_paths_param_tip = \
"Number of Monte Carlo simulations per batch per variance reduction mode."

_univ_hlength_val_param_tip = \
"History length in number of years. The larger the better. \
A typical value is 12."

_Universal_model_tip = \
"Universal Portfolio strategy. \
Any additional selector model will be ignored.",

_settings_UserPortfolioDirectory_tip = \
"Default folder to save portfolio collection."

_settings_UserMktDataDirectory_tip = \
"Working directory for temporary market data"

_settings_UserOutputDirectory_tip = \
"Default folder for user reports etc."

_settings_MkTDataProvider_tip = \
"Name of historical market data provider."

_settings_porviderKey_tip = \
"Market data provider access key \
(if is not already set as an environment variable)."

_settings_max_req_per_min_tip = \
"Maximum number of requests per minute (as specified by the provider)."

_settings_ShowTips_tip = \
"Set visibility for widget tips."

_settings_edate_default_tip = \
"Default end data for market data (e.g. today or 1/1/2024 etc.)."

_settings_sdate_default_tip = \
"Default starting date for market data (e.g. 1/1/2012)."

_settings_noffset_default_tip = \
"Default rebalancing date as offset days relative to investment period \
end (e.g. -3)."

_settings_fixoffset_default_tip = \
"Default fixing date as offset days relative to rebalancing date (e.g. -1)."

_settings_capital_default_tip = \
"Default initial (cash) Capital value."

_settings_nsh_round_default_tip = \
"Default setting for the quantity of shares as a whole number."

_settings_force_default_tip = \
"Default value for the force flag in market data retrieving procedure."

_settings_OpenExcel_tip = \
"Auto open Excel when an xlsx file is saved."

_epw_portfolio_name_tip = \
"Short, unique, name to identify the portfolio."

_bkt_edate_tip = \
"Backtesting end date (e.g. today)."

_bkt_sdate_tip = \
"Backtesting start date (e.g. 1/1/2012)."

_bkt_noffset_tip = \
"Rebalancing date, as number of business days offset relative to the end \
of investment period (end of month or quarter). A typical value is -3."

_bkt_fixoffset_tip = \
"Fixing date, as number of business days offset relative to the rebalancing \
date (always a <=0). A typical value is -1."

_bkt_capital_tip = \
"Initial capital (cash value), e.g. 100000."

_bkt_nsh_round_tip = \
"Check to set the number of shares as whole numbers."

_bkt_provider_tip = \
"Market data provider."

_bkt_force_tip = \
"Check to force a fresh reading of market data from the Provider \
(ignoring the local buffer) - potentially slowing the application."

_reb_as_of_tip = \
"Reference date - the weights will be computed using the latest closing \
relative to this day."

_reb_cash_tip = \
"Additional cash to be added at the rebalancing (a negative value is a \
reduction of the reinvested total capital)."
                                                                
_reb_nsh_round_tip = _bkt_nsh_round_tip

_reb_provider_tip = _bkt_provider_tip

_reb_force_tip = _bkt_force_tip

_sew_symb_tip = \
"Comma delimited list of symbols"

_sew_edate_tip = \
"Market data end date (e.g. today or 1/1/2024 etc.)."

_sew_sdate_tip = \
"Market data start date (e.g. 1/1/2012, or empty to get the most recent hist. data only)."

_sew_provider_tip = \
"Market data provider."

_sew_force_tip = \
"Check to force market data reding from provider (slower)."

_exchange_calendar_tip = \
"Exchange business calendar."

_imputation_method_tip = \
"Method to imputing missing data."
