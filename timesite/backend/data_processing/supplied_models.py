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
        #calc MSE for AR(1)
        mse_ar=0
        for i in residuals:
            mse_ar+=(i**2)
        mse_ar/=df.shape[0]
        rmse_ar=np.sqrt(mse_ar)
        
        
        # Fit GARCH to the residuals from AR(1) process (instead of daily log rate)
        garch_model = arch_model(residuals, vol='GARCH', p=p, q=q, dist=dist)
        garch_fit = garch_model.fit(disp='off')
        garch_params = {
            'omega': garch_fit.params['omega'],
            'alpha': garch_fit.params['alpha[1]'],
            'beta': garch_fit.params['beta[1]'],
        }

        #calc MSE for GARCH
        mse_garch=0
        for i in garch_fit.resid:
            mse_garch+=(i**2)
        mse_garch/=df.shape[0]
        rmse_garch=np.sqrt(mse_garch)
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
        return [models_params,ar_model,garch_fit,mse_ar,rmse_ar,mse_garch,rmse_garch]

def simulate_paths(df, modelsparams, n_simulations, n_steps, dt=250, calc_correlation_matrix=False):
    import time
    start_time = time.time()

    tenors = list(modelsparams.keys())
    n_tenors = len(tenors)

    paths = {tenor: np.zeros((n_simulations, n_steps)) for tenor in tenors}
    vol = {tenor: np.zeros((n_simulations, n_steps)) for tenor in tenors}

    # correlation matrices
    if calc_correlation_matrix:
        pass
    else:
        #corr_matrix = np.array([[1.0]])
        #L = np.array([[1.0]])
        corr_matrix=np.ones((len(tenors),len(tenors)))
        L=np.ones((len(tenors),len(tenors)))

    for tenor in tenors:
        paths[tenor][:, 0] = df[tenor].iloc[-1]
        print(type(modelsparams[tenor]['ar']['resid_variance']))
        vol[tenor][:, 0] = modelsparams[tenor]['ar']['resid_variance'] # starting variance from AR(1)

    for t in range(1, n_steps):
        Z = np.random.normal(0, 1, (n_simulations, n_tenors))
        Z = Z @ L.T

        check_epsilon_t=0
        for tenor_idx, tenor in enumerate(tenors):
            # Initialize models' params
            ar_params = modelsparams[tenor]['ar']
            garch_params = modelsparams[tenor]['garch']
            jd_params = modelsparams[tenor]['jd']

            # AR params
            const = ar_params['const']
            phi = ar_params['phi']

            # GARCH params
            omega = garch_params['omega']
            alpha = garch_params['alpha']
            beta = garch_params['beta']

            # JMP params
            lambda_ = jd_params['lambda']
            jd_mean = jd_params['jd_mean']
            jd_std = jd_params['jd_std']

            if t == 1:
                epsilon_prev = paths[tenor][:, t-1] - const - phi*paths[tenor][:, t-1]
            else:
                epsilon_prev = paths[tenor][:, t-1] - const - phi*paths[tenor][:, t-2]

            # brownian term
            z_t = Z[:, tenor_idx]

            # dr_CV
            vol[tenor][:, t] = np.sqrt(omega + alpha*epsilon_prev**2 + beta*vol[tenor][:, t-1]**2)
            epsilon_t = vol[tenor][:, t]*z_t*np.sqrt(paths[tenor][:, t])

            # dr_JMP
            jumps = np.random.binomial(1, lambda_*dt, n_simulations)
            jump_sizes = np.random.normal(jd_mean, jd_std, n_simulations)

            check_epsilon_t += jumps*jump_sizes
            check_rate_t = const + phi*paths[tenor][:, t-1] + check_epsilon_t

            if t == 1:
                check_rate_t_prev = const + phi*paths[tenor][:, t-1] + check_epsilon_t
            else:
                check_rate_t_prev = const + phi*paths[tenor][:, t-2] + check_epsilon_t
            #print(check_rate_t)
            # dr_JMP, ensure non-negative values
            if check_rate_t.all() < 0:
                epsilon_t += max(jumps*jump_sizes, -check_rate_t_prev)
            else:
                epsilon_t += jumps*jump_sizes

            #dr_MR (in discrete AR-form)
            paths[tenor][:, t] = const + phi*paths[tenor][:, t-1] + epsilon_t

    elapsed_time = time.time() - start_time
    elapsed_time = float(f'{elapsed_time:.6f}')
    print(f'Simulated paths for dataset. Execution time: {round(elapsed_time, 2)} seconds.')
    return paths