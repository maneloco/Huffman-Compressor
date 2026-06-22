from typing import TextIO, List, Tuple


def get_frequencies(file: TextIO) -> List[Tuple[bytes, int]]:
    bloque = file.read(1024)
    freqs_dict = dict()
    while bloque:
        for byte in bloque:
            freqs_dict[byte] = freqs_dict.get(byte, 0) + 1
        bloque = file.read(1024)
    freqs_list = list()
    for key, value in freqs_dict.items():
        freqs_list.append((key, value))
    return freqs_list
