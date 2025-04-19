import pandas as pd
import backend.models as models


class LoadCSV:
    def __init__(self):
        self.initial=True
        self.description='Loads a CSV file from the DataStore'
        self.type='loader'
        
        self.accepts=['.csv']
        self.returns=['df']
    def execute(self,data_obj:models.DataFile):
        return pd.read_csv(data_obj.file.path)
    