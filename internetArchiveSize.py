import argparse
from internetarchive import get_item
from datetime import datetime

def list_files_from_ia(item_identifier):
    # Get the item object and iterate through its files
    item = get_item(item_identifier)

    # Create output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{item_identifier}_{timestamp}.txt"

    # Initialize counters
    total_size = 0
    file_count = 0
    files_info = []

    # Collect file information
    for file in item.files:
        if not file['name'].startswith('_'):
            size_mb = float(file.get('size', 0)) / (1024 * 1024)
            total_size += size_mb
            file_count += 1
            files_info.append({
                'name': file['name'],
                'size': size_mb,
                'md5': file.get('md5', 'N/A')
            })

    # Write to file
    with open(output_file, 'w') as f:
        # Write header information
        f.write(f"File listing for item: {item_identifier}\n")
        f.write("Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write(f"Total Files: {file_count}\n")
        f.write(f"Total Size: {total_size:.2f} MB\n\n")
        f.write("Filename | Size (MB) | MD5\n")
        f.write("-" * 50 + "\n")

        # Write file details
        for file in files_info:
            output_line = f"{file['name']} | {file['size']:.2f} MB | {file['md5']}"
            f.write(output_line + "\n")

    # Print summary to console
    print(f"\nSummary for item: {item_identifier}")
    print(f"Total Files: {file_count}")
    print(f"Total Size: {total_size:.2f} MB")
    print(f"\nDetailed file list has been written to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List files from Internet Archive item')
    parser.add_argument('item_identifier', help='The Internet Archive item identifier')

    args = parser.parse_args()
    list_files_from_ia(args.item_identifier)
