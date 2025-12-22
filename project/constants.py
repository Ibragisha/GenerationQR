"""
Constants for QR Code generation according to ISO/IEC 18004:2015
"""

from typing import Dict, List, Tuple
from enum import Enum


class ErrorCorrectionLevel(Enum):
    """Error correction levels for QR codes"""
    L = 0b01  # Low - 7%
    M = 0b00  # Medium - 15%
    Q = 0b11  # Quartile - 25%
    H = 0b10  # High - 30%


class EncodingMode(Enum):
    """Data encoding modes"""
    NUMERIC = 1
    ALPHANUMERIC = 2
    BYTE = 4
    KANJI = 8


# QR Code capacity table for versions 1-40
# Format: {version: {ecl: {'numeric': int, 'alphanumeric': int, 'byte': int, 'kanji': int,
#                          'total_codewords': int, 'groups': List[Tuple[int, int, int]]}}}
QR_CAPACITY_TABLE = {
    1: {
        'L': {'numeric': 41, 'alphanumeric': 25, 'byte': 17, 'kanji': 10, 'total_codewords': 26, 'groups': [(1, 19, 7)]},
        'M': {'numeric': 34, 'alphanumeric': 20, 'byte': 14, 'kanji': 8, 'total_codewords': 26, 'groups': [(1, 16, 10)]},
        'Q': {'numeric': 27, 'alphanumeric': 16, 'byte': 11, 'kanji': 7, 'total_codewords': 26, 'groups': [(1, 13, 13)]},
        'H': {'numeric': 17, 'alphanumeric': 10, 'byte': 7, 'kanji': 4, 'total_codewords': 26, 'groups': [(1, 9, 17)]}
    },
    2: {
        'L': {'numeric': 77, 'alphanumeric': 47, 'byte': 32, 'kanji': 20, 'total_codewords': 44, 'groups': [(1, 34, 10)]},
        'M': {'numeric': 63, 'alphanumeric': 38, 'byte': 26, 'kanji': 16, 'total_codewords': 44, 'groups': [(1, 28, 16)]},
        'Q': {'numeric': 48, 'alphanumeric': 29, 'byte': 20, 'kanji': 12, 'total_codewords': 44, 'groups': [(1, 22, 22)]},
        'H': {'numeric': 34, 'alphanumeric': 20, 'byte': 14, 'kanji': 8, 'total_codewords': 44, 'groups': [(1, 16, 28)]}
    },
    3: {
        'L': {'numeric': 127, 'alphanumeric': 77, 'byte': 53, 'kanji': 32, 'total_codewords': 70, 'groups': [(1, 55, 15)]},
        'M': {'numeric': 101, 'alphanumeric': 61, 'byte': 42, 'kanji': 26, 'total_codewords': 70, 'groups': [(1, 44, 26)]},
        'Q': {'numeric': 77, 'alphanumeric': 47, 'byte': 32, 'kanji': 20, 'total_codewords': 70, 'groups': [(2, 17, 13)]},
        'H': {'numeric': 58, 'alphanumeric': 35, 'byte': 24, 'kanji': 15, 'total_codewords': 70, 'groups': [(2, 13, 22)]}
    },
    4: {
        'L': {'numeric': 187, 'alphanumeric': 114, 'byte': 78, 'kanji': 48, 'total_codewords': 100, 'groups': [(1, 80, 20)]},
        'M': {'numeric': 149, 'alphanumeric': 90, 'byte': 62, 'kanji': 38, 'total_codewords': 100, 'groups': [(2, 32, 18)]},
        'Q': {'numeric': 111, 'alphanumeric': 67, 'byte': 46, 'kanji': 28, 'total_codewords': 100, 'groups': [(2, 24, 26)]},
        'H': {'numeric': 82, 'alphanumeric': 50, 'byte': 34, 'kanji': 21, 'total_codewords': 100, 'groups': [(4, 9, 16)]}
    },
    5: {
        'L': {'numeric': 255, 'alphanumeric': 154, 'byte': 106, 'kanji': 65, 'total_codewords': 134, 'groups': [(1, 108, 26)]},
        'M': {'numeric': 202, 'alphanumeric': 122, 'byte': 84, 'kanji': 52, 'total_codewords': 134, 'groups': [(2, 43, 22)]},
        'Q': {'numeric': 144, 'alphanumeric': 87, 'byte': 60, 'kanji': 37, 'total_codewords': 134, 'groups': [(2, 15, 18), (2, 16, 26)]},
        'H': {'numeric': 106, 'alphanumeric': 64, 'byte': 44, 'kanji': 27, 'total_codewords': 134, 'groups': [(2, 11, 24), (2, 12, 28)]}
    },
    6: {
        'L': {'numeric': 322, 'alphanumeric': 195, 'byte': 134, 'kanji': 82, 'total_codewords': 172, 'groups': [(2, 68, 18)]},
        'M': {'numeric': 255, 'alphanumeric': 154, 'byte': 106, 'kanji': 65, 'total_codewords': 172, 'groups': [(4, 27, 16)]},
        'Q': {'numeric': 178, 'alphanumeric': 108, 'byte': 74, 'kanji': 45, 'total_codewords': 172, 'groups': [(4, 19, 24)]},
        'H': {'numeric': 139, 'alphanumeric': 84, 'byte': 58, 'kanji': 36, 'total_codewords': 172, 'groups': [(4, 15, 28)]}
    },
    5: {
        'L': {'numeric': 255, 'alphanumeric': 154, 'byte': 106, 'kanji': 65, 'total_codewords': 134, 'groups': [(1, 108, 26)]},
        'M': {'numeric': 202, 'alphanumeric': 122, 'byte': 84, 'kanji': 52, 'total_codewords': 134, 'groups': [(2, 43, 22)]},
        'Q': {'numeric': 144, 'alphanumeric': 87, 'byte': 60, 'kanji': 37, 'total_codewords': 134, 'groups': [(2, 15, 18), (2, 16, 26)]},
        'H': {'numeric': 106, 'alphanumeric': 64, 'byte': 44, 'kanji': 27, 'total_codewords': 134, 'groups': [(2, 11, 24), (2, 12, 28)]}
    },
    6: {
        'L': {'numeric': 322, 'alphanumeric': 195, 'byte': 134, 'kanji': 82, 'total_codewords': 172, 'groups': [(2, 68, 18)]},
        'M': {'numeric': 255, 'alphanumeric': 154, 'byte': 106, 'kanji': 65, 'total_codewords': 172, 'groups': [(4, 27, 16)]},
        'Q': {'numeric': 178, 'alphanumeric': 108, 'byte': 74, 'kanji': 45, 'total_codewords': 172, 'groups': [(4, 19, 24)]},
        'H': {'numeric': 139, 'alphanumeric': 84, 'byte': 58, 'kanji': 36, 'total_codewords': 172, 'groups': [(4, 15, 28)]}
    },
    # Extended capacity table for versions 7-40 would go here
    # For brevity, including only versions 1-6 in this example
    # In a full implementation, all 40 versions should be included
}


