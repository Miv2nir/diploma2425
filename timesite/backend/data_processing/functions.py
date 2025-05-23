import pandas as pd
import backend.models as models
from timesite.settings import MEDIA_ROOT

from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from django.template.loader import render_to_string
from arch import arch_model
from arch.univariate.base import ARCHModelResult

from statsmodels.tsa.stattools import acf, pacf
import plotly.graph_objects as go

import plotly.express as px
import os
from backend.data_processing.supplied_models import *
'''
self.initial - declares whether the function is the leading function in a pipeline
self.type - self-referential property declaring its subclass. To be replaced with smth better most likely.
self.accepts - keywords to hint what can be fed into the function from other functions
self.returns - keywords to hint what object does it return.
'''
class LoadCSV:
    def __init__(self):
        self.initial=True
        self.display_name='Load CSV'
        self.description='Loads a CSV file from the Datastore'
        self.type='loader'
        
        self.accepts=[] #from models.DataFile
        self.returns=['df']
    def execute(self,data_obj:models.DataFile):
        return pd.read_csv(data_obj.file.path)

class DropColumns:
    def __init__(self):
        self.initial=False
        self.display_name='Drop Columns'
        self.description='Drops columns from a dataframe by their names'
        self.type='processor'
        
        self.accepts=['df']
        self.returns=['df']
    def execute(self,df:pd.DataFrame,params={}):
        columns=params['text_params']
        columns_list=columns.split(',')
        return df.drop(columns=columns_list)

class FillNA:
    def __init__(self):
        self.initial=False
        self.display_name='Fill NaN'
        self.description='Fills all of the NaN values in accordance to a specified method'
        
        self.type='processor'
        self.accepts=['df']
        self.returns=['df']
    def execute(self,df:pd.DataFrame,params={}):
        #expected values
        #medhot: value fill, ffill, bfill, average fill
        if params['fill_mode']=='average':
            #average fill - calculate averages in columns and fill them out (main method used)
            for i in df.columns:
                mean_value=df[i].mean()
                df[i].fillna(value=mean_value,inplace=True)
        elif params['fill_mode']=='ffill':
            #forward fill - propagate last values to next valid
            df.ffill(inplace=True)
        elif params['fill_mode']=='bfill':
            #backward fill - propagate next valid values backwards until the last valid
            df.bfill(inplace=True)
        elif params['fill_mode']=='value':
            #value fill will replace all nans with a specific value
            value_number=params['value']
            df.fillna(value=value_number,inplace=True)
        return df

class DropNA:
    def __init__(self):
        self.initial=False
        self.display_name='Drop NaN'
        self.description='Drops rows containing NaN values'
        
        self.type='processor'
        self.accepts=['df']
        self.returns=['df']
    def execute(self,df:pd.DataFrame,params={}):
        df.dropna(axis=0,inplace=True)
        return df
class GetQuantile:
    def __init__(self):
        self.initial=False
        self.display_name='Quantile'
        self.description='Calculates quantile of a dataset'
        self.type='processor'
        self.accepts=['df']
        self.returns=['df']
    def execute(self,df:pd.DataFrame,params={}):
        quantile=float(params['quantile'])
        numeric_only=params['numeric_only']
        #method=params['method']
        return df.quantile(quantile,numeric_only=numeric_only).to_frame()
class SplitByIndex:
    def __init__(self):
        self.initial=False
        self.display_name='Split By Index'
        self.description='Removes values from a Dataframe by index.'
        self.type='processor'
        self.accepts=['df']
        self.returns=['df']
    def execute(self,df:pd.DataFrame,params={}):
        split_point=int(params['split_point'])
        splitting_mode=params['splitting_mode']
        if splitting_mode=='left':
            df = df.iloc[:split_point,:]
        elif splitting_mode=='right':
            df = df.iloc[split_point:,:]
        return df
class MergeDF:
    def __init__(self):
        self.initial=False
        self.display_name='Merge Dataframes'
        self.description='Merge two Dataframes into one based on the coming order of the items within.'
        self.type='processor'
        self.accepts=['df']
        self.returns=['df']
    def execute(self,df1:pd.DataFrame,df2:pd.DataFrame,params={}):
        '''
        how=params['how']
        left_index=False
        try:
            if params['left_index']=='on':
                left_index=True
        except KeyError:
            pass
        right_index=False
        try:
            if params['right_index']=='on':
                right_index=True
        except KeyError:
            pass
        '''
        df1.reset_index(inplace=True)
        df2.reset_index(inplace=True)
        print(df1)
        df_new=df1.merge(df2,left_index=True,right_index=True)
        return df_new
        
