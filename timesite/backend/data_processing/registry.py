from backend.data_processing.functions import *
import json

#class Loaders:
#    def __init__(self):

class Registry:

    loaders={
        'LoadCSV':LoadCSV
    }
    renderers={
        'RenderDF':RenderDF
    }
    processors={}
    splitters={}
    models={}
    #def get_json_lists(self):

#class Registry:
#    test='hi'
#    def __init__(self):
#        self.loaders={
#            'LoadCSV':LoadCSV
#        }
#        self.renderers={
#            'RenderDF':RenderDF
#        }
#        self.processors={}
#        self.splitters={}
#        self.models={}