from src.frequencies import get_frequencies
from src.compress import compress, write_header
from src.huffman_tree import create_huffman_tree
from src.decompress import decompress
import argparse
import os


def main():
    parser = argparse.ArgumentParser(
            description="Script to compress using the Huffman Method."
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
            "-c",
            "--compress",
            action="store_true",
            help="This flag is to compress a file into .huff ."
    )

    group.add_argument(
            "-d",
            "--decompress",
            action="store_true",
            help="This flag is to decompress a .huff file."
    )

    parser.add_argument(
            "path",
            type=str,
            help="Path of the origin file."
    )
    parser.add_argument(
            "-rm",
            "--remove",
            action="store_true",
            help="This flag is to remove a file after compression."
    )

    parser.add_argument(
            "-o",
            "--output",
            type=str,
            help="Specify a route or a filename for the compressed file."
    )

    args = parser.parse_args()

    if args.output and not args.compress:
        parser.error(
                "The --output flag must be used in compress only (-c, --compress)."
        )

    if args.compress:
        origin_path = args.path
        original_name = os.path.basename(origin_path)
        output_base = args.output if args.output else origin_path
        output_dir = os.path.dirname(output_base + ".huff")
        if output_dir:
            os.makedirs(output_dir, exist_ok = True)


        print(f"📦 Compressing: {args.path} -> Destination: {output_base}.huff")
        
        with open(origin_path, "rb") as file:
            frequencies = get_frequencies(file)
        
        codes_dict = create_huffman_tree(frequencies)
        
        with open(origin_path, "rb") as file:
            padding = compress(file, codes_dict, output_base)

        write_header(output_base, original_name, padding, frequencies)

        print("✨ Compression completed successfully.")

        if args.remove:
            print(f"🗑️ Removing original uncompressed file: {origin_path}")
            os.remove(origin_path)

    elif args.decompress:
        origin_path = args.path
        print(f"🔓 Decompressing: {args.path}")

        actual_directory = os.getcwd()
        os.makedirs(actual_directory, exist_ok=True)

        decompress(origin_path, "")
        print("✨ File restored successfully.")

        if args.remove:
            print(f"🗑️ Removing source .huff file: {origin_path}")
            os.remove(origin_path)