class SetDateIndex:
    def __init__(self):
        self.initial=False
        self.display_name='Set Date as Index'
        self.description='Converts a selected column into datetime and then assigns it as the index column of the DataFrame.'
        self.type='processor'
        self.accepts=['df']
        self.returns=['df']
    def execute(self,df:pd.DataFrame,params={}):
        chosen_column=params['chosen_column']
        #method=params['method']
        df[chosen_column]=pd.to_datetime(df[chosen_column])
        return df.set_index(chosen_column)

class RenderDF:
    def __init__(self):
        self.initial=False
        self.display_name='Render Dataframe'
        self.description='Invokes .to_html() of a dataframe object.'
        self.type='renderer'
        
        self.accepts=['df']
        self.returns=[]
    def execute(self,df:pd.DataFrame,params={}):
        render_full_dataset=False
        try:
            if params['render_full_dataset']=='on':
                render_full_dataset=True
        except KeyError:
            pass
        #render_full_dataset=params['render_full_dataset']
        if render_full_dataset:
            df_render = '<div style="max-width:100%;overflow-x:scroll;">'+df.to_html()+'<br></div>' #get the main thing
            shape_html='<p>'+str(df.shape[0])+' rows, '+str(df.shape[1])+' columns'+'</p>\n'
            df_render=shape_html+df_render
        #html = df.to_html()+'<br>'
        else:
            df_render=df._repr_html_()+'<br>'
        #create shape
        return df_render
class DownloadDF:
    def __init__(self):
        self.initial=False
        self.display_name='Download Dataframe'
        self.description='Provides with a link for a dataset download.'
        self.type='renderer'
        
        self.accepts=['df']
        self.returns=[]
    def execute(self,df:pd.DataFrame,params={}):
        print('params:',params)
        #TODO: somehow return a file download to the frontend
        #expecting params object to have
        #index flag
        index=False
        if params['index']=='on':
            index=True
        #name of the file = smth about function parameters
        df.to_csv(MEDIA_ROOT+'temp/'+params['params_id']+'.csv',index=index)
        return MEDIA_ROOT+'temp/'+params['params_id']+'.csv'
class LinePlotDF:
    def __init__(self):
        self.initial=False
        self.display_name='Plot Line Graph'
        self.description='Creates an interactive line graph of the DataFrame provided.'
        self.type='renderer'
    
        self.accepts=['df']
        self.returns=[]
    def execute(self,df:pd.DataFrame,params={}):
        #expected params
        do_all=False
        x=params['x']
        if not x:
            x=df.index
        y=params['y'].split(',')
        if y==['']:
            do_all=True
        labels={
            'x':params['x_label'],
            'y':params['y_label']
        }
        print('y',y)
        if do_all:
            fig=px.line(df,labels=labels)
        else:
            fig=px.line(df,x=x,y=y,labels=labels)
        #fig.update_yaxes(autorange=False)
        #return fig.to_html(include_plotlyjs='cdn',full_html=False)
        fig.write_html(MEDIA_ROOT+'temp/'+params['params_id']+'.html',config={'displaylogo': False,'responsive':False})
        return '<iframe src="/'+MEDIA_ROOT+'temp/'+params['params_id']+'.html'+'" frameBorder="0" style="width:55vw; height:63vh;"></iframe>'
