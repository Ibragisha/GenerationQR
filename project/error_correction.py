"""
Reed-Solomon error correction implementation for QR codes
"""

from typing import List
from .constants import GENERATOR_POLYNOMIALS


class GaloisField:
    """Arithmetic operations in Galois Field GF(256)"""

    def __init__(self):
        self.exp_table = [0] * 512
        self.log_table = [0] * 256
        self._init_tables()

    def _init_tables(self):
        """Initialize exponential and logarithmic tables"""
        x = 1
        for i in range(255):
            self.exp_table[i] = x
            self.exp_table[i + 255] = x
            self.log_table[x] = i
            x <<= 1
            if x & 0x100:
                x ^= 0x11D  # x^8 + x^4 + x^3 + x^2 + 1

        self.exp_table[255] = self.exp_table[0]

    def mul(self, a: int, b: int) -> int:
        """Multiplication in GF(256)"""
        if a == 0 or b == 0:
            return 0
        return self.exp_table[self.log_table[a] + self.log_table[b]]

    def div(self, a: int, b: int) -> int:
        """Division in GF(256)"""
        if b == 0:
            raise ValueError("Division by zero")
        if a == 0:
            return 0
        return self.exp_table[(self.log_table[a] - self.log_table[b]) % 255]

    def pow(self, x: int, n: int) -> int:
        """Exponentiation in GF(256)"""
        if n == 0:
            return 1
        if x == 0:
            return 0
        return self.exp_table[(self.log_table[x] * n) % 255]

    def inverse(self, x: int) -> int:
        """Multiplicative inverse in GF(256)"""
        if x == 0:
            raise ValueError("Zero has no inverse")
        return self.exp_table[255 - self.log_table[x]]


class ReedSolomonEncoder:
    """Reed-Solomon encoder for QR codes"""

    def __init__(self):
        self.gf = GaloisField()

    def encode(self, data: List[int], ecc_count: int) -> List[int]:
        """Encode data with Reed-Solomon error correction"""
        if ecc_count not in GENERATOR_POLYNOMIALS:
            raise ValueError(f"No generator polynomial for {ecc_count} ECC codewords")

        # Create message polynomial (data + ecc_count zeros)
        message = data + [0] * ecc_count

        # Get generator polynomial
        generator = GENERATOR_POLYNOMIALS[ecc_count]  # Already in correct order

        # Perform polynomial division (Galois Field arithmetic)
        for i in range(len(data)):
            coef = message[i]
            if coef != 0:
                for j in range(len(generator)):
                    # XOR with multiplication in GF(256)
                    # Generator polynomial coefficients are from highest to lowest degree
                    message[i + j] ^= self.gf.mul(generator[len(generator) - 1 - j], coef)

        # Return ECC codewords (last ecc_count elements)
        return message[-ecc_count:]


class ReedSolomonDecoder:
    """Reed-Solomon decoder for error correction (optional)"""

    def __init__(self):
        self.gf = GaloisField()

    def decode(self, received: List[int], ecc_count: int) -> List[int]:
        """Attempt to decode and correct errors"""
        # This is a simplified implementation
        # Full Reed-Solomon decoding is complex and not required for QR code generation
        # QR codes rely on the error correction being done at scan time
        return received[:-ecc_count] if len(received) > ecc_count else received
