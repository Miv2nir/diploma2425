import pandas as pd
import backend.models as models
from timesite.settings import MEDIA_ROOT

from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from django.template.loader import render_to_string
from arch import arch_model

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
        html = df.to_html()+'<br>' #get the main thing
        #create shape
        shape_html='<p>'+str(df.shape[0])+' rows, '+str(df.shape[1])+' columns'+'</p>\n'
        return shape_html+html
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
        x=params['x']
        y=params['y'].split(',')
        labels={
            'x':params['x_label'],
            'y':params['y_label']
        }
        fig=px.line(df,x=x,y=y,labels=labels)
        #return fig.to_html(include_plotlyjs='cdn',full_html=False)
        fig.write_html(MEDIA_ROOT+'temp/'+params['params_id']+'.html',config={'displaylogo': False})
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
        
        self.ar_model=None
        self.garch_model=None
    def execute(self,df:pd.DataFrame,params={}):
        #tenor is a column from a dataset
        chosen_column=params['chosen_column']
        #tenor = df[chosen_column]
        tenor = chosen_column
        #p,q,dist,jump_threshold - all need to appear in a form on the frontend
        p=int(params['p'])
        q=int(params['q'])
        #dist=params['dist'] #set up presets for it
        dist='Normal'
        jump_threshold=int(params['jump_threshold'])
        result=calibrate_models(df,tenor,p,q,dist,jump_threshold)
        models_params=result[0]
        #save models for render work
        self.ar_model=result[1]
        self.garch_model=result[2]
        return models_params
    def render(self,execution_result):
        #produce a representation for the result object
        #return str(execution_result)
        
        return render_to_string('function_render/FloatPointEvolModelFit.html',{
            'models_params':execution_result,
            'ar_summary':self.ar_model.summary().as_html(),
            'garch_summary':self.garch_model.summary().as_html()
        })

class ArchModelFit:
    def __init__(self):
        self.initial=False
        self.display_name='ARCH Fit'
        self.description='ARCH Model: Initialization and fitting function.'
        self.type='model'
        self.accepts=['df']
        self.returns=['am']
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
        >"+execution_result.summary().as_html()+'</div>'
        return html
class ARIMAModelFit:
    def __init__(self):
        self.initial=False
        self.display_name='ARIMA Fit'
        self.description='ARIMA Model: Initialization and fitting function.'
        self.type='model'
        self.accepts=['df']
        self.returns=['arima_model']
    def execute(self,df:pd.DataFrame,params={}):
        chosen_column=params['chosen_column']
        p=int(params['p'])
        d=int(params['d'])
        q=int(params['q'])
        arima_model=ARIMA(df[chosen_column],order=(p,d,q)).fit()
        return arima_model
    def render(self,execution_result):
        #execution result is am
        #print(type(execution_result.summary()))
        #some html styling
        html="<div style='\
        display: flex;\
        flex-direction: column; align-items: center;'\
        >"+execution_result.summary().as_html()+'</div>'
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