class FloatPointEvolModelFit:
    def __init__(self):
        self.initial=False
        self.display_name='Floating Point Evolution Model: Fitting'
        self.description='Math Model defining Evolution of a Floating Point through utilization of several processes.\
            This function is required for the execution of the model. Requires a dataset containing values per day.'
        self.type='model'
        self.accepts=['df']
        self.returns=['models_params']
        
        self.ar_model={}
        self.garch_model={}
        self.mse_ar={}
        self.rmse_ar={}
        self.mse_garch={}
        self.rmse_garch={}
    def execute(self,df:pd.DataFrame,params={}):
        #tenor is a column from a dataset
        chosen_columns=params['chosen_column'].split(',')
        #tenor = df[chosen_column]
        p=int(params['p'])
        q=int(params['q'])
        #dist=params['dist'] #set up presets for it
        dist='Normal'
        jump_threshold=int(params['jump_threshold'])
        modelsparams={}
        for tenor in chosen_columns:
            #p,q,dist,jump_threshold - all need to appear in a form on the frontend
            result=calibrate_models(df,tenor,p,q,dist,jump_threshold)
            models_params=result[0]
            modelsparams[tenor]=models_params
            #save models for render work
            self.ar_model[tenor]=result[1]
            self.garch_model[tenor]=result[2]
            self.mse_ar[tenor]=result[3]
            self.rmse_ar[tenor]=result[4]
            self.mse_garch[tenor]=result[5]
            self.rmse_garch[tenor]=result[6]
        return modelsparams
    def render(self,execution_result):
        #produce a representation for the result object
        #return str(execution_result)
        super_html=''
        for tenor in execution_result:
            ar_summary=self.ar_model[tenor].summary().as_html().replace('</table>',
                                                                        render_to_string('function_render/table_addon.html',{
                                                                            'mse':self.mse_ar[tenor],
                                                                            'rmse':self.rmse_ar[tenor]
                                                                        })+'</table>',1)
            garch_summary=self.garch_model[tenor].summary().as_html().replace('</table>',
                                                                        render_to_string('function_render/table_addon.html',{
                                                                            'mse':self.mse_garch[tenor],
                                                                            'rmse':self.rmse_garch[tenor]
                                                                        })+'</table>',1)
            print(ar_summary)
            super_html+= render_to_string('function_render/FloatPointEvolModelFit.html',{
            'tenor':tenor,
            'models_params':execution_result[tenor],
            'ar_summary':ar_summary,
            'garch_summary':garch_summary,
            'mse_ar':self.mse_ar[tenor],
            'rmse_ar':self.rmse_ar[tenor],
            'mse_garch':self.mse_garch[tenor],
            'rmse_garch':self.rmse_garch[tenor]
        })
        return super_html
class FloatPointEvolModelForecast:
    def __init__(self):
        self.initial=False
        self.display_name='Floating Point Evolution Model: Forecast'
        self.description='Forecasting part of the Floating Point Evolution Model involving a simulation being executed through a Monte Carlo process.'
        self.type='model'
        self.accepts=['df','models_params']
        self.returns=['df']
        
        self.ar_model=None
        self.garch_model=None
    def execute(self,df:pd.DataFrame,modelsparams,params={}):
        chosen_column=params['chosen_column']
        n_simulations=int(params['n_simulations'])
        n_steps=int(params['n_steps'])
        dt=int(params['dt'])
        res=simulate_paths(df,modelsparams,n_simulations,n_steps,dt)
        df_res=pd.DataFrame(res[chosen_column]).transpose()
        df_res['mean']=df_res.mean(axis=1)
        return df_res
    
    def render(self,execution_result):
        df=execution_result
        html = df.to_html()+'<br>' #get the main thing
        #create shape
        shape_html='<p>'+str(df.shape[0])+' rows, '+str(df.shape[1])+' columns'+'</p>\n'
        return shape_html+html
class ArchModelFit:
    def __init__(self):
        self.initial=False
        self.display_name='ARCH Fit'
        self.description='ARCH Model: Initialization and fitting function.'
        self.type='model'
        self.accepts=['df']
        self.returns=['am']
        self.mse=0
        self.rmse=0
    def execute(self,df:pd.DataFrame,params={}):
        chosen_column=params['chosen_column']
        #3 apsects to the ARCH model
        #1. Mean Model
        #2. Volatility Process
        #3. Distributions
        #Each part holds a certain parameter type to supply 
        #aka on every choice there are special parameter fields
        mean=params['mean']
        lags=int(params['lags'])
        vol=params['vol']
        p=int(params['p'])
        o=int(params['o'])
        q=int(params['q'])
        power=float(params['power'])
        dist=params['dist']
        rescale=bool(params['rescale'])
        #defaults are defined on the frontend side (probably not the best)
        am=arch_model(df[chosen_column],
                      mean=mean,lags=lags,vol=vol,p=p,o=o,q=q,power=power,
                      dist=dist,rescale=rescale).fit()
        for i in am.resid:
            self.mse+=(i**2)
        self.mse/=df.shape[0]
        self.rmse=np.sqrt(self.mse)
        #print(am.summary())
        #am.summary().
        return am
    def render(self,execution_result:arch_model):
        #execution result is am
        #print(type(execution_result.summary()))
        #some html styling
        html="<div style='\
        display: flex;\
        flex-direction: column; align-items: center;'\
        >"+execution_result.summary().as_html().replace('</table>',render_to_string('function_render/table_addon.html',{
                                                                            'mse':self.mse,
                                                                            'rmse':self.rmse
                                                                        })+'</table>',1)+'</div>'
        return html

