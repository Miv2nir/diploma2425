from statsmodels.tsa.ar_model import AutoReg
import numpy as np
import pandas as pd
from arch import arch_model

def calibrate_models(df, tenor, p=1, q=1, dist='Normal', jump_threshold=3):
        #rate_series = df[tenor]['rate'].dropna()
        rate_series=df[tenor].dropna()
        # AR(1) as a discrete approx. of the OU process for mean reversion
        ar_model = AutoReg(rate_series, lags=1, trend='c').fit()
        ar_params = {
            'const': ar_model.params[0],
            'phi': ar_model.params[1],
            'resid_variance': np.sqrt(ar_model.sigma2)
        }
        residuals = ar_model.resid

        # Fit GARCH to the residuals from AR(1) process (instead of daily log rate)
        garch_model = arch_model(residuals, vol='GARCH', p=p, q=q, dist=dist)
        garch_fit = garch_model.fit(disp='off')
        garch_params = {
            'omega': garch_fit.params['omega'],
            'alpha': garch_fit.params['alpha[1]'],
            'beta': garch_fit.params['beta[1]'],
        }

        # Standardize residuals using GARCH volatility
        vol = garch_fit.conditional_volatility
        standardized_residuals = residuals / vol

        # Identify jumps from standardized residuals
        jumps = standardized_residuals[np.abs(standardized_residuals) > jump_threshold]
        jump_count = len(jumps)
        total_steps = len(standardized_residuals)
        lambda_ = jump_count / total_steps # daily jump probability
        jd_mean = jumps.mean()
        jd_std = jumps.std()
        
        jd_params = {
            'lambda': lambda_,
            'jd_mean': jd_mean,
            'jd_std': jd_std
        }

        models_params = {
            'ar': ar_params,
            'garch': garch_params,
            'jd': jd_params
        }
        return [models_params,ar_model,garch_fit]