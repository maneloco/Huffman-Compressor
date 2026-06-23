from typing import Dict, List, Tuple
import os


def compress(file_path:str, output_path: str, codes_dict: Dict[bytes, str]):
    output_path += ".huff.tmp"
    with open(output_path, "wb") as output:
        accumulator: int = 0
        bit_counter: int = 0
        with open(file_path, "rb") as file:
            output_buffer = bytearray()
            block = file.read(1024)
            while block:
                for byte in block:
                    current_huff = codes_dict[byte]
                    for bit in current_huff:
                        accumulator = accumulator << 1
                        accumulator = accumulator | int(bit)
                        bit_counter += 1
                        if bit_counter == 8:
                            output_buffer.append(accumulator)
                            accumulator = 0
                            bit_counter = 0
                        if len(output_buffer) == 1024:
                            output.write(output_buffer)
                            output_buffer = bytearray()
                block = file.read(1024)
            if bit_counter != 0:
                for _ in range((8 - bit_counter) % 8):
                    accumulator = accumulator << 1
                output_buffer.append(accumulator)
            output.write(output_buffer)
    return (8 - bit_counter) % 8

def write_header(output_path: str, original_name: str, padding: int, freq_list: List[Tuple[bytes, int]]):
    header = bytearray()
    header.append(padding)

    original_name_bytes = bytearray(original_name, encoding="utf-8")
    header.extend(int(len(original_name_bytes)).to_bytes(4, byteorder="big"))
    header.extend(original_name_bytes)

    header.extend(int(len(freq_list)).to_bytes(2, byteorder="big"))
    for byte, freq in freq_list:
        header.append(byte)
        header.extend(freq.to_bytes(4, byteorder="big"))

    output_path += ".huff"
    temp_path = output_path + ".tmp"
    with open(output_path, "wb") as file:
        file.write(header)
        with open(temp_path, "rb") as temp:
            while True:
                buffer = temp.read(1024)
                if not buffer:
                    break
                file.write(buffer)
    os.remove(temp_path)


