""""
Example:
    >>> from qrcode_generator import QRCode, ErrorCorrectionLevel
    >>> qr = QRCode("Hello World", ErrorCorrectionLevel.M)
    >>> qr.save_png("hello.png")
"""

from .core import QRCode, ErrorCorrectionLevel, EncodingMode
from .constants import VERSION_INFO_TABLE, QR_CAPACITY_TABLE, FORMAT_INFO_TABLE

__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "QR Code generator implementing ISO/IEC 18004"

__all__ = [
    "QRCode",
    "ErrorCorrectionLevel",
    "EncodingMode",
    "VERSION_INFO_TABLE",
    "QR_CAPACITY_TABLE",
    "FORMAT_INFO_TABLE",
]
