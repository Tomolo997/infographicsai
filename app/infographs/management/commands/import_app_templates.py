"""
Django management command to import template images from app/templates/app_templates
and save them to R2 storage, then create Template objects in the database.

This command:
- Scans the app/templates/app_templates directory for image files
- Uploads each image to R2 storage
- Extracts aspect ratio from image dimensions
- Creates Template objects with is_public=True

Usage:
    python manage.py import_app_templates
"""

import os
from io import BytesIO
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from PIL import Image
from infographs.models import Template, AspectRatio
from file_upload.client import R2Client


def calculate_aspect_ratio(width: int, height: int) -> str:
    """
    Calculate the closest matching aspect ratio from AspectRatio choices.
    
    Args:
        width: Image width in pixels
        height: Image height in pixels
    
    Returns:
        str: Aspect ratio string matching AspectRatio choices
    """
    if width == 0 or height == 0:
        return AspectRatio.NINE_ONE_SIX  # Default
    
    ratio = width / height
    
    # Define aspect ratios with their approximate values
    aspect_ratios = {
        AspectRatio.NINE_ONE_SIX: 9 / 16,      # 0.5625
        AspectRatio.ONE_ONE: 1 / 1,              # 1.0
        AspectRatio.FOUR_FIVE: 4 / 5,            # 0.8
        AspectRatio.SIXTEEN_NINE: 16 / 9,       # 1.777...
        AspectRatio.TWENTY_ONE_NINE: 21 / 9,     # 2.333...
        AspectRatio.THREE_TWO: 3 / 2,            # 1.5
        AspectRatio.FOUR_THREE: 4 / 3,           # 1.333...
        AspectRatio.TWO_THREE: 2 / 3,            # 0.666...
    }
    
    # Find the closest match
    closest_ratio = AspectRatio.NINE_ONE_SIX
    min_diff = float('inf')
    
    for aspect_ratio_str, aspect_ratio_value in aspect_ratios.items():
        diff = abs(ratio - aspect_ratio_value)
        if diff < min_diff:
            min_diff = diff
            closest_ratio = aspect_ratio_str
    
    return closest_ratio


def get_content_type(file_path: str) -> str:
    """
    Get MIME content type based on file extension.
    
    Args:
        file_path: Path to the file
    
    Returns:
        str: MIME content type
    """
    extension = Path(file_path).suffix.lower()
    content_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.webp': 'image/webp',
    }
    return content_types.get(extension, 'image/png')


class Command(BaseCommand):
    help = "Import template images from app/templates/app_templates to R2 and create Template objects"

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Skip templates that already exist (by name)',
        )
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update existing templates with new image URLs',
        )

    def handle(self, *args, **options):
        # Get the templates directory
        # BASE_DIR is at app/ level, templates are at app/templates/app_templates
        base_dir = Path(settings.BASE_DIR)
        templates_dir = base_dir / 'templates' / 'app_templates'
        
        if not templates_dir.exists():
            self.stdout.write(
                self.style.ERROR(f"Templates directory not found: {templates_dir}")
            )
            return
        
        # Find all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        image_files = [
            f for f in templates_dir.iterdir()
            if f.is_file() and f.suffix.lower() in image_extensions
        ]
        
        if not image_files:
            self.stdout.write(
                self.style.WARNING(f"No image files found in {templates_dir}")
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(f"Found {len(image_files)} image file(s) to process")
        )
        
        # Initialize R2 client
        r2_client = R2Client()
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        error_count = 0
        
        for image_file in sorted(image_files):
            try:
                # Extract template name from filename (remove extension)
                template_name = image_file.stem.replace('_', ' ').title()
                # If it's like "template_11", make it "Template 11"
                if template_name.startswith('Template '):
                    template_name = template_name.replace('Template ', 'Template ')
                
                # Check if template already exists
                existing_template = Template.objects.filter(name=template_name).first()
                
                if existing_template:
                    if options['skip_existing']:
                        self.stdout.write(
                            self.style.WARNING(
                                f"⏭️  Skipping {image_file.name} - template '{template_name}' already exists"
                            )
                        )
                        skipped_count += 1
                        continue
                    elif not options['update_existing']:
                        self.stdout.write(
                            self.style.WARNING(
                                f"⏭️  Skipping {image_file.name} - template '{template_name}' already exists. "
                                f"Use --update-existing to update or --skip-existing to skip"
                            )
                        )
                        skipped_count += 1
                        continue
                
                # Open image to get dimensions
                self.stdout.write(f"📷 Processing {image_file.name}...")
                
                with Image.open(image_file) as img:
                    width, height = img.size
                    aspect_ratio = calculate_aspect_ratio(width, height)
                    
                    self.stdout.write(
                        f"   Dimensions: {width}x{height}, Aspect Ratio: {aspect_ratio}"
                    )
                
                # Read file for upload
                with open(image_file, 'rb') as f:
                    file_data = BytesIO(f.read())
                
                # Set content type
                content_type = get_content_type(str(image_file))
                file_data.content_type = content_type  # type: ignore[attr-defined]
                file_data.seek(0)
                
                # Upload to R2
                file_extension = image_file.suffix.lower().lstrip('.')
                if not file_extension:
                    file_extension = 'png'
                
                r2_filename = f"templates/app_templates/{image_file.name}"
                self.stdout.write(f"   Uploading to R2: {r2_filename}...")
                
                image_url = r2_client.upload_file(file_data, r2_filename)
                
                if not image_url:
                    raise Exception("R2 upload failed - no URL returned")
                
                self.stdout.write(f"   ✅ Uploaded to: {image_url}")
                
                # Create or update Template
                template_data = {
                    'image_url': image_url,
                    'aspect_ratio': aspect_ratio,
                    'is_public': True,
                    'account': None,  # Public templates have no account
                    'description_json': {
                        'source': 'app_templates',
                        'original_filename': image_file.name,
                        'dimensions': {
                            'width': width,
                            'height': height,
                        },
                    },
                }
                
                if existing_template and options['update_existing']:
                    # Update existing template
                    for key, value in template_data.items():
                        setattr(existing_template, key, value)
                    existing_template.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"   ✅ Updated template: {template_name} (ID: {existing_template.pk})"
                        )
                    )
                    updated_count += 1
                else:
                    # Create new template
                    template = Template.objects.create(
                        name=template_name,
                        **template_data
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"   ✅ Created template: {template_name} (ID: {template.pk})"
                        )
                    )
                    created_count += 1
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"   ❌ Error processing {image_file.name}: {str(e)}"
                    )
                )
                error_count += 1
                continue
        
        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("Import Summary:"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"✅ Created: {created_count}")
        self.stdout.write(f"🔄 Updated: {updated_count}")
        self.stdout.write(f"⏭️  Skipped: {skipped_count}")
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f"❌ Errors: {error_count}"))
        self.stdout.write("=" * 60)
        
        if created_count > 0 or updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✓ Successfully processed {created_count + updated_count} template(s)!"
                )
            )

