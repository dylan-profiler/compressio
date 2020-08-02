from compressario.compress import Compress, storage_size
from compressario.diagnostics import compress_report, savings, savings_report
from compressario.formatter import StorageSize
from compressario.type_compressions import TypeCompressor

__all__ = [
    "Compress",
    "storage_size",
    "TypeCompressor",
    "StorageSize",
    "savings",
    "savings_report",
    "compress_report",
]
