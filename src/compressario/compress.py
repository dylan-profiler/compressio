from compressario.type_compressions import TypeCompressor
from visions import StandardSet, Date, VisionsTypeset
import pandas as pd
import numpy as np


class StorageSize(float):
    _conversion = {
        'B': lambda x: x,
        'KB': lambda x: x / 1000,
        'MB': lambda x: x / 1000**2,
        'GB': lambda x: x / 1000**3
    }

    def __init__(self, total, units='B'):
        self.units = units
        self.total = total
        float.__init__(total)

    @property
    def _in_units(self):
        return self._conversion[self.units](self.total) 
    
    def __str__(self):
        return f"{self._in_units} {self.units}"

    def __repr__(self):
        return self.__str__()


class Compress:
    def __init__(self, typeset: VisionsTypeset = None, type_compression: TypeCompressor = None):
        self.typeset = typeset if typeset is not None else StandardSet()
        self.type_compressor = type_compression if type_compression is not None else TypeCompressor()
    
    def it(self, data):
        if isinstance(data, pd.DataFrame):
            ret = self.dataframe(data)
        elif isinstance(data, pd.Series):
            ret = self.series(data)
        else:
            raise f"Can't compress objects of type {type(data)}"
            
        return ret

    def dataframe(self, df):
        dtypes = self.typeset.detect_frame_type(df)
        return df.apply(lambda s: self.series(s, dtypes[s.name]))

    def series(self, series, dtype=None):
        if dtype is None:
            dtype = self.typeset.detect_series_type(series)

        return self.type_compressor.compress(series, dtype)

    @staticmethod
    def _dataframe_savings(df1, df2):
        s1_size = df1.memory_usage().sum()
        s2_size = df2.memory_usage().sum()
        return StorageSize(s1_size - s2_size, units='MB')
    
    @staticmethod
    def _series_savings(s1, s2):
        s1_size = s1.memory_usage()
        s2_size = s2.memory_usage()
        return StorageSize(s1_size - s2_size, units='MB')
    
    def savings(self, original_data, new_data):
        if isinstance(original_data, pd.DataFrame) and isinstance(new_data, pd.DataFrame):
            ret = self._dataframe_savings(original_data, new_data)
        elif isinstance(original_data, pd.Series) and isinstance(new_data, pd.Series):
            ret = self._series_savings(original_data, new_data)
        else:
            raise f"Can't compute memory savings for objects of type {type(original_data)} and {type(new_data)}"
        
        return ret