# Alignment pattern positions for each version
ALIGNMENT_PATTERN_POSITIONS = {
    1: [],
    2: [6, 18],
    3: [6, 22],
    4: [6, 26],
    5: [6, 30],
    6: [6, 34],
    7: [6, 22, 38],
    8: [6, 24, 42],
    9: [6, 26, 46],
    10: [6, 28, 50],
    11: [6, 30, 54],
    12: [6, 32, 58],
    13: [6, 34, 62],
    14: [6, 26, 46, 66],
    15: [6, 26, 48, 70],
    16: [6, 26, 50, 74],
    17: [6, 30, 54, 78],
    18: [6, 30, 56, 82],
    19: [6, 30, 58, 86],
    20: [6, 34, 62, 90],
    21: [6, 28, 50, 72, 94],
    22: [6, 26, 50, 74, 98],
    23: [6, 30, 54, 78, 102],
    24: [6, 28, 54, 80, 106],
    25: [6, 32, 58, 84, 110],
    26: [6, 30, 58, 86, 114],
    27: [6, 34, 62, 90, 118],
    28: [6, 26, 50, 74, 98, 122],
    29: [6, 30, 54, 78, 102, 126],
    30: [6, 26, 52, 78, 104, 130],
    31: [6, 30, 56, 82, 108, 134],
    32: [6, 34, 60, 86, 112, 138],
    33: [6, 30, 58, 86, 114, 142],
    34: [6, 34, 62, 90, 118, 146],
    35: [6, 30, 54, 78, 102, 126, 150],
    36: [6, 24, 50, 76, 102, 128, 154],
    37: [6, 28, 54, 80, 106, 132, 158],
    38: [6, 32, 58, 84, 110, 136, 162],
    39: [6, 26, 54, 82, 110, 138, 166],
    40: [6, 30, 58, 86, 114, 142, 170],
}


