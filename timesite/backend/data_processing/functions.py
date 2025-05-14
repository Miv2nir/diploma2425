import pandas as pd
import backend.models as models
from timesite.settings import MEDIA_ROOT

from statsmodels.tsa.ar_model import AutoReg
import numpy as np

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
    
class FloatPointEvolModelFit:
    def __init__(self):
        self.initial=False
        self.display_name='Floating Point Evolution Model: Fitting'
        self.description='Math Model defining Evolution of a Floating Point through utilization of several processes.\
            This function is required for the execution of the model. Requires a dataset containing values per day.'
        self.type='model'
        self.accepts=['df']
        self.returns=['models_params']
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
        models_params=calibrate_models(df,tenor,p,q,dist,jump_threshold)
        #returns models_params
        #somehow should also make a render of an output
        return models_params
    def render(self,execution_result={}):
        #produce a representation for the result object
        return str(execution_result)
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