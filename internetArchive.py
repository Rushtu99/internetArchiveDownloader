import os
import shutil
import argparse
from internetarchive import download, get_item
from concurrent.futures import ThreadPoolExecutor
import threading

def read_files_to_download(file_path=None):
    if not file_path:
        return []

    try:
        with open(file_path, 'r') as f:
            # Skip header lines until we reach the table header
            while True:
                line = f.readline().strip()
                if line.startswith('Filename | Size'):
                    f.readline()  # Skip the separator line
                    break
                if not line:  # EOF
                    return []

            # Create a list of files to download
            files_to_download = []
            for line in f:
                if line.strip():  # Skip empty lines
                    file_name = line.split('|')[0].strip()
                    files_to_download.append(file_name)

    except FileNotFoundError:
        print(f"\n-->No existing file list found: {file_path}")
        return []

    print(f"\nFound {len(files_to_download)} files to download")
    return files_to_download

def download_single_file(item_identifier, file_info, temp_download_directory, download_directory):
    file_name = file_info['name']
    src_file = os.path.join(temp_download_directory, item_identifier, file_name)
    dest_file = os.path.join(download_directory, item_identifier, file_name)

    # Skip if file already exists in destination
    if os.path.exists(dest_file):
        print(f"-->Skipping {file_name} - already exists in destination")
        return

    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)

    # Download individual file
    try:
        download(
            item_identifier,
            files=[file_name],
            destdir=temp_download_directory,
            verbose=True,
            checksum=True,
            retries=30
        )

        # Copy the downloaded file to final destination
        if os.path.exists(src_file):
            shutil.copy2(src_file, dest_file)
            print(f"\n\n---->Copied {file_name} to final destination\n")

            # Remove the file from temp directory after copying
            os.remove(src_file)
        else:
            print(f"\n\n-->Failed to download {file_name}\n")
    except Exception as e:
        print(f"\n\n-->Error downloading {file_name}: {str(e)}\n")

def download_files_from_ia(item_identifier, download_directory, file_list=None, max_workers=4):
    # Change temp directory to be relative to current directory
    temp_download_directory = os.path.join(os.getcwd(), 'iaTempDownload')

    # Ensure the temporary download directory exists
    os.makedirs(temp_download_directory, exist_ok=True)
    os.makedirs(download_directory, exist_ok=True)

    # Get the item object
    item = get_item(item_identifier)

    # Get list of files that need to be downloaded
    files_to_download = read_files_to_download(file_list)
    if files_to_download:
        print(f"\n\n->Downloading {len(files_to_download)} files from list...\n")
    else:
        print("\n\n->No file list provided. Downloading all files...\n")

    # Filter files to download
    files_to_process = [
        file for file in item.files
        if not file['name'].startswith('_') and
           (not files_to_download or file['name'] in files_to_download)
    ]

    # Use ThreadPoolExecutor for parallel downloads
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                download_single_file,
                item_identifier,
                file,
                temp_download_directory,
                download_directory
            )
            for file in files_to_process
        ]

        # Wait for all downloads to complete
        for future in futures:
            future.result()

    # Clean up the temporary directory
    if os.path.exists(temp_download_directory):
        shutil.rmtree(temp_download_directory)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download files from Internet Archive')
    parser.add_argument('item_identifier', help='The Internet Archive item identifier')
    parser.add_argument('--file-list', help='Path to file containing list of files to download')
    parser.add_argument('--download-dir', default='E:/internetArchive',
                        help='Download directory (default: E:/internetArchive)')
    parser.add_argument('--max-workers', type=int, default=4,
                        help='Maximum number of concurrent downloads (default: 4)')

    args = parser.parse_args()
    download_files_from_ia(
        args.item_identifier,
        args.download_dir,
        args.file_list,
        args.max_workers
    )
