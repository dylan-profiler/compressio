from compressario.compress import Compress
from compressario.diagnostics import (
    compress_report,
    savings,
    savings_report,
    storage_size,
)
#from compressario.formatter import StorageSize
from compressario.type_compressor import BaseTypeCompressor, DefaultCompressor
from compressario.typing import pdT
from compressario.compression_algorithms import type_compressions

__all__ = [
    "Compress",
    "storage_size",
    "TypeCompressor",
    "StorageSize",
    "savings",
    "savings_report",
    "compress_report",
]
