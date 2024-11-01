import os
from bs4 import BeautifulSoup
import pdfkit
from urllib.parse import urljoin
import logging
import time
import argparse

class UnityDocConverter:
    def __init__(self, docs_folder, output_pdf):
        self.docs_folder = docs_folder
        self.output_pdf = output_pdf
        self.visited_links = set()
        
        # Configure pdfkit
        self.config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def parse_html_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
                # Force text color to black
                for text_element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'a', 'li']):
                    text_element['style'] = 'color: #000000 !important;'
                
                # Remove unnecessary elements
                for element in soup.select('nav, footer, .search-bar, .unnecessary-class'):
                    element.decompose()
                
                # Keep only the main content
                main_content = soup.select_one('main, .main-content, article')
                if main_content:
                    return BeautifulSoup(str(main_content), 'html.parser')
                return soup
        except Exception as e:
            self.logger.error(f"Error parsing {file_path}: {str(e)}")
            return None

    def get_links(self, soup, base_path):
        links = []
        if not soup:
            return links
            
        for a in soup.find_all('a'):
            href = a.get('href')
            if href and href.endswith('.html') and not href.startswith(('http://', 'https://')):
                full_path = os.path.normpath(os.path.join(os.path.dirname(base_path), href))
                # Only include files that are in the Manual folder
                if (full_path not in self.visited_links 
                    and os.path.exists(full_path) 
                    and 'Manual' in full_path 
                    and 'ScriptReference' not in full_path):
                    links.append(full_path)
                    self.visited_links.add(full_path)
        
        return links

    def create_pdf(self):
        html_files = []
        start_file = os.path.join(self.docs_folder, 'UnityManual.html')
        
        if not os.path.exists(start_file):
            self.logger.error(f"Starting file not found: {start_file}")
            return
        
        to_visit = [start_file]
        
        # Collect first 100 HTML files
        while to_visit and len(html_files) < 35000:  # Added limit condition
            current_file = to_visit.pop(0)
            total_files = 35000  # Total number of HTML files
            current_count = len(html_files)
            percentage = (current_count / total_files) * 100
            self.logger.info(f"Processing: {current_file} ({percentage:.1f}% completed, {current_count}/{total_files} files)")
            
            soup = self.parse_html_file(current_file)
            if soup:
                html_files.append(current_file)
                to_visit.extend(self.get_links(soup, current_file))

        # Configure PDF options
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': None,
            'enable-javascript': None,
            'javascript-delay': 1000,
            'images': True,
            'no-background': True,
            'print-media-type': True,
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'quiet': ''
        }

        # Process files in smaller batches
        batch_size = 3  # Reduced to 3 files per batch
        total_files = len(html_files)
        temp_pdfs = []

        try:
            for i in range(0, total_files, batch_size):
                batch = html_files[i:i + batch_size]
                temp_pdf = f'temp_batch_{i}.pdf'
                self.logger.info(f"Generating batch {i//batch_size + 1} of {(total_files + batch_size - 1)//batch_size} ({len(batch)} pages)")
                
                pdfkit.from_file(batch, temp_pdf, options=options, configuration=self.config)
                temp_pdfs.append(temp_pdf)
                
                # Add a small delay between batches
                time.sleep(0.5)  # 1 second delay between batches

            # Merge all temporary PDFs
            import PyPDF2

            self.logger.info("Merging PDF files...")
            merger = PyPDF2.PdfMerger()
            
            for temp_pdf in temp_pdfs:
                merger.append(temp_pdf)
            
            merger.write(self.output_pdf)
            merger.close()

            # Clean up temporary files
            for temp_pdf in temp_pdfs:
                os.remove(temp_pdf)

            self.logger.info(f"PDF successfully created: {self.output_pdf}")

        except Exception as e:
            self.logger.error(f"Error creating PDF: {str(e)}")
            # Clean up any temporary files in case of error
            for temp_pdf in temp_pdfs:
                if os.path.exists(temp_pdf):
                    os.remove(temp_pdf)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Unity documentation to PDF')
    parser.add_argument('--docs-folder', type=str, required=True,
                       help='Path to Unity documentation Manual folder')
    parser.add_argument('--output', type=str, default="unity_manual.pdf",
                       help='Output PDF filename (default: unity_manual.pdf)')
    
    args = parser.parse_args()
    
    # Verify the starting file exists
    start_file = os.path.join(args.docs_folder, 'UnityManual.html')
    if not os.path.exists(start_file):
        print(f"Error: Starting file not found at {start_file}")
        print("Please verify the correct path to your Unity documentation.")
        exit(1)
        
    converter = UnityDocConverter(args.docs_folder, args.output)
    converter.create_pdf() 