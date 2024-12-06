# Internet Archive Download Scripts

A collection of Python scripts for interacting with Internet Archive items.

## Scripts Overview

### 1. Internet Archive File Lister (`internetArchiveSize.py`)

A script that generates a detailed list of files available in an Internet Archive item, including their sizes and MD5 checksums.

#### Features

-   Lists all non-metadata files in an Internet Archive item
-   Calculates file sizes in MB
-   Includes MD5 checksums
-   Saves output to a timestamped text file
-   Skips metadata files (starting with '\_')

#### Usage

```bash
python internetArchiveSize.py <item_identifier>
```

Example output file format:

```
Filename | Size (MB) | MD5
--------------------------------------------------
example.pdf | 2.45 MB | a1b2c3d4e5f6g7h8i9j0
```

### 2. Internet Archive Downloader (`internetArchive.py`)

A multi-threaded downloader for Internet Archive items that supports selective file downloading and temporary storage management.

#### Features

-   Concurrent downloads using ThreadPoolExecutor
-   Selective file downloading using a file list (generated from internetArchiveSize.py)
-   Temporary download directory management
-   Automatic checksum verification
-   Retry mechanism for failed downloads
-   Skip existing files to avoid re-downloads

#### Usage

```bash
python internetArchive.py <item_identifier> [options]
```

#### Options

-   `--file-list`: Path to a text file containing list of files to download(just remove lines of files not needed to download from generated txt file and pass here)
-   `--download-dir`: Download directory (default: E:/internetArchive)
-   `--max-workers`: Maximum number of concurrent downloads (default: 4)

#### Example

```bash
python internetArchive.py example_identifier --file-list files.txt --download-dir D:/Downloads --max-workers 6
```

## Requirements

-   Python 3.x
-   `internetarchive` package

```bash
pip install internetarchive
```

## Setup

1. Install the required package:

```bash
pip install internetarchive
```

2. Configure Internet Archive credentials (if needed):

```bash
ia configure
```

## Error Handling

Both scripts include error handling for common issues:

-   Network connectivity problems
-   File access permissions
-   Invalid item identifiers
-   Checksum verification failures

## Notes

-   The file lister creates timestamped output files in the current directory
-   The downloader uses a temporary directory for downloads before moving files to their final location
-   Both scripts skip metadata files (those starting with '\_')
-   The downloader will automatically create necessary directories
