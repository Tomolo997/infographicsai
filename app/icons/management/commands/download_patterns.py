from django.core.management.base import BaseCommand
from django.db import transaction
import logging
from pathlib import Path
from icons.models import Pattern

class Command(BaseCommand):
    help = 'Creates Pattern entries from existing R2 files'

    def __init__(self):
        super().__init__()
        self.setup_logging()
        self.base_url = "https://images.ainfographic.com/patterns/"
        self.pattern_files = [
            "beanstalk.png",
            "blue-snow.webp",
            "canadian-dollar.webp",
            "checkerboard-cross.webp",
            "chevron.webp",
            "christmas-colour.png",
            "circles-dark.webp",
            "circles-light.webp",
            "circuit.png",
            "country-quilt.png",
            "criss-cross.webp",
            "crossline-dots.webp",
            "crossline-lines.webp",
            "dot-grid.webp",
            "dust_scratches.webp",
            "dynamic-style.webp",
            "email-pattern.png",
            "embossed-diamond.webp",
            "fishnets-and-hearts.webp",
            "floor-tile.png",
            "folk-pattern.png",
            "funky-lines.webp",
            "gravel.png",
            "greek-vase.webp",
            "halftone-yellow.webp",
            "herringbone.webp",
            "hotel-wallpaper.webp",
            "houndstooth-pattern.webp",
            "hypnotize.webp",
            "interlaced.png",
            "intersection.webp",
            "just-waves.webp",
            "leaves.webp",
            "let-there-be-sun.webp",
            "light-veneer.webp",
            "lilypads.webp",
            "memphis-mini.webp",
            "moroccan-flower.png",
            "morocco.png",
            "oriental.webp",
            "papyrus.png",
            "pipes.webp",
            "pixel-heart.webp",
            "regal.webp",
            "repeated-square.webp",
            "ripples.png",
            "round.webp",
            "so-white.png",
            "spikes.webp",
            "spiration-light.webp",
            "stonehaven.webp",
            "stripes-light.webp",
            "sun-pattern.webp",
            "tic-tac-toe.webp",
            "tiny-squares.webp",
            "trees.webp",
            "triangle-mosaic.webp",
            "united-squares-negative.webp",
            "united-squares.png",
            "wavy-dots.webp",
            "webb.png",
            "what-the-hex.png",
            "white-waves.webp",
            "y-so-serious-white.png"
        ]

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing patterns before creating new ones'
        )

    def create_pattern(self, filename: str) -> bool:
        """Create a single Pattern entry"""
        try:
            # Convert filename to title (e.g., "blue-snow.webp" -> "Blue Snow")
            title = filename.replace('.webp', '').replace('.png', '').replace('-', ' ').title()
            cdn_url = self.base_url + filename
            file_format = Path(filename).suffix[1:].upper()

            with transaction.atomic():
                Pattern.objects.create(
                    title=title,
                    cdn_url=cdn_url,
                    file_format=file_format
                )
            return True
        except Exception as e:
            self.logger.error(f"Error creating Pattern for {filename}: {str(e)}")
            return False

    def handle(self, *args, **options):
        """Command entry point"""
        try:
            # Clear existing if requested
            if options.get('clear_existing'):
                Pattern.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('Cleared existing patterns'))

            successful = 0
            failed = 0

            # Process each file
            for filename in self.pattern_files:
                if self.create_pattern(filename):
                    successful += 1
                    self.stdout.write(self.style.SUCCESS(f'Created Pattern for {filename}'))
                else:
                    failed += 1
                    self.stdout.write(self.style.ERROR(f'Failed to create Pattern for {filename}'))

            # Print report
            self.stdout.write(self.style.SUCCESS(f"\nPattern Creation Report:"))
            self.stdout.write(f"Total Processed: {len(self.pattern_files)}")
            self.stdout.write(self.style.SUCCESS(f"Successfully Created: {successful}"))
            if failed > 0:
                self.stdout.write(self.style.ERROR(f"Failed: {failed}"))

            self.stdout.write("\nDatabase Status:")
            self.stdout.write(f"Total Patterns: {Pattern.objects.count()}")

        except Exception as e:
            self.logger.error(f'Command failed: {str(e)}')
            raise e