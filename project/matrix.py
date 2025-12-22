"""
QR code matrix generation and manipulation
"""

from typing import List, Optional
from .constants import ALIGNMENT_PATTERN_POSITIONS


class QRMatrix:
    """QR code matrix representation"""

    def __init__(self, version: int):
        self.version = version
        self.size = version * 4 + 17
        self.matrix: List[List[Optional[bool]]] = [
            [None for _ in range(self.size)] for _ in range(self.size)
        ]
        self._place_finder_patterns()
        self._place_separators()
        self._place_timing_patterns()
        self._place_alignment_patterns()
        self._place_dark_module()
        self._reserve_format_areas()

    def _place_finder_patterns(self):
        """Place the three finder patterns"""
        positions = [(0, 0), (self.size - 7, 0), (0, self.size - 7)]

        for row, col in positions:
            self._draw_finder_pattern(row, col)

    def _draw_finder_pattern(self, row: int, col: int):
        """Draw a single finder pattern"""
        # Outer black square (7x7)
        for i in range(7):
            for j in range(7):
                if 0 <= row + i < self.size and 0 <= col + j < self.size:
                    self.matrix[row + i][col + j] = True

        # Inner white square (5x5)
        for i in range(1, 6):
            for j in range(1, 6):
                if 0 <= row + i < self.size and 0 <= col + j < self.size:
                    self.matrix[row + i][col + j] = False

        # Inner black square (3x3)
        for i in range(2, 5):
            for j in range(2, 5):
                if 0 <= row + i < self.size and 0 <= col + j < self.size:
                    self.matrix[row + i][col + j] = True

    def _place_separators(self):
        """Place separator patterns (white borders around finder patterns)"""
        # Horizontal separators
        for col in range(8):
            # Top-left finder separator
            if 7 < self.size:
                self.matrix[7][col] = False
            # Top-right finder separator
            if self.size - 8 + col < self.size:
                self.matrix[7][self.size - 8 + col] = False
            # Bottom-left finder separator
            if self.size - 8 < self.size:
                self.matrix[self.size - 8][col] = False

        # Vertical separators
        for row in range(8):
            # Top-left finder separator
            if 7 < self.size:
                self.matrix[row][7] = False
            # Top-right finder separator
            if self.size - 8 < self.size:
                self.matrix[row][self.size - 8] = False
            # Bottom-left finder separator
            if self.size - 8 + row < self.size and 7 < self.size:
                self.matrix[self.size - 8 + row][7] = False

    def _place_timing_patterns(self):
        """Place timing patterns"""
        # Horizontal timing pattern (row 6)
        for col in range(8, self.size - 8):
            if col < self.size:
                self.matrix[6][col] = ((col - 8) % 2 == 0)

        # Vertical timing pattern (column 6)
        for row in range(8, self.size - 8):
            if row < self.size:
                self.matrix[row][6] = ((row - 8) % 2 == 0)

    def _place_alignment_patterns(self):
        """Place alignment patterns"""
        positions = ALIGNMENT_PATTERN_POSITIONS.get(self.version, [])

        for center_row in positions:
            for center_col in positions:
                # Skip if overlaps with finder patterns
                if self._overlaps_finder(center_row, center_col):
                    continue

                self._draw_alignment_pattern(center_row, center_col)

    def _overlaps_finder(self, row: int, col: int) -> bool:
        """Check if alignment pattern overlaps with finder patterns"""
        finder_positions = [(3, 3), (self.size - 4, 3), (3, self.size - 4)]

        for fr, fc in finder_positions:
            if abs(row - fr) <= 2 and abs(col - fc) <= 2:
                return True
        return False

    def _draw_alignment_pattern(self, center_row: int, center_col: int):
        """Draw a single alignment pattern (5x5)"""
        # Alignment pattern structure:
        # ■ ■ ■ ■ ■
        # ■ □ □ □ ■
        # ■ □ ■ □ ■
        # ■ □ □ □ ■
        # ■ ■ ■ ■ ■

        pattern = [
            [True,  True,  True,  True,  True],
            [True,  False, False, False, True],
            [True,  False, True,  False, True],
            [True,  False, False, False, True],
            [True,  True,  True,  True,  True]
        ]

        for i in range(5):
            for j in range(5):
                r, c = center_row + i - 2, center_col + j - 2
                if 0 <= r < self.size and 0 <= c < self.size:
                    self.matrix[r][c] = pattern[i][j]

    def _place_dark_module(self):
        """Place the dark module"""
        self.matrix[self.size - 8][8] = True

    def _reserve_format_areas(self):
        """Reserve areas for format information"""
        # These will be filled later with format and version information
        # Horizontal format area (row 8)
        for col in range(self.size):
            if col < 9 or col >= self.size - 8:
                if self.matrix[8][col] is None:
                    self.matrix[8][col] = None  # Reserve for format info

        # Vertical format area (column 8)
        for row in range(self.size):
            if row < 9 or row >= self.size - 8:
                if self.matrix[row][8] is None:
                    self.matrix[row][8] = None  # Reserve for format info

    def place_data(self, data_bits: List[bool]):
        """Place data bits using the correct QR code data placement algorithm"""
        bit_index = 0
        total_bits = len(data_bits)

        # QR code data placement: start from bottom-right, zigzag through columns
        # Process pairs of columns from right to left
        for right_col in range(self.size - 1, -1, -2):
            # Skip timing column
            if right_col == 6:
                right_col -= 1

            left_col = right_col - 1
            if left_col == 6:
                left_col -= 1

            # Right column: bottom to top
            for row in range(self.size - 1, -1, -1):
                if row == 6:  # Skip timing row
                    continue

                # Place in right column
                if right_col >= 0 and self._is_data_cell(row, right_col):
                    if bit_index < total_bits:
                        self.matrix[row][right_col] = data_bits[bit_index]
                        bit_index += 1
                    else:
                        self.matrix[row][right_col] = False

                # Place in left column (top to bottom)
                if left_col >= 0 and self._is_data_cell(row, left_col):
                    if bit_index < total_bits:
                        self.matrix[row][left_col] = data_bits[bit_index]
                        bit_index += 1
                    else:
                        self.matrix[row][left_col] = False

        # Fill any remaining cells
        self._fill_remaining()

    def _is_data_cell(self, row: int, col: int) -> bool:
        """Check if a cell is part of the data area"""
        # Finder patterns and separators
        if row < 9 and col < 9:  # Top-left
            return False
        if row < 9 and col >= self.size - 8:  # Top-right
            return False
        if row >= self.size - 8 and col < 9:  # Bottom-left
            return False

        # Timing patterns
        if row == 6 or col == 6:
            return False

        # Dark module
        if row == self.size - 8 and col == 8:
            return False

        # Alignment patterns
        positions = ALIGNMENT_PATTERN_POSITIONS.get(self.version, [])
        for center_row in positions:
            for center_col in positions:
                if abs(row - center_row) <= 2 and abs(col - center_col) <= 2:
                    return False

        # Format areas (will be filled separately)
        if row == 8 or col == 8:
            return False

        return True

    def _fill_remaining(self):
        """Fill any remaining None cells"""
        for row in range(self.size):
            for col in range(self.size):
                if self.matrix[row][col] is None:
                    self.matrix[row][col] = False

    def apply_mask(self, mask_pattern: int):
        """Apply data masking pattern"""
        for row in range(self.size):
            for col in range(self.size):
                if self._is_data_cell(row, col):
                    if self._should_mask(row, col, mask_pattern):
                        self.matrix[row][col] = not self.matrix[row][col]

    def _should_mask(self, row: int, col: int, mask_pattern: int) -> bool:
        """Determine if a cell should be masked"""
        if mask_pattern == 0:
            return (row + col) % 2 == 0
        elif mask_pattern == 1:
            return row % 2 == 0
        elif mask_pattern == 2:
            return col % 3 == 0
        elif mask_pattern == 3:
            return (row + col) % 3 == 0
        elif mask_pattern == 4:
            return (row // 2 + col // 3) % 2 == 0
        elif mask_pattern == 5:
            return ((row * col) % 2 + (row * col) % 3) == 0
        elif mask_pattern == 6:
            return ((row * col) % 2 + (row * col) % 3) % 2 == 0
        elif mask_pattern == 7:
            return ((row + col) % 2 + (row * col) % 3) % 2 == 0
        return False

    def add_format_info(self, format_bits: int):
        """Add format information to the matrix according to ISO/IEC 18004"""
        # Format information is 15 bits: [ECC level (2 bits)][Mask pattern (3 bits)][BCH code (10 bits)]

        # Horizontal format information (row 8)
        # Positions: 0,1,2,3,4,5,7,8,14,15,16,17,18,19,20 (skipping 6=timing, 9-13=alignment/finder)

        horizontal_positions = [0, 1, 2, 3, 4, 5, 7, 8, 14, 15, 16, 17, 18, 19, 20]
        for i, col in enumerate(horizontal_positions):
            if col < self.size and i < 15:
                # Skip dark module position
                if 8 == 8 and col == 8:  # Dark module at [8][8]
                    continue
                bit_value = bool((format_bits >> (14 - i)) & 1)
                self.matrix[8][col] = bit_value

        # Vertical format information (column 8)
        # Positions: 0,1,2,3,4,5,7,8,14,15,16,17,18,19,20 (skipping 6=timing, 9-13=alignment/finder)

        vertical_positions = [0, 1, 2, 3, 4, 5, 7, 8, 14, 15, 16, 17, 18, 19, 20]
        for i, row in enumerate(vertical_positions):
            if row < self.size and i < 15:
                # Skip dark module position
                if row == self.size - 8 and 8 == 8:  # Dark module at [size-8][8]
                    continue
                bit_value = bool((format_bits >> (14 - i)) & 1)
                self.matrix[row][8] = bit_value

    def add_version_info(self, version_bits: int):
        """Add version information for versions 7-40"""
        if self.version < 7:
            return

        # Version info is placed in two 3x6 areas in the corners
        # Top-right area
        bit_pos = 0
        for i in range(6):
            for j in range(3):
                row = i
                col = self.size - 11 + j
                if bit_pos < 18:
                    self.matrix[row][col] = bool((version_bits >> (17 - bit_pos)) & 1)
                    bit_pos += 1

        # Bottom-left area
        bit_pos = 0
        for j in range(6):
            for i in range(3):
                row = self.size - 11 + i
                col = j
                if bit_pos < 18:
                    self.matrix[row][col] = bool((version_bits >> (17 - bit_pos)) & 1)
                    bit_pos += 1

    def calculate_penalty_score(self) -> int:
        """Calculate penalty score for mask pattern evaluation"""
        score = 0
        size = self.size

        # Rule 1: Adjacent modules in row/column with same color
        for row in range(size):
            run_length = 1
            for col in range(1, size):
                if self.matrix[row][col] == self.matrix[row][col - 1]:
                    run_length += 1
                else:
                    if run_length >= 5:
                        score += run_length - 2
                    run_length = 1
            if run_length >= 5:
                score += run_length - 2

        for col in range(size):
            run_length = 1
            for row in range(1, size):
                if self.matrix[row][col] == self.matrix[row - 1][col]:
                    run_length += 1
                else:
                    if run_length >= 5:
                        score += run_length - 2
                    run_length = 1
            if run_length >= 5:
                score += run_length - 2

        # Rule 2: 2x2 blocks of same color
        for row in range(size - 1):
            for col in range(size - 1):
                if (self.matrix[row][col] == self.matrix[row][col + 1] ==
                    self.matrix[row + 1][col] == self.matrix[row + 1][col + 1]):
                    score += 3

        # Rule 3: Specific patterns (finder-like)
        pattern1 = [True, False, True, True, True, False, True, False, False, False, False]
        pattern2 = [False, False, False, False, True, False, True, True, True, False, True]

        for row in range(size):
            for col in range(size - len(pattern1) + 1):
                row_slice = [self.matrix[row][col + i] for i in range(len(pattern1))]
                if row_slice == pattern1 or row_slice == pattern2:
                    score += 40

        for col in range(size):
            for row in range(size - len(pattern1) + 1):
                col_slice = [self.matrix[row + i][col] for i in range(len(pattern1))]
                if col_slice == pattern1 or col_slice == pattern2:
                    score += 40

        # Rule 4: Balance of black and white modules
        black_count = sum(sum(1 for cell in row if cell) for row in self.matrix)
        total_count = size * size
        percentage = (black_count * 100) // total_count
        deviation = abs(percentage - 50)
        score += (deviation // 5) * 10

        return score
