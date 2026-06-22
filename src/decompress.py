from typing import List, Dict, Tuple, FileIO
from src.huffman_node import HuffmanNode
from src.huffman_tree import create_huffman_tree
import os


def decompress(path: str, output_path: str):
    file_length = os.path.get_size(path)
    with open(path, "rb") as file:
        header_length: int= 1
        padding = file.read(1)[0]
        
        original_name_length = int.from_bytes(file.read(4), byteorder="big")
        header_length += 4 + original_name_length
        original_name_bytes = file.read(original_name_length)
        original_name = original_name_bytes.decode(encoding="utf-8")
        
        freq_list_length = int.from_bytes(file.read(2), byteorder="big")
        header_length += 2 + freq_list_length * 5
        freq_list = list()
        for _ in range(freq_list_length):
            byte = file.read(1)[0]
            freq = int.from_bytes(file.read(4), byteorder="big")
            freq_list.append((byte, freq))

        codes_dict = create_huffman_tree(freq_list)
        inverse_codes_dict = dict()
        for key, value in codes_dict.items():
            inverse_codes_dict[value] = key
    
        content_length = file_length - header_length
        counter = 0
        with open(original_name, "wb") as output:
            actual_code = ""
            while True:
                block = file.read(1024)
                if not block:
                    break
                for byte in block:
                    if counter < content_length - 1:
                        for i in range(7, -1, -1):                
                            bit = (byte >> i) & 1
                            actual_code += str(bit)
                            if actual_code in inverse_codes_dict.keys():
                                output.write(bytes([inverse_codes_dict[actual_code]]))
                                actual_code = ""
                    else:
                        if padding == 0:
                            for i in range(7, -1, -1):                
                                bit = (byte >> i) & 1
                                actual_code += str(bit)
                                if actual_code in inverse_codes_dict.keys():
                                    output.write(bytes([inverse_codes_dict[actual_code]]))
                                    actual_code = ""
                            break
                        for i in range(7, -padding, -1):
                            bit = (byte >> i) & 1
                            actual_code += str(bit)
                            if actual_code in inverse_codes_dict.keys():
                                output.write(bytes([inverse_codes_dict[actual_code]]))
                                actual_code = ""
                    counter += 1



