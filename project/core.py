"""
Core QR code generation functionality
"""

from typing import List, Optional, Tuple
from .constants import (
    ErrorCorrectionLevel, EncodingMode, QR_CAPACITY_TABLE,
    get_format_info, get_version_info
)
from .encoder import DataEncoder
from .error_correction import ReedSolomonEncoder
from .matrix import QRMatrix


class QRCode:
    """Main QR code generator class"""

    def __init__(self, data: str, error_correction: ErrorCorrectionLevel = ErrorCorrectionLevel.M):
        self.data = data
        self.error_correction = error_correction
        self.version = self._determine_version()
        self.mode = DataEncoder.detect_mode(data)
        self.mask_pattern = 0
        self.matrix: Optional[QRMatrix] = None

        # Generate the QR code
        self._generate()

    def _determine_version(self) -> int:
        """Determine the minimum QR version needed for the data"""
        mode = DataEncoder.detect_mode(self.data)
        ecl_name = self.error_correction.name

        for version in range(1, 7):  # Support versions 1-6 for now
            if version in QR_CAPACITY_TABLE:
                capacity_info = QR_CAPACITY_TABLE[version].get(ecl_name, {})
                capacity = capacity_info.get(mode.name.lower(), 0)
                if len(self.data) <= capacity:
                    return version

        raise ValueError(f"Data too long for supported versions (max ~1000 chars)")

    def _generate(self):
        """Generate the complete QR code"""
        # Encode data
        encoded_data = DataEncoder.encode(self.data, self.mode, self.version)

        # Add terminator and padding
        capacity_info = QR_CAPACITY_TABLE[self.version][self.error_correction.name]
        total_codewords = capacity_info['total_codewords']
        total_bits = total_codewords * 8
        padded_data = DataEncoder.add_terminator_and_padding(encoded_data, total_bits)

        # Convert to codewords (MSB first)
        data_codewords = []
        for i in range(0, len(padded_data), 8):
            codeword = 0
            for j in range(8):
                if i + j < len(padded_data):
                    codeword |= padded_data[i + j] << (7 - j)  # MSB first
            data_codewords.append(codeword)

        # Calculate number of data codewords
        data_codewords_count = 0
        for num_blocks, data_words, ecc_words in capacity_info['groups']:
            data_codewords_count += num_blocks * data_words

        # Take only data codewords (exclude padding that will be replaced by ECC)
        actual_data_codewords = data_codewords[:data_codewords_count]

        # Apply error correction and interleave
        interleaved = self._apply_error_correction_and_interleave(actual_data_codewords)

        # Convert back to bits (MSB first)
        data_bits = []
        for codeword in interleaved:
            for i in range(7, -1, -1):  # MSB first
                data_bits.append(bool((codeword >> i) & 1))

        # Choose best mask pattern
        self.mask_pattern = self._choose_best_mask(data_bits)

        # Create final matrix
        self.matrix = QRMatrix(self.version)
        self.matrix.place_data(data_bits)

        # Apply the chosen mask pattern
        self.matrix.apply_mask(self.mask_pattern)

        # Add format and version information
        format_bits = get_format_info(self.error_correction, self.mask_pattern)
        self.matrix.add_format_info(format_bits)

        if self.version >= 7:
            version_bits = get_version_info(self.version)
            self.matrix.add_version_info(version_bits)

    def _apply_error_correction_and_interleave(self, data_codewords: List[int]) -> List[int]:
        """Apply error correction and interleave data and ECC codewords"""
        capacity_info = QR_CAPACITY_TABLE[self.version][self.error_correction.name]
        groups = capacity_info['groups']

        rs_encoder = ReedSolomonEncoder()
        data_blocks = []
        ecc_blocks = []

        codeword_index = 0

        for num_blocks, data_words, ecc_words in groups:
            for _ in range(num_blocks):
                # Extract block data (exactly data_words codewords)
                block_data = []
                for _ in range(data_words):
                    if codeword_index < len(data_codewords):
                        block_data.append(data_codewords[codeword_index])
                        codeword_index += 1
                    else:
                        block_data.append(0)  # Pad with zeros if needed

                # Generate ECC for this block
                block_ecc = rs_encoder.encode(block_data, ecc_words)

                data_blocks.append(block_data)
                ecc_blocks.append(block_ecc)

        # For version 1, no interleaving needed - just concatenate data + ECC
        if self.version == 1:
            result = []
            if data_blocks:
                result.extend(data_blocks[0])  # First (and only) data block
            if ecc_blocks:
                result.extend(ecc_blocks[0])  # First (and only) ECC block
            return result

        # Interleave data blocks (take one codeword from each block in round-robin)
        result = []
        max_data_len = max(len(block) for block in data_blocks) if data_blocks else 0
        for i in range(max_data_len):
            for block in data_blocks:
                if i < len(block):
                    result.append(block[i])

        # Interleave ECC blocks
        max_ecc_len = max(len(block) for block in ecc_blocks) if ecc_blocks else 0
        for i in range(max_ecc_len):
            for block in ecc_blocks:
                if i < len(block):
                    result.append(block[i])

        return result

    def _choose_best_mask(self, data_bits: List[bool]) -> int:
        """Choose the best mask pattern by evaluating penalty scores"""
        best_mask = 0
        best_score = float('inf')

        for mask_pattern in range(8):
            # Create test matrix
            test_matrix = QRMatrix(self.version)
            test_matrix.place_data(data_bits)
            test_matrix.apply_mask(mask_pattern)

            # Calculate penalty
            score = test_matrix.calculate_penalty_score()

            if score < best_score:
                best_score = score
                best_mask = mask_pattern

        return best_mask

    def get_matrix(self) -> List[List[bool]]:
        """Get the QR code matrix"""
        if self.matrix is None:
            raise RuntimeError("QR code not generated")
        return self.matrix.matrix

    def get_size(self) -> int:
        """Get the size of the QR code matrix"""
        return self.version * 4 + 17

    def save_png(self, filename: str, scale: int = 10, border: int = 4,
                 dark_color: Tuple[int, int, int] = (0, 0, 0),
                 light_color: Tuple[int, int, int] = (255, 255, 255),
                 background_color: Tuple[int, int, int] = (255, 255, 255)):
        """Save QR code as PNG image"""
        try:
            from PIL import Image
        except ImportError:
            raise ImportError("Pillow is required for PNG output. Install with: pip install Pillow")

        if self.matrix is None:
            raise RuntimeError("QR code not generated")

        size = self.get_size()
        img_size = (size + 2 * border) * scale

        # Create image
        img = Image.new('RGB', (img_size, img_size), background_color)
        pixels = img.load()

        # Draw QR code
        for img_y in range(img_size):
            for img_x in range(img_size):
                qr_x = (img_x // scale) - border
                qr_y = (img_y // scale) - border

                if 0 <= qr_x < size and 0 <= qr_y < size:
                    if self.matrix.matrix[qr_y][qr_x]:
                        pixels[img_x, img_y] = dark_color
                    else:
                        pixels[img_x, img_y] = light_color
                # Background color is already set

        img.save(filename, 'PNG')

    def save_svg(self, filename: str, scale: int = 10, border: int = 4,
                 dark_color: str = 'black', light_color: str = 'white'):
        """Save QR code as SVG image"""
        try:
            import svgwrite
        except ImportError:
            raise ImportError("svgwrite is required for SVG output. Install with: pip install svgwrite")

        if self.matrix is None:
            raise RuntimeError("QR code not generated")

        size = self.get_size()
        img_size = (size + 2 * border) * scale

        # Create SVG
        dwg = svgwrite.Drawing(filename, size=(img_size, img_size))

        # Background
        dwg.add(dwg.rect(insert=(0, 0), size=(img_size, img_size), fill=light_color))

        # Draw modules
        for y in range(size):
            for x in range(size):
                if self.matrix.matrix[y][x]:
                    dwg.add(dwg.rect(
                        insert=((x + border) * scale, (y + border) * scale),
                        size=(scale, scale),
                        fill=dark_color
                    ))

        dwg.save()

    def save_eps(self, filename: str, scale: int = 10, border: int = 4):
        """Save QR code as EPS image"""
        if self.matrix is None:
            raise RuntimeError("QR code not generated")

        size = self.get_size()
        img_size = (size + 2 * border) * scale

        with open(filename, 'w') as f:
            # EPS header
            f.write("%!PS-Adobe-3.0 EPSF-3.0\n")
            f.write(f"%%BoundingBox: 0 0 {img_size} {img_size}\n")
            f.write("%%EndComments\n")
            f.write("/pixel { rectfill } def\n")

            # Draw background
            f.write(f"0 0 {img_size} {img_size} rectfill\n")

            # Set black color for modules
            f.write("0 0 0 setrgbcolor\n")

            # Draw black modules
            for y in range(size):
                for x in range(size):
                    if self.matrix.matrix[y][x]:
                        px = (x + border) * scale
                        py = img_size - (y + border + 1) * scale  # Flip Y coordinate
                        f.write(f"{px} {py} {scale} {scale} rectfill\n")

            f.write("%%EOF\n")

    def __str__(self) -> str:
        """String representation of the QR code"""
        if self.matrix is None:
            return "QR Code not generated"

        lines = []
        for row in self.matrix.matrix:
            line = ''.join('██' if cell else '  ' for cell in row)
            lines.append(line)

        return '\n'.join(lines)