class ArchModelForecast:
    def __init__(self):
        self.initial=False
        self.display_name='ARCH Forecast'
        self.description='ARCH Model: Initialization and fitting function.'
        self.type='model'
        self.accepts=['am']
        self.returns=['df']
    def execute(self,am:ARCHModelResult,params={}):
        horizon=int(params['horizon'])
        forecast_type=params['forecast_type']
        forecasts=am.forecast(horizon=horizon)
        match forecast_type:
            case 'mean':
                df_result=forecasts.mean
            case 'residual_variance':
                df_result=forecasts.residual_variance
            case 'variance':
                df_result=forecasts.variance
        return df_result.transpose()
    def render(self,execution_result):
        df=execution_result
        html = df.to_html()+'<br>' #get the main thing
        #create shape
        shape_html='<p>'+str(df.shape[0])+' rows, '+str(df.shape[1])+' columns'+'</p>\n'
        return shape_html+html
    
        
class ARIMAModelFit:
    def __init__(self):
        self.initial=False
        self.display_name='ARIMA Fit'
        self.description='ARIMA Model: Modeling forecasts for the trained model.'
        self.type='model'
        self.accepts=['arima_model']
        self.returns=['df']
        
        self.mse=0
        self.rmse=0
    def execute(self,df:pd.DataFrame,params={}):
        chosen_column=params['chosen_column']
        p=int(params['p'])
        d=int(params['d'])
        q=int(params['q'])
        arima_model=ARIMA(df[chosen_column],order=(p,d,q)).fit()
        for i in arima_model.resid:
            self.mse+=(i**2)
        self.mse/=df.shape[0]
        self.rmse=np.sqrt(self.mse)
        return arima_model
    def render(self,execution_result):
        #execution result is am
        #print(type(execution_result.summary()))
        #some html styling
        html="<div style='\
        display: flex;\
        flex-direction: column; align-items: center;'\
        >"+execution_result.summary().as_html().replace('</table>',render_to_string('function_render/table_addon.html',{
                                                                            'mse':self.mse,
                                                                            'rmse':self.rmse
                                                                        })+'</table>',1)+'</div>'
        return html
class ARIMAModelForecast:
    def __init__(self):
        self.initial=False
        self.display_name='ARIMA Forecast'
        self.description='ARIMA Model: Modeling forecasts for the trained model.'
        self.type='model'
        self.accepts=['arima_model']
        self.returns=['df_pred']
    def execute(self,arima_model,params={}):
        steps=int(params['steps'])
        res=arima_model.get_forecast(steps=steps)
        df_pred=res.predicted_mean.to_frame()
        return df_pred
    def render(self,execution_result):
        df=execution_result
        html = df.to_html()+'<br>' #get the main thing
        #create shape
        shape_html='<p>'+str(df.shape[0])+' rows, '+str(df.shape[1])+' columns'+'</p>\n'
        return shape_html+html
    
class ARModelFit:
    def __init__(self):
        self.initial=False
        self.display_name='AutoReg Fit'
        self.description='AutoRegression Model: Initialization and fitting function.'
        self.type='model'
        self.accepts=['df']
        self.returns=['ar_model']
        
        self.mse=0
        self.rmse=0
    def execute(self,df:pd.DataFrame,params={}):
        chosen_column=params['chosen_column']
        lags=int(params['lags'])
        trend=params['trend']
        ar_model=AutoReg(df[chosen_column],lags=lags,trend=trend,missing='drop').fit()
        
        for i in ar_model.resid:
            self.mse+=(i**2)
        self.mse/=df.shape[0]
        self.rmse=np.sqrt(self.mse)
        return ar_model
    def render(self,execution_result):
        #execution result is am
        #print(type(execution_result.summary()))
        #some html styling
        html="<div style='\
        display: flex;\
        flex-direction: column; align-items: center;'\
        >"+execution_result.summary().as_html().replace('</table>',render_to_string('function_render/table_addon.html',{
                                                                            'mse':self.mse,
                                                                            'rmse':self.rmse
                                                                        })+'</table>',1)+'</div>'
        return html

class ARModelForecast:
    def __init__(self):
        self.initial=False
        self.display_name='AutoReg Forecast'
        self.description='AutoRegression Model: Modeling forecasts for the trained model.'
        self.type='model'
        self.accepts=['ar_model']
        self.returns=['df']
    def execute(self,ar_model,params={}):
        steps=int(params['steps'])
        res=ar_model.forecast(steps=steps)
        df_pred=res.to_frame()
        return df_pred
    def render(self,execution_result):
        df=execution_result
        html = df.to_html()+'<br>' #get the main thing
        #create shape
        shape_html='<p>'+str(df.shape[0])+' rows, '+str(df.shape[1])+' columns'+'</p>\n'
        return shape_html+html

