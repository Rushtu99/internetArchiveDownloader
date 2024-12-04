import argparse
from internetarchive import get_item
from datetime import datetime

def list_files_from_ia(item_identifier):
    # Get the item object and iterate through its files
    item = get_item(item_identifier)

    # Create output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{item_identifier}_{timestamp}.txt"

    print(f"\nFile listing for item: {item_identifier}\n")
    print("Filename | Size (MB) | MD5")
    print("-" * 50)

    # Open file for writing
    with open(output_file, 'w') as f:
        f.write(f"File listing for item: {item_identifier}\n")
        f.write("Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        f.write("Filename | Size (MB) | MD5\n")
        f.write("-" * 50 + "\n")

        for file in item.files:
            # Skip metadata files
            if not file['name'].startswith('_'):
                size_mb = float(file.get('size', 0)) / (1024 * 1024)
                md5 = file.get('md5', 'N/A')
                output_line = f"{file['name']} | {size_mb:.2f} MB | {md5}"
                print(output_line)
                f.write(output_line + "\n")

    print(f"\nFile list has been written to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List files from Internet Archive item')
    parser.add_argument('item_identifier', help='The Internet Archive item identifier')

    args = parser.parse_args()
    list_files_from_ia(args.item_identifier)
