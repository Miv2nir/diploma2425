from backend.data_processing.functions import *
import json

#class Loaders:
#    def __init__(self):


class Registry:
    #TODO: rewrite this to have only one dictionary, multiple dicts overcomplicate things
    #make sure that the function type is stored within the function object itself
    def __init__(self):
        self.loaders={
            'LoadCSV':LoadCSV
        }
        self.processors={
            'DropColumns':DropColumns,
            'FillNA':FillNA,
            'DropNA':DropNA,
            'GetQuantile':GetQuantile,
            'SetDateIndex':SetDateIndex
        }
        self.renderers={
            'RenderDF':RenderDF,
            'DownloadDF':DownloadDF,
            'LinePlotDF':LinePlotDF
        }
        self.models={
            'FloatPointEvolModelFit':FloatPointEvolModelFit,
            'ArchModelFit':ArchModelFit,
            'ARIMAModelFit':ARIMAModelFit,
            'ARIMAModelForecast':ARIMAModelForecast,
            'ARModelFit':ARModelFit
        }

    def get_all(self):
        l={}
        all_functions=[self.loaders,self.processors,self.renderers,self.models]
        for i in all_functions:
            for j in i.keys():
                l[j]=i[j]
        return l