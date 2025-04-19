from backend.data_processing.functions import *

#class Loaders:
#    def __init__(self):

class Registry:
    def __init__(self):
        self.loaders={
            'LoadCSV':LoadCSV
        }
        self.displayers={}
        self.processors={}
        self.splitters={}
        self.models={}
    