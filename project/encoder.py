"""
Data encoding module for QR codes
"""

from typing import List
from .constants import EncodingMode, ALPHANUMERIC_CHARS


class DataEncoder:
    """Encodes data into QR code format"""

    @staticmethod
    def detect_mode(data: str) -> EncodingMode:
        """Automatically detect the best encoding mode for the data"""
        if data.isdigit():
            return EncodingMode.NUMERIC
        elif DataEncoder._is_alphanumeric(data):
            return EncodingMode.ALPHANUMERIC
        else:
            return EncodingMode.BYTE

    @staticmethod
    def _is_alphanumeric(data: str) -> bool:
        """Check if data can be encoded in alphanumeric mode"""
        return all(c.upper() in ALPHANUMERIC_CHARS for c in data)

    @staticmethod
    def get_mode_indicator(mode: EncodingMode) -> List[int]:
        """Get mode indicator bits (4 bits)"""
        indicators = {
            EncodingMode.NUMERIC: [0, 0, 0, 1],
            EncodingMode.ALPHANUMERIC: [0, 0, 1, 0],
            EncodingMode.BYTE: [0, 1, 0, 0],
            EncodingMode.KANJI: [1, 0, 0, 0]
        }
        return indicators[mode]

    @staticmethod
    def get_char_count_bits(mode: EncodingMode, version: int) -> int:
        """Get number of bits needed for character count"""
        if version <= 9:
            counts = {
                EncodingMode.NUMERIC: 10,
                EncodingMode.ALPHANUMERIC: 9,
                EncodingMode.BYTE: 8,
                EncodingMode.KANJI: 8
            }
        elif version <= 26:
            counts = {
                EncodingMode.NUMERIC: 12,
                EncodingMode.ALPHANUMERIC: 11,
                EncodingMode.BYTE: 16,
                EncodingMode.KANJI: 10
            }
        else:  # version 27-40
            counts = {
                EncodingMode.NUMERIC: 14,
                EncodingMode.ALPHANUMERIC: 13,
                EncodingMode.BYTE: 16,
                EncodingMode.KANJI: 12
            }
        return counts[mode]

    @staticmethod
    def encode_numeric(data: str) -> List[int]:
        """Encode numeric data"""
        bits = []

        # Process in groups of 3 digits
        for i in range(0, len(data), 3):
            group = data[i:i+3]
            value = int(group)

            if len(group) == 3:
                bit_count = 10
            elif len(group) == 2:
                bit_count = 7
            else:  # 1 digit
                bit_count = 4

            # Convert to binary (MSB first)
            for j in range(bit_count - 1, -1, -1):
                bits.append((value >> j) & 1)

        return bits

    @staticmethod
    def encode_alphanumeric(data: str) -> List[int]:
        """Encode alphanumeric data"""
        bits = []
        data = data.upper()

        # Character to value mapping
        char_values = {char: i for i, char in enumerate(ALPHANUMERIC_CHARS)}

        # Process in pairs
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                # Two characters
                val1 = char_values[data[i]]
                val2 = char_values[data[i + 1]]
                value = val1 * 45 + val2
                bit_count = 11
            else:
                # Single character
                value = char_values[data[i]]
                bit_count = 6

            # Convert to binary (MSB first)
            for j in range(bit_count - 1, -1, -1):
                bits.append((value >> j) & 1)

        return bits

    @staticmethod
    def encode_byte(data: str) -> List[int]:
        """Encode byte data (UTF-8)"""
        bits = []

        # Encode as UTF-8 bytes
        for char in data:
            byte_value = ord(char)
            # Convert byte to 8 bits (MSB first)
            for j in range(7, -1, -1):
                bits.append((byte_value >> j) & 1)

        return bits

    @staticmethod
    def encode_kanji(data: str) -> List[int]:
        """Encode Kanji data (Shift JIS)"""
        bits = []

        # Simplified Kanji encoding
        # In a full implementation, this would handle Shift JIS encoding
        # For now, fall back to byte encoding
        return DataEncoder.encode_byte(data)

    @staticmethod
    def encode(data: str, mode: EncodingMode, version: int) -> List[int]:
        """Main encoding function"""
        bits = []

        # Add mode indicator (4 bits, MSB first)
        mode_bits = DataEncoder.get_mode_indicator(mode)
        bits.extend(mode_bits)

        # Add character count (MSB first)
        char_count = len(data)
        count_bits = DataEncoder.get_char_count_bits(mode, version)
        for i in range(count_bits - 1, -1, -1):
            bits.append((char_count >> i) & 1)

        # Add encoded data
        if mode == EncodingMode.NUMERIC:
            bits.extend(DataEncoder.encode_numeric(data))
        elif mode == EncodingMode.ALPHANUMERIC:
            bits.extend(DataEncoder.encode_alphanumeric(data))
        elif mode == EncodingMode.BYTE:
            bits.extend(DataEncoder.encode_byte(data))
        elif mode == EncodingMode.KANJI:
            bits.extend(DataEncoder.encode_kanji(data))

        return bits

    @staticmethod
    def add_terminator_and_padding(bits: List[int], total_bits: int) -> List[int]:
        """Add terminator and padding to reach required length"""
        result = bits.copy()

        # Add terminator (up to 4 zeros)
        terminator_length = min(4, total_bits - len(result))
        result.extend([0] * terminator_length)

        # Pad to byte boundary
        while len(result) % 8 != 0:
            result.append(0)

        # Add padding bytes (0xEC, 0x11 alternating)
        padding_patterns = [[1, 1, 1, 0, 1, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1]]
        pattern_index = 0

        while len(result) < total_bits:
            result.extend(padding_patterns[pattern_index])
            pattern_index = (pattern_index + 1) % 2

        # Truncate if too long (shouldn't happen in correct usage)
        return result[:total_bits]