# Format information table (15 bits)
# Index is (error_correction << 3) | mask_pattern
FORMAT_INFO_TABLE = [
    0b111011111000100,  # L, mask 0
    0b111001011110011,  # L, mask 1
    0b111110110101010,  # L, mask 2
    0b111100010011101,  # L, mask 3
    0b110011000101111,  # L, mask 4
    0b110001100011000,  # L, mask 5
    0b110110001000001,  # L, mask 6
    0b110100101110110,  # L, mask 7
    0b101010000010010,  # M, mask 0
    0b101000100100101,  # M, mask 1
    0b101111001111100,  # M, mask 2
    0b101101101001011,  # M, mask 3
    0b100010111111001,  # M, mask 4
    0b100000011001110,  # M, mask 5
    0b100111110010111,  # M, mask 6
    0b100101010100000,  # M, mask 7
    0b011010101011111,  # Q, mask 0
    0b011000001101000,  # Q, mask 1
    0b011111100110001,  # Q, mask 2
    0b011101000000110,  # Q, mask 3
    0b010010010110100,  # Q, mask 4
    0b010000110000011,  # Q, mask 5
    0b010111011011010,  # Q, mask 6
    0b010101111101101,  # Q, mask 7
    0b001011010001001,  # H, mask 0
    0b001001110111110,  # H, mask 1
    0b001110011100111,  # H, mask 2
    0b001100111010000,  # H, mask 3
    0b000011101100010,  # H, mask 4
    0b000001001010101,  # H, mask 5
    0b000110100001100,  # H, mask 6
    0b000100000111011,  # H, mask 7
]


# Version information table for versions 7-40 (18 bits)
VERSION_INFO_TABLE = [
    # Version 7-11
    0b000111110010010100,  # Version 7
    0b001000010110111100,  # Version 8
    0b001001101000011001,  # Version 9
    0b001010010011011110,  # Version 10
    0b001011101101001000,  # Version 11
    # Version 12-16
    0b001100011101100010,  # Version 12
    0b001101100111000111,  # Version 13
    0b001110011001101011,  # Version 14
    0b001111100011001110,  # Version 15
    0b010000101101110000,  # Version 16
    # Version 17-21
    0b010001010111010101,  # Version 17
    0b010010101001111001,  # Version 18
    0b010011010111011100,  # Version 19
    0b010100101001110110,  # Version 20
    0b010101010111100000,  # Version 21
    # Version 22-26
    0b010110101001000101,  # Version 22
    0b010111010111100110,  # Version 23
    0b011000101001101000,  # Version 24
    0b011001010111001101,  # Version 25
    0b011010101001011001,  # Version 26
    # Version 27-31
    0b011011010111111100,  # Version 27
    0b011100101001011111,  # Version 28
    0b011101010111110011,  # Version 29
    0b011110101001111101,  # Version 30
    0b011111010111011000,  # Version 31
    # Version 32-36
    0b100000100011000110,  # Version 32
    0b100001011101100011,  # Version 33
    0b100010100111001111,  # Version 34
    0b100011011101101010,  # Version 35
    0b100100100111100100,  # Version 36
    # Version 37-40
    0b100101011101000001,  # Version 37
    0b100110100111101101,  # Version 38
    0b100111011101001000,  # Version 39
    0b101000100111010110,  # Version 40
]


