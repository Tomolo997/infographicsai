# File: yourapp/management/commands/upload_svgs_to_r2.py

import os
import uuid
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.conf import settings
from file_upload.client import R2Client
from icons.models import VectorIcon
from io import BytesIO

class Command(BaseCommand):
    help = 'Uploads SVG files to R2 storage and adds them to the VectorIcon model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--directory', '-d',
            type=str,
            default='undraw_svgs',
            help='Directory containing SVG files (default: undraw_svgs)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit the number of files to process (default: all files)'
        )
        parser.add_argument(
            '--file-format',
            type=str,
            default='SVG',
            help='File format to set in the database (default: SVG)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without actually uploading or creating database entries'
        )

    def handle(self, *args, **options):
        directory = options['directory']
        limit = options['limit']
        file_format = options['file_format']
        dry_run = options['dry_run']
        
        # Get full path to the directory
        svg_dir = os.path.join(settings.MEDIA_ROOT, directory)
        
        if not os.path.exists(svg_dir):
            self.stdout.write(self.style.ERROR(f"Directory not found: {svg_dir}"))
            return
        
        # Initialize R2 client
        r2_client = R2Client()
        
        # Get list of SVG files
        svg_files = [f for f in os.listdir(svg_dir) if f.lower().endswith('.svg')]
        
        if limit:
            svg_files = svg_files[:limit]
            
        self.stdout.write(f"Found {len(svg_files)} SVG files to process")
        
        # Process each SVG file
        for i, svg_file in enumerate(svg_files):
            try:
                file_path = os.path.join(svg_dir, svg_file)
                
                # Get SVG dimensions by parsing the file
                width, height = self.get_svg_dimensions(file_path)
                
                # Generate a title from the filename
                title = os.path.splitext(svg_file)[0].replace('_', ' ').title()
                
                # Generate a unique filename for R2
                unique_filename = f"vectors/{str(uuid.uuid4())}.svg"
                
                self.stdout.write(f"[{i+1}/{len(svg_files)}] Processing: {svg_file}")
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
                            vector_icon = VectorIcon.objects.create(
                                title=title,
                                cdn_url=cdn_url,
                                file_format=file_format
                            )
                            self.stdout.write(self.style.SUCCESS(f"  Uploaded and added to database with ID: {vector_icon.id}"))
                        else:
                            self.stdout.write(self.style.ERROR(f"  Failed to upload to R2"))
                else:
                    self.stdout.write(self.style.WARNING("  [DRY RUN] Skipping upload and database entry"))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  Error processing {svg_file}: {str(e)}"))
                continue
                
        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"Dry run completed. {len(svg_files)} files would be processed."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Processing completed. {len(svg_files)} files processed."))
            
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