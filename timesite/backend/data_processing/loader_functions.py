import pandas as pd


class LoadCSV:
    def __init__(self):
        self.initial=True
        self.description='Loads a CSV file from the DataStore'
        self.type='loader'
        
        self.accepts=[]
    #def execute(self):