# Alphanumeric character set for QR codes
ALPHANUMERIC_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:'


# Generator polynomials for Reed-Solomon error correction
# Index is the number of error correction codewords
GENERATOR_POLYNOMIALS = {
    # degree: coefficients (from highest to lowest)
    7: [1, 127, 122, 154, 164, 11, 68, 117],
    10: [1, 216, 194, 159, 111, 199, 94, 95, 113, 157, 193],
    13: [1, 137, 73, 227, 17, 177, 17, 52, 13, 46, 43, 83, 132, 120],
    15: [1, 29, 196, 111, 163, 112, 74, 10, 105, 105, 139, 132, 151, 32, 134, 26],
    16: [1, 59, 13, 104, 189, 68, 209, 30, 8, 163, 65, 41, 229, 98, 50, 36, 59],
    17: [1, 119, 66, 83, 120, 119, 22, 197, 83, 249, 41, 143, 134, 85, 53, 125, 99, 79],
    18: [1, 239, 251, 183, 113, 149, 175, 199, 215, 240, 220, 73, 82, 173, 75, 32, 67, 217, 146],
    20: [1, 152, 185, 240, 5, 111, 99, 6, 220, 112, 150, 69, 36, 187, 22, 228, 198, 121, 121, 165, 174],
    22: [1, 89, 179, 131, 176, 182, 244, 19, 189, 69, 40, 28, 137, 29, 123, 67, 253, 86, 218, 230, 26, 145, 245],
    24: [1, 122, 118, 169, 70, 178, 237, 216, 102, 115, 150, 229, 73, 130, 72, 61, 43, 206, 1, 237, 247, 127, 217, 144, 117],
    26: [1, 246, 51, 183, 4, 136, 13, 227, 42, 141, 60, 65, 253, 224, 27, 217, 35, 208, 145, 7, 228, 72, 29, 111, 185, 153, 208],
    28: [1, 252, 9, 28, 13, 18, 251, 208, 150, 103, 174, 100, 41, 167, 12, 247, 56, 117, 119, 233, 127, 181, 100, 121, 147, 176, 74, 58, 197],
    30: [1, 212, 246, 77, 73, 195, 192, 75, 98, 5, 70, 103, 177, 22, 217, 138, 51, 181, 246, 72, 25, 18, 46, 228, 74, 216, 195, 11, 106, 130, 150],
}


def get_format_info(error_correction: ErrorCorrectionLevel, mask_pattern: int) -> int:
    """Get format information bits for given error correction level and mask pattern"""
    # Use precomputed table for format information
    # This ensures correctness according to ISO/IEC 18004
    ec_map = {
        ErrorCorrectionLevel.L: 0,   # L -> 0-7
        ErrorCorrectionLevel.M: 8,   # M -> 8-15
        ErrorCorrectionLevel.Q: 16,  # Q -> 16-23
        ErrorCorrectionLevel.H: 24   # H -> 24-31
    }
    index = ec_map[error_correction] + mask_pattern
    if index >= len(FORMAT_INFO_TABLE):
        raise ValueError(f"Invalid format info index: {index}")
    return FORMAT_INFO_TABLE[index]


def get_version_info(version: int) -> int:
    """Get version information bits for given version (7-40)"""
    if 7 <= version <= 40:
        return VERSION_INFO_TABLE[version - 7]
    return 0


def get_capacity(version: int, error_correction: ErrorCorrectionLevel, mode: EncodingMode) -> int:
    """Get maximum capacity for given parameters"""
    if version not in QR_CAPACITY_TABLE:
        raise ValueError(f"Version {version} not supported")

    ecl_name = error_correction.name
    mode_name = mode.name.lower()

    if ecl_name not in QR_CAPACITY_TABLE[version]:
        raise ValueError(f"Error correction level {ecl_name} not supported for version {version}")

    if mode_name not in QR_CAPACITY_TABLE[version][ecl_name]:
        raise ValueError(f"Mode {mode_name} not supported for version {version} with ECL {ecl_name}")

    return QR_CAPACITY_TABLE[version][ecl_name][mode_name]
