#!/usr/bin/env python3
"""Extract text from PowerPoint files using zipfile and xml parsing"""
import zipfile
import xml.etree.ElementTree as ET
import sys
import re

def extract_text_from_pptx(pptx_path):
    """Extract all text from a PowerPoint file"""
    # PPTX files are zip archives
    with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
        # Get list of slide files
        slide_files = [f for f in zip_ref.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
        slide_files.sort(key=lambda x: int(re.search(r'slide(\d+)', x).group(1)))

        print(f"Total slides: {len(slide_files)}\n")

        for slide_file in slide_files:
            slide_num = re.search(r'slide(\d+)', slide_file).group(1)
            print(f"{'='*60}")
            print(f"SLIDE {slide_num}")
            print(f"{'='*60}")

            # Read the XML content
            xml_content = zip_ref.read(slide_file)

            # Parse XML
            root = ET.fromstring(xml_content)

            # Define namespaces
            namespaces = {
                'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
                'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
            }

            # Find all text elements
            texts = []
            for t in root.findall('.//a:t', namespaces):
                if t.text and t.text.strip():
                    texts.append(t.text)

            # Print text grouped by paragraphs
            if texts:
                current_para = []
                for text in texts:
                    current_para.append(text)

                # Join and print
                full_text = ''.join(current_para)
                # Split by likely paragraph breaks
                paragraphs = re.split(r'\n+', full_text)
                for para in paragraphs:
                    if para.strip():
                        print(para.strip())
                        print()
            else:
                print("[No text content]")

            print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: extract_pptx_text.py <file.pptx>")
        sys.exit(1)

    extract_text_from_pptx(sys.argv[1])
