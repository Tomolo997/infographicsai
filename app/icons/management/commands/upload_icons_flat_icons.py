# File: yourapp/management/commands/upload_svgs_to_r2.py

import os
import uuid
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.conf import settings
from file_upload.client import R2Client
from icons.models import SVGIcon
from io import BytesIO

class Command(BaseCommand):
    help = 'Uploads SVG files to R2 storage and adds them to the SVGIcon model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--directory', '-d',
            type=str,
            default='SVG',
            help='Directory containing SVG files (default: SVG)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit the number of files to process (default: all files)'
        )
        parser.add_argument(
            '--category',
            type=str,
            default=None,
            help='Process only a specific category folder (default: all categories)'
        )
        parser.add_argument(
            '--start-category',
            type=str,
            default=None,
            help='Start processing from this category and continue alphabetically'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without actually uploading or creating database entries'
        )

    def handle(self, *args, **options):
        directory = options['directory']
        limit = options['limit']
        category = options['category']
        start_category = options['start_category']
        dry_run = options['dry_run']
        
        # Get full path to the base directory
        svg_base_dir = os.path.join(settings.MEDIA_ROOT, directory)
        
        if not os.path.exists(svg_base_dir):
            self.stdout.write(self.style.ERROR(f"Directory not found: {svg_base_dir}"))
            return
        
        # Initialize R2 client
        r2_client = R2Client()
        
        # Collect all SVG files with their categories
        svg_files_info = []
        
        # Get all available categories
        all_categories = sorted([d for d in os.listdir(svg_base_dir) if os.path.isdir(os.path.join(svg_base_dir, d))])
        
        # Determine which categories to process
        if category:
            # If specific category is requested
            categories = [category] if category in all_categories else []
        elif start_category:
            # If start category is provided, process from that point onwards
            try:
                start_index = all_categories.index(start_category)
                categories = all_categories[start_index:]
                self.stdout.write(f"Starting from category '{start_category}', processing {len(categories)} categories")
            except ValueError:
                self.stdout.write(self.style.ERROR(f"Start category not found: {start_category}"))
                categories = []
        else:
            # Otherwise process all categories
            categories = all_categories
        
        for cat in categories:
            cat_path = os.path.join(svg_base_dir, cat)
            
            # Skip if not a directory
            if not os.path.isdir(cat_path):
                continue
                
            self.stdout.write(f"Processing category: {cat}")
            
            # Get all SVG files in this category
            for file in os.listdir(cat_path):
                if file.lower().endswith('.svg'):
                    svg_files_info.append({
                        'file': file,
                        'category': cat,
                        'path': os.path.join(cat_path, file)
                    })
        
        # Apply limit if specified
        if limit:
            svg_files_info = svg_files_info[:limit]
            
        self.stdout.write(f"Found {len(w)} SVG files to process")
        
        # Process each SVG file
        total_success = 0
        for i, file_info in enumerate(svg_files_info):
            try:
                svg_file = file_info['file']
                category = file_info['category']
                file_path = file_info['path']
                
                # Get SVG dimensions by parsing the file
                width, height = self.get_svg_dimensions(file_path)
                
                # Generate a title from the filename, including category
                base_name = os.path.splitext(svg_file)[0]
                title = f"{category} - {base_name.replace('_', ' ').replace('-', ' ').title()}"
                
                # Generate a unique filename for R2
                unique_filename = f"svg_icons/{category}/{str(uuid.uuid4())}.svg"
                
                self.stdout.write(f"[{i+1}/{len(svg_files_info)}] Processing: {svg_file}")
                self.stdout.write(f"  Category: {category}")
                self.stdout.write(f"  Title: {title}")
                self.stdout.write(f"  Dimensions: {width}x{height}")
                self.stdout.write(f"  R2 Path: {unique_filename}")
                
                if not dry_run:
                    # Open the file and upload to R2
                    with open(file_path, 'rb') as file_obj:
                        file_content = file_obj.read()
                        
                        # Create a BytesIO object to mimic a file object
                        file_obj_for_upload = BytesIO(file_content)
                        file_obj_for_upload.content_type = 'image/svg+xml'
                        
                        # Upload to R2
                        cdn_url = r2_client.upload_file(file_obj_for_upload, unique_filename)
                        
                        if cdn_url:
                            # Create database entry
                            svg_icon = SVGIcon.objects.create(
                                title=title,
                                cdn_url=cdn_url,
                                width=width,
                                height=height
                            )
                            self.stdout.write(self.style.SUCCESS(f"  Uploaded and added to database with ID: {svg_icon.id}"))
                            total_success += 1
                        else:
                            self.stdout.write(self.style.ERROR(f"  Failed to upload to R2"))
                else:
                    self.stdout.write(self.style.WARNING("  [DRY RUN] Skipping upload and database entry"))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  Error processing {file_info['file']}: {str(e)}"))
                continue
                
        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"Dry run completed. {len(svg_files_info)} files would be processed."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Processing completed. {total_success} of {len(svg_files_info)} files processed successfully."))
            
    def get_svg_dimensions(self, svg_path):
        """Extract width and height from SVG file"""
        try:
            # Parse SVG file
            tree = ET.parse(svg_path)
            root = tree.getroot()
            
            # Try to get width and height attributes
            width = root.get('width')
            height = root.get('height')
            
            # If width/height not found, try to get from viewBox
            if not width or not height:
                viewbox = root.get('viewBox')
                if viewbox:
                    # viewBox format: "min-x min-y width height"
                    parts = viewbox.split()
                    if len(parts) >= 4:
                        width = float(parts[2])
                        height = float(parts[3])
            
            # Convert to integers if possible
            try:
                width = int(float(width)) if width else 800
                height = int(float(height)) if height else 600
            except (ValueError, TypeError):
                width = 800
                height = 600
                
            return width, height
            
        except Exception as e:
            # Default values if parsing fails
            return 800, 600