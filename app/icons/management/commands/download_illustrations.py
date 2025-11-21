# File: yourapp/management/commands/download_undraw_svgs.py

import os
import json
import requests
import re
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Downloads all SVGs from undraw.co illustrations page'

    def add_arguments(self, parser):
        parser.add_argument(
            '--page', 
            type=int,
            default=None,
            help='Specific page number to download (default: all pages)'
        )
        parser.add_argument(
            '--start-page',
            type=int, 
            default=1,
            help='Page number to start downloading from (default: 1)'
        )
        parser.add_argument(
            '--directory', '-d',
            type=str,
            default='undraw_svgs',
            help='Directory to save SVGs (default: undraw_svgs)'
        )
        parser.add_argument(
            '--max-pages',
            type=int,
            default=None,
            help='Maximum number of pages to scrape (default: all available)'
        )

    def handle(self, *args, **options):
        page = options['page']
        start_page = options['start_page']
        directory = options['directory']
        max_pages = options['max_pages']
        
        # Ensure the directory exists
        download_dir = os.path.join(settings.MEDIA_ROOT, directory)
        os.makedirs(download_dir, exist_ok=True)
        
        if page is not None:
            # Download a specific page
            self.download_page(page, download_dir)
        else:
            # Download all pages, starting from start_page
            current_page = start_page
            total_pages = None
            
            while total_pages is None or current_page <= total_pages:
                if max_pages and current_page > start_page + max_pages - 1:
                    self.stdout.write(self.style.SUCCESS(f"Reached maximum pages limit ({max_pages} pages from start page)"))
                    break
                    
                page_info = self.download_page(current_page, download_dir)
                
                if not page_info:
                    self.stdout.write(self.style.ERROR(f"Failed to download page {current_page}"))
                    break
                
                total_pages = page_info['total_pages']
                self.stdout.write(self.style.SUCCESS(f"Processed page {current_page}/{total_pages}"))
                current_page += 1

    def download_page(self, page_num, download_dir):
        if page_num == 1:
            url=f"https://undraw.co/illustrations"
        else:
            url = f"https://undraw.co/illustrations/{page_num}"
        self.stdout.write(f"Fetching content from {url}...")
        
        try:
            # Send request with browser-like headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Extract JSON data from the page
            json_data = self.extract_json_data(response.text)
            if not json_data:
                self.stdout.write(self.style.ERROR("Could not find JSON data in the page"))
                return None
                
            illustrations = json_data.get('props', {}).get('pageProps', {}).get('illustrations', [])
            current_page = json_data.get('props', {}).get('pageProps', {}).get('currentPage', page_num)
            total_pages = json_data.get('props', {}).get('pageProps', {}).get('totalPages', 0)
            
            if not illustrations:
                self.stdout.write(self.style.ERROR("No illustrations found in the JSON data"))
                return None
                
            self.stdout.write(f"Found {len(illustrations)} illustrations on page {current_page}")
            
            # Download each SVG
            for index, illustration in enumerate(illustrations):
                media_url = illustration.get('media')
                title = illustration.get('title')
                
                if not media_url:
                    continue
                    
                # Create a filename from the title or use the last part of the URL
                if title:
                    # Remove any characters that are not allowed in filenames
                    filename = re.sub(r'[^\w\-_. ]', '_', title).replace(' ', '_').lower() + '.svg'
                else:
                    filename = os.path.basename(media_url)
                
                # Download the SVG
                svg_response = requests.get(media_url, headers=headers)
                if svg_response.status_code == 200:
                    file_path = os.path.join(download_dir, filename)
                    with open(file_path, 'wb') as file:
                        file.write(svg_response.content)
                    self.stdout.write(f"  [{index+1}/{len(illustrations)}] Downloaded: {filename}")
                else:
                    self.stdout.write(self.style.WARNING(f"  [{index+1}/{len(illustrations)}] Failed to download: {media_url}"))
            
            return {
                'current_page': current_page,
                'total_pages': total_pages
            }
            
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching URL: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
            
        return None
            
    def extract_json_data(self, html_content):
        """Extract the JSON data embedded in the Next.js page"""
        pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
        match = re.search(pattern, html_content, re.DOTALL)
        
        if match:
            json_str = match.group(1)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                return None
        
        return None