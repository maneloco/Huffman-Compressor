class HuffmanNode:
    def __init__(self, byte: bytes, freq: int):
        self.byte = byte
        self.freq = freq
        self.izq: HuffmanNode = None
        self.der: HuffmanNode = None
