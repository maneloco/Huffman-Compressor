from typing import List, Dict, Tuple
from src.huffman_node import HuffmanNode
from src.huffman_tree import create_huffman_tree
import os


def decompress(file_path: str, output_path: str):
    file_length = os.path.get_size(file_path)
    with open(file_path, "rb") as file:
        padding, original_name, freq_list_length, header_length = get_header(file)
        inverse_codes_dict = get_inverse_codes_dict(file, freq_list_length)

        content_length = file_length - header_length
        counter = 0
        with open(os.path.join(output_path, original_name), "wb") as output:
            actual_code = ""
            while True:
                block = file.read(1024)
                if not block:
                    break
                for byte in block:
                    if counter < content_length - 1:
                        actual_code = bit_comparer(byte, output, inverse_codes_dict, actual_code)
                    else:
                        bit_comparer(byte, output, inverse_codes_dict, actual_code, padding)
                    counter += 1

def bit_comparer(byte, output, inverse_codes_dict, actual_code, padding = 0):

    for i in range(7, padding-1, -1):
        bit = (byte >> i) & 1
        actual_code += str(bit)
        if actual_code in inverse_codes_dict:
            output.write(bytes([inverse_codes_dict[actual_code]]))
            actual_code = ""
    return actual_code

def get_header(file):
    header_length: int= 1
    padding = file.read(1)[0]
        
    original_name_length = int.from_bytes(file.read(4), byteorder="big")
    header_length += 4 + original_name_length
    original_name_bytes = file.read(original_name_length)
    original_name = original_name_bytes.decode(encoding="utf-8")
        
    freq_list_length = int.from_bytes(file.read(2), byteorder="big")
    header_length += 2 + freq_list_length * 5
    
    return padding, original_name, freq_list_length, header_length

def get_inverse_codes_dict(file, freq_list_length: int):
    freq_list = list()
    for _ in range(freq_list_length):
        byte = file.read(1)[0]
        freq = int.from_bytes(file.read(4), byteorder="big")
        freq_list.append((byte, freq))

    codes_dict = create_huffman_tree(freq_list)
    inverse_codes_dict = dict()
    for key, value in codes_dict.items():
        inverse_codes_dict[value] = key
    return inverse_codes_dict

