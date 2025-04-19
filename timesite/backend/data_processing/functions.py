import pandas as pd
import backend.models as models

'''
self.initial - declares whether the function is the leading function in a pipeline
self.type - self-referential property declaring its subclass. To be replaced with smth better most likely.
self.accepts - keywords to hint what can be fed into the function from other functions
self.returns - keywords to hint what object does it return.
'''

class LoadCSV:
    def __init__(self):
        self.initial=True
        self.description='Loads a CSV file from the DataStore'
        self.type='loader'
        
        self.accepts=['.csv'] #from models.DataFile
        self.returns=['df']
    def execute(self,data_obj:models.DataFile):
        return pd.read_csv(data_obj.file.path)
    
class RenderDF:
    def __init__(self):
        self.initial=False
        self.description='Invokes .to_html() of a dataframe object.'
        self.type='renderer'
        
        self.accepts=['df']
        self.returns=['html']
    def execute(self,df:pd.DataFrame):
        return df.to_html()
        