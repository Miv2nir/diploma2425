from backend.data_processing.functions import *
import json

#class Loaders:
#    def __init__(self):


class Registry:
    test='hi'
    def __init__(self):
        self.loaders={
            'LoadCSV':LoadCSV
        }
        self.renderers={
            'RenderDF':RenderDF
        }
        self.processors={}
        self.splitters={}
        self.models={}
    def get_all(self):
        l={}
        all_functions=[self.loaders,self.renderers,self.processors,self.splitters,self.models]
        for i in all_functions:
            for j in i.keys():
                l[j]=i[j]
        return l