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

    origin_path = os.path.abspath(args.path)

    if not os.path.exists(origin_path):
        print(f"❌ Error: The file '{origin_path}' does not exist.")
        return

    if args.compress:
        original_name = os.path.basename(origin_path)
        
        if args.output:
            output_base = os.path.abspath(args.output)
        else:
            output_base = os.path.splitext(origin_path)[0]

        output_dir = os.path.dirname(output_base + ".huff")
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        print(f"📦 Compressing: {origin_path} -> {output_base}.huff")

        with open(origin_path, "rb") as file:
            frequencies = get_frequencies(file)

        codes_dict = create_huffman_tree(frequencies)

        padding = compress(origin_path, output_base, codes_dict)

        write_header(output_base, original_name, padding, frequencies)
        print("✨ Compression completed successfully.")

    elif args.decompress:
        if args.output:
            output_dir = os.path.abspath(args.output)
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = os.getcwd()

        print(f"🔓 Decompressing: {origin_path} -> {output_dir}")

        decompress(origin_path, output_dir)
        print(f"✨ File restored successfully inside: {output_dir}")

    if args.remove:
        print(f"🗑️ Removing source .huff file: {origin_path}")
        os.remove(origin_path)

if __name__ == "__main__":
    main()