class ARMAModelFit:
    def __init__(self):
        self.initial=False
        self.display_name='ARMA Fit'
        self.description='ARMA Model: Initialization and fitting function.'
        self.type='model'
        self.accepts=['df']
        self.returns=['arma_model']

        self.mse=0
        self.rmse=0
    def execute(self,df:pd.DataFrame,params={}):
        chosen_column=params['chosen_column']
        p=int(params['p'])
        q=int(params['q'])
        arma_model=ARIMA(df[chosen_column],order=(p,0,q)).fit()
        
        for i in arma_model.resid:
            self.mse+=(i**2)
        self.mse/=df.shape[0]
        self.rmse=np.sqrt(self.mse)
        return arma_model
    def render(self,execution_result):
        #execution result is am
        #print(type(execution_result.summary()))
        #some html styling
        html="<div style='\
        display: flex;\
        flex-direction: column; align-items: center;'\
        >"+execution_result.summary().as_html().replace('</table>',render_to_string('function_render/table_addon.html',{
                                                                            'mse':self.mse,
                                                                            'rmse':self.rmse
                                                                        })+'</table>',1)+'</div>'
        return html
class ARMAModelForecast:
    def __init__(self):
        self.initial=False
        self.display_name='ARMA Forecast'
        self.description='ARMA Model: Modeling forecasts for the trained model.'
        self.type='model'
        self.accepts=['arma_model']
        self.returns=['df_pred']
    def execute(self,arima_model,params={}):
        steps=int(params['steps'])
        res=arima_model.get_forecast(steps=steps)
        df_pred=res.predicted_mean.to_frame()
        return df_pred
    def render(self,execution_result):
        df=execution_result
        html = df.to_html()+'<br>' #get the main thing
        #create shape
        shape_html='<p>'+str(df.shape[0])+' rows, '+str(df.shape[1])+' columns'+'</p>\n'
        return shape_html+html

class PlotACF:
    def __init__(self):
        self.initial=False
        self.display_name='Plot ACF'
        self.description='Creates an interactive line graph of the DataFrame provided.'
        self.type='renderer'
    
        self.accepts=['df']
        self.returns=[]
    def execute(self,df:pd.DataFrame,params={}):
        chosen_column=params['chosen_column']
        lags=int(params['lags'])
        df_acf=acf(df[chosen_column],nlags=lags)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x= np.arange(len(df_acf)),
            y= df_acf,
            name= 'ACF',
            ))
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(
            title="Autocorrelation",
            xaxis_title="Lag",
            yaxis_title="Autocorrelation",
            height=500
            )
        fig.write_html(MEDIA_ROOT+'temp/'+params['params_id']+'.html',config={'displaylogo': False})
        return '<iframe src="/'+MEDIA_ROOT+'temp/'+params['params_id']+'.html'+'" frameBorder="0" style="width:55vw; height:63vh;"></iframe>'
        
class PlotPACF:
    def __init__(self):
        self.initial=False
        self.display_name='Plot PACF'
        self.description='Creates an interactive line graph of the DataFrame provided.'
        self.type='renderer'
    
        self.accepts=['df']
        self.returns=[]
    def execute(self,df:pd.DataFrame,params={}):
        chosen_column=params['chosen_column']
        lags=int(params['lags'])
        df_pacf=pacf(df[chosen_column],nlags=lags)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x= np.arange(len(df_pacf)),
            y= df_pacf,
            name= 'PACF',
            ))
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(
            title="Partial Autocorrelation",
            xaxis_title="Lag",
            yaxis_title="Partial Autocorrelation",
            height=500
            )
        fig.write_html(MEDIA_ROOT+'temp/'+params['params_id']+'.html',config={'displaylogo': False})
        return '<iframe src="/'+MEDIA_ROOT+'temp/'+params['params_id']+'.html'+'" frameBorder="0" style="width:55vw; height:63vh;"></iframe>'
        
'''
#leaving out the constructor intentionally so to not nuke the memory of the host on every api call
class LoadCSV:
    initial=True
    display_name='Load CSV'
    description='Loads a CSV file from the Datastore'
    type='loader'
    
    accepts=['.csv'] #from models.DataFile
    returns=['df']
    def execute(self,data_obj:models.DataFile):
        return pd.read_csv(data_obj.file.path)
    
class RenderDF:
    initial=False
    display_name='Render Dataframe'
    description='Invokes .to_html() of a dataframe object.'
    type='renderer'
    
    accepts=['df']
    returns=['html']
    def execute(self,df:pd.DataFrame):
        return df.to_html()
'''