from typing import List, Tuple, Dict
from min_heap import MinHeap
from huffman_node import HuffmanNode


def create_huffman_tree(frequencies: List[Tuple[int, int]]) -> Dict[int, str]:
    if not frequencies:
        return None

    min_heap = MinHeap(key = lambda x: x.freq)
    for byte, freq in frequencies:
        min_heap.insert(HuffmanNode(byte, freq))

    while min_heap.len() > 1:
        izq = min_heap.pop()
        der = min_heap.pop()
        father = HuffmanNode(None, izq.freq + der.freq)
        father.izq = izq
        father.der = der
        min_heap.insert(father)
    
    codes_dict = dict()
    create_code_dict(min_heap.pop(), "", codes_dict)
    return codes_dict

def create_code_dict(node: HuffmanNode, current_code: str, codes_dict: Dict):
    if not node:
        return

    if node.byte != None:
        codes_dict[node.byte] = current_code
        return

    create_code_dict(node.izq, current_code + "0", codes_dict)
    create_code_dict(node.der, current_code + "1", codes_dict)
