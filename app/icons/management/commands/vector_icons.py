from django.core.management.base import BaseCommand
from django.db import transaction
import logging
from pathlib import Path
from icons.models import SVGIcon, VectorIcon

class Command(BaseCommand):
    help = 'Creates VectorIcon entries from existing R2 files'

    def __init__(self):
        super().__init__()
        self.setup_logging()
        self.base_url = "https://images.ainfographic.com/download_vectors/"
        self.vector_files = [
            "undraw_arched-arrow.svg",
            "undraw_arrow.svg",
            "undraw_asterisk.svg",
            "undraw_asymmetric-lines.svg",
            "undraw_asymmetric-parallels.svg",
            "undraw_balloon.svg",
            "undraw_bike.svg",
            "undraw_bird.svg",
            "undraw_camera.svg",
            "undraw_chat-text.svg",
            "undraw_chat.svg",
            "undraw_check.svg",
            "undraw_chevrons.svg",
            "undraw_circled-arrow (1).svg",
            "undraw_circled-arrow.svg",
            "undraw_circled-plus.svg",
            "undraw_circled-x.svg",
            "undraw_clock.svg",
            "undraw_cloud-upload.svg",
            "undraw_cloud.svg",
            "undraw_code.svg",
            "undraw_coffee.svg",
            "undraw_command-button.svg",
            "undraw_command-line.svg",
            "undraw_cupcake.svg",
            "undraw_curved-underline.svg",
            "undraw_dashed-arrow.svg",
            "undraw_dashed-underline.svg",
            "undraw_double-underline.svg",
            "undraw_empty-note.svg",
            "undraw_envelope.svg",
            "undraw_escape-button.svg",
            "undraw_flower.svg",
            "undraw_fun-arrow.svg",
            "undraw_fun-star.svg",
            "undraw_fun-underline.svg",
            "undraw_ghost.svg",
            "undraw_heart-fun.svg",
            "undraw_heart.svg",
            "undraw_ice-cream.svg",
            "undraw_love.svg",
            "undraw_note.svg",
            "undraw_parenthesis.svg",
            "undraw_party-hat.svg",
            "undraw_party-streamer.svg",
            "undraw_person.svg",
            "undraw_pointer.svg",
            "undraw_rocket.svg",
            "undraw_screen-pointer.svg",
            "undraw_smiley-face.svg",
            "undraw_spiral.svg",
            "undraw_square-bracket.svg",
            "undraw_star.svg",
            "undraw_sticky-note.svg",
            "undraw_straight-arrow.svg",
            "undraw_three-lines.svg",
            "undraw_tree.svg",
            "undraw_two-lines.svg",
            "undraw_underline.svg",
            "undraw_x-mark.svg"
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
            help='Clear existing vector icons before creating new ones'
        )

    def create_vector_icon(self, filename: str) -> bool:
        """Create a single VectorIcon entry"""
        try:
            title = filename.replace('undraw_', '').replace('.svg', '').replace('-', ' ').title()
            cdn_url = self.base_url + filename
            file_format = Path(filename).suffix[1:].upper()

            with transaction.atomic():
                VectorIcon.objects.create(
                    title=title,
                    cdn_url=cdn_url,
                    file_format=file_format
                )
            return True
        except Exception as e:
            self.logger.error(f"Error creating VectorIcon for {filename}: {str(e)}")
            return False

    def handle(self, *args, **options):
        """Command entry point"""
        try:
            # Clear existing if requested
            if options.get('clear_existing'):
                VectorIcon.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('Cleared existing vector icons'))

            successful = 0
            failed = 0

            # Process each file
            for filename in self.vector_files:
                if self.create_vector_icon(filename):
                    successful += 1
                    self.stdout.write(self.style.SUCCESS(f'Created VectorIcon for {filename}'))
                else:
                    failed += 1
                    self.stdout.write(self.style.ERROR(f'Failed to create VectorIcon for {filename}'))

            # Print report
            self.stdout.write(self.style.SUCCESS(f"\nVector Icon Creation Report:"))
            self.stdout.write(f"Total Processed: {len(self.vector_files)}")
            self.stdout.write(self.style.SUCCESS(f"Successfully Created: {successful}"))
            if failed > 0:
                self.stdout.write(self.style.ERROR(f"Failed: {failed}"))

            self.stdout.write("\nDatabase Status:")
            self.stdout.write(f"Total Vector Icons: {VectorIcon.objects.count()}")

        except Exception as e:
            self.logger.error(f'Command failed: {str(e)}')
            raise e