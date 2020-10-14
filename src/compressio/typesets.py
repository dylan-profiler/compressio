from visions import String, Object, Integer, Float, Complex, Generic, DateTime, Boolean
from visions.typesets import VisionsTypeset


class DefaultCompressioTypeset(VisionsTypeset):
    def __init__(self):
        types = [Object, String, Integer, Float, Complex, Generic]
        super().__init__(types)


class SparseCompressioTypeset(VisionsTypeset):
    def __init__(self):
        types = [Object, String, Integer, Float, Complex, DateTime, Boolean, Generic]
        super().__init__(types)
