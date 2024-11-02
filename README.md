# Unity Documentation to PDF Converter

A Python tool that converts Unity's offline documentation into a single, searchable PDF file. This tool preserves the documentation's structure and hierarchy based on Unity's official table of contents.

## Features

- Converts Unity Manual documentation to a single PDF file
- Maintains original documentation hierarchy from Unity's TOC
- Preserves document structure and nesting levels
- Optimizes text formatting and readability
- Processes documentation in small batches to manage memory usage
- Includes progress tracking and logging
- Supports custom output file naming

## Prerequisites

- Python 3.6 or higher
- wkhtmltopdf installed on your system ([Download here](https://wkhtmltopdf.org/downloads.html))
- Unity Documentation files (offline version)

## Installation

1. Download Unity's offline documentation:
   - Visit [Unity's Offline Documentation page](https://docs.unity3d.com/Manual/OfflineDocumentation.html)

2. Clone this repository:
   ```bash
   git clone https://github.com/cavallimarko/UnityDocumentationOfflinePDFGenerator.git
   ```

3. Install required Python packages:
   ```bash
   pip install beautifulsoup4
   pip install pdfkit
   pip install PyPDF2
   ```

4. Ensure wkhtmltopdf is installed and accessible in your system PATH (default installation path on Windows: `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`)

## Usage

Run the script with the following command:
```bash
python docs_to_pdf.py --docs-folder "path/to/unity/documentation" --output "output_filename.pdf"
```

### Arguments

- `--docs-folder` (required): Path to the Unity documentation Manual folder
- `--output` (optional): Name of the output PDF file (default: unity_manual.pdf)

## Dependencies

- beautifulsoup4
- pdfkit
- PyPDF2
- wkhtmltopdf (external dependency)

## How It Works

1. Reads the Unity documentation's table of contents (toc.json)
2. Creates a hierarchical structure of documentation pages
3. Processes pages in the order defined by the TOC
4. Maintains proper document nesting and hierarchy
5. Converts documentation in small batches
6. Merges individual PDFs into a single file
7. Removes temporary files

## Document Structure

The PDF is generated following Unity's official documentation structure:
- Unity User Manual
  - Documentation versions
  - Offline documentation
  - Trademarks and terms of use
- New Features
- Package documentation
- etc.

## Limitations

- Currently processes only the Manual section (excludes Script Reference)
- Requires local Unity documentation files
- Some interactive elements may not be preserved in PDF format

## License

[Your chosen license]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 