from compressio.compress import Compress
from compressio.compression_algorithms import type_compressions
from compressio.diagnostics import (
    compress_report,
    savings,
    savings_report,
    storage_size,
)
from compressio.type_compressor import (
    BaseTypeCompressor,
    DefaultCompressor,
    SparseCompressor,
)

from .version import __version__

__all__ = [
    "Compress",
    "storage_size",
    "savings",
    "savings_report",
    "compress_report",
    "BaseTypeCompressor",
    "DefaultCompressor",
    "SparseCompressor",
    "type_compressions",
    "__version__",
]
