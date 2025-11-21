# management/commands/fetch_freepik_icons.py
from django.core.management.base import BaseCommand
from django.conf import settings
from file_upload.client import R2Client
import requests
import logging
from ...models import SVGIcon
from datetime import datetime

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch icons from Freepik API and save to R2 storage'

    def add_arguments(self, parser):
        parser.add_argument('--page', type=int, default=1, help='Page number')
        parser.add_argument('--per_page', type=int, default=100, help='Results per page')
        parser.add_argument('--free_svg', action='store_true', help='Only fetch free SVGs')

    def get_thumbnail_data(self, url):
        """Download thumbnail data from URL"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Error downloading thumbnail: {str(e)}")
            return None

    def handle(self, *args, **options):
        try:
            # Initialize R2 client
            r2_client = R2Client()
            
            # Freepik API configuration
            api_url = 'https://api.freepik.com/v1/icons'
            headers = {
                'x-freepik-api-key': settings.FREEPIK_API_KEY
            }
            
            # Build query parameters
            params = {
                'page': options['page'],
                'per_page': options['per_page']
            }

            # Make API request
            self.stdout.write(f"Fetching icons from Freepik API (page {options['page']})...")
            response = requests.get(api_url, headers=headers, params=params)

            if response.status_code != 200:
                self.stderr.write(self.style.ERROR(
                    f'API request failed: {response.status_code} - {response.text}'
                ))
                return

            data = response.json()

            icons_created = 0
            for icon in data.get('data', []):
                try:
                    # Skip non-free SVGs if specified
                    if options['free_svg'] and not icon.get('free_svg'):
                        continue

                    # Get thumbnail
                    thumbnails = icon.get('thumbnails', [])
                    if not thumbnails or not thumbnails[0].get('url'):
                        continue

                    thumbnail_url = thumbnails[0]['url']
                    content = self.get_thumbnail_data(thumbnail_url)
                    
                    if not content:
                        continue

                    # Generate filename from icon ID
                    filename = f"freepik-icons/{icon['id']}.png"

                    print("FILENMA", filename)

                    # Upload to R2
                    cdn_url = r2_client.upload_file(
                        content,
                        filename
                    )

                    if not cdn_url:
                        logger.error(f"Failed to upload icon to R2: {filename}")
                        continue

                    # Create SVG icon record
                    created_at = datetime.strptime(icon['created'], "%Y-%m-%dT%H:%M:%Sz")
                    svg_icon = SVGIcon.objects.create(
                        title=icon['name'],
                        cdn_url=cdn_url,
                        width=thumbnails[0].get('width', 0),
                        height=thumbnails[0].get('height', 0),
                        created_at=created_at
                    )

                    icons_created += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully saved icon: {svg_icon.title} (ID: {svg_icon.id})'
                    ))

                except Exception as e:
                    logger.error(f"Error processing icon {icon.get('id')}: {str(e)}")
                    continue

            # Print summary
            pagination = data.get('meta', {}).get('pagination', {})
            self.stdout.write(self.style.SUCCESS(
                f'\nSummary:\n'
                f'Successfully created {icons_created} icons\n'
                f'Page {pagination.get("current_page")} of {pagination.get("last_page")} '
                f'(Total icons: {pagination.get("total")})'
            ))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'API request failed: {str(e)}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))