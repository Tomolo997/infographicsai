from django.core.management.base import BaseCommand
import aiohttp
import asyncio
import json
from pathlib import Path
from django.conf import settings
import logging
from io import BytesIO
from file_upload.client import R2Client
from icons.models import SVGIcon, VectorIcon
from asgiref.sync import sync_to_async

from django.core.management.base import BaseCommand
import aiohttp
import asyncio
import json
from pathlib import Path
from django.conf import settings
import logging
from io import BytesIO
import xml.etree.ElementTree as ET
import re
from asgiref.sync import sync_to_async
from django.db import transaction


# Expanded Icon sources configuration
ICON_SOURCES = {
    "feather": {
        "base_url": "https://raw.githubusercontent.com/feathericons/feather/master/icons/",
        "icons": [
            # "activity.svg",
            # "airplay.svg",
            # "alert-circle.svg",
            # "alert-octagon.svg",
            # "alert-triangle.svg",
            # "align-center.svg",
            # "align-justify.svg",
            # "align-left.svg",
            # "align-right.svg",
            # "anchor.svg",
            # "aperture.svg",
            # "archive.svg",
            # "arrow-down.svg",
            # "arrow-down-circle.svg",
            # "arrow-down-left.svg",
            # "arrow-down-right.svg",
            # "arrow-left.svg",
            # "arrow-left-circle.svg",
            # "arrow-right.svg",
            # "arrow-right-circle.svg",
            # "arrow-up.svg",
            # "arrow-up-circle.svg",
            # "arrow-up-left.svg",
            # "arrow-up-right.svg",
            # "at-sign.svg",
            # "award.svg",
            # "bar-chart.svg",
            # "bar-chart-2.svg",
            # "battery.svg",
            # "battery-charging.svg",
            # "bell.svg",
            # "bell-off.svg",
            # "bluetooth.svg",
            # "bold.svg",
            "book.svg",
            "book-open.svg",
            "bookmark.svg",
            "box.svg",
            "briefcase.svg",
            "calendar.svg",
            "camera.svg",
            "camera-off.svg",
            "cast.svg",
            "check.svg",
            "check-circle.svg",
            "check-square.svg",
            "chevron-down.svg",
            "chevron-left.svg",
            "chevron-right.svg",
            "chevron-up.svg",
            "chrome.svg",
            "circle.svg",
            "clipboard.svg",
            "clock.svg",
            "cloud.svg",
            "cloud-drizzle.svg",
            "cloud-lightning.svg",
            "cloud-off.svg",
            "cloud-rain.svg",
            "cloud-snow.svg",
            "code.svg",
            "codepen.svg",
            "codesandbox.svg",
            "coffee.svg",
            "columns.svg",
            "command.svg",
            "compass.svg",
            "copy.svg",
            "corner-down-left.svg",
            "corner-down-right.svg",
            "corner-left-down.svg",
            "corner-left-up.svg",
            "corner-right-down.svg",
            "corner-right-up.svg",
            "corner-up-left.svg",
            "corner-up-right.svg",
            "cpu.svg",
            "credit-card.svg",
            "crop.svg",
            "crosshair.svg",
            "database.svg",
            "delete.svg",
            "disc.svg",
            "divide.svg",
            "divide-circle.svg",
            "divide-square.svg",
            "dollar-sign.svg",
            "download.svg",
            "download-cloud.svg",
            "dribbble.svg",
            "droplet.svg",
            "edit.svg",
            "edit-2.svg",
            "edit-3.svg",
            "external-link.svg",
            "eye.svg",
            "eye-off.svg",
            "facebook.svg",
            "fast-forward.svg",
            "feather.svg",
            "figma.svg",
            "file.svg",
            "file-minus.svg",
            "file-plus.svg",
            "file-text.svg",
            "film.svg",
            "filter.svg",
            "flag.svg",
            "folder.svg",
            "folder-minus.svg",
            "folder-plus.svg",
            "framer.svg",
            "frown.svg",
            "gift.svg",
            "git-branch.svg",
            "git-commit.svg",
            "git-merge.svg",
            "git-pull-request.svg",
            "github.svg",
            "gitlab.svg",
            "globe.svg",
            "grid.svg",
            "hard-drive.svg",
            "hash.svg",
            "headphones.svg",
            "heart.svg",
            "help-circle.svg",
            "hexagon.svg",
            "home.svg",
            "image.svg",
            "inbox.svg",
            "info.svg",
            "instagram.svg",
            "italic.svg",
            "key.svg",
            "layers.svg",
            "layout.svg",
            "life-buoy.svg",
            "link.svg",
            "link-2.svg",
            "linkedin.svg",
            "list.svg",
            "loader.svg",
            "lock.svg",
            "log-in.svg",
            "log-out.svg",
            "mail.svg",
            "map.svg",
            "map-pin.svg",
            "maximize.svg",
            "maximize-2.svg",
            "meh.svg",
            "menu.svg",
            "message-circle.svg",
            "message-square.svg",
            "mic.svg",
            "mic-off.svg",
            "minimize.svg",
            "minimize-2.svg",
            "minus.svg",
            "minus-circle.svg",
            "minus-square.svg",
            "monitor.svg",
            "moon.svg",
            "more-horizontal.svg",
            "more-vertical.svg",
            "mouse-pointer.svg",
            "move.svg",
            "music.svg",
            "navigation.svg",
            "navigation-2.svg",
            "octagon.svg",
            "package.svg",
            "paperclip.svg",
            "pause.svg",
            "pause-circle.svg",
            "pen-tool.svg",
            "percent.svg",
            "phone.svg",
            "phone-call.svg",
            "phone-forwarded.svg",
            "phone-incoming.svg",
            "phone-missed.svg",
            "phone-off.svg",
            "phone-outgoing.svg",
            "pie-chart.svg",
            "play.svg",
            "play-circle.svg",
            "plus.svg",
            "plus-circle.svg",
            "plus-square.svg",
            "pocket.svg",
            "power.svg",
            "printer.svg",
            "radio.svg",
            "refresh-ccw.svg",
            "refresh-cw.svg",
            "repeat.svg",
            "rewind.svg",
            "rotate-ccw.svg",
            "rotate-cw.svg",
            "rss.svg",
            "save.svg",
            "scissors.svg",
            "search.svg",
            "send.svg",
            "server.svg",
            "settings.svg",
            "share.svg",
            "share-2.svg",
            "shield.svg",
            "shield-off.svg",
            "shopping-bag.svg",
            "shopping-cart.svg",
            "shuffle.svg",
            "sidebar.svg",
            "skip-back.svg",
            "skip-forward.svg",
            "slack.svg",
            "slash.svg",
            "sliders.svg",
            "smartphone.svg",
            "smile.svg",
            "speaker.svg",
            "square.svg",
            "star.svg",
            "stop-circle.svg",
            "sun.svg",
            "sunrise.svg",
            "sunset.svg",
            "tablet.svg",
            "tag.svg",
            "target.svg",
            "terminal.svg",
            "thermometer.svg",
            "thumbs-down.svg",
            "thumbs-up.svg",
            "toggle-left.svg",
            "toggle-right.svg",
            "tool.svg",
            "trash.svg",
            "trash-2.svg",
            "trello.svg",
            "trending-down.svg",
            "trending-up.svg",
            "triangle.svg",
            "truck.svg",
            "tv.svg",
            "twitch.svg",
            "twitter.svg",
            "type.svg",
            "umbrella.svg",
            "underline.svg",
            "unlock.svg",
            "upload.svg",
            "upload-cloud.svg",
            "user.svg",
            "user-check.svg",
            "user-minus.svg",
            "user-plus.svg",
            "user-x.svg",
            "users.svg",
            "video.svg",
            "video-off.svg",
            "voicemail.svg",
            "volume.svg",
            "volume-1.svg",
            "volume-2.svg",
            "volume-x.svg",
            "watch.svg",
            "wifi.svg",
            "wifi-off.svg",
            "wind.svg",
            "x.svg",
            "x-circle.svg",
            "x-octagon.svg",
            "x-square.svg",
            "youtube.svg",
            "zap.svg",
            "zap-off.svg",
            "zoom-in.svg",
            "zoom-out.svg",
        ],
    },
    "heroicons": {
        "base_url": "https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/",
        "icons": [
            # "academic-cap.svg",
            # "adjustments-horizontal.svg",
            # "adjustments-vertical.svg",
            # "archive-box.svg",
            # "archive-box-arrow-down.svg",
            # "archive-box-x-mark.svg",
            # "arrow-down.svg",
            # "arrow-down-circle.svg",
            # "arrow-down-left.svg",
            # "arrow-down-on-square.svg",
            # "arrow-down-right.svg",
            # "arrow-down-tray.svg",
            # "arrow-left.svg",
            # "arrow-left-circle.svg",
            # "arrow-left-on-rectangle.svg",
            # "arrow-long-down.svg",
            # "arrow-long-left.svg",
            # "arrow-long-right.svg",
            # "arrow-long-up.svg",
            # "arrow-path.svg",
            # "arrow-path-rounded-square.svg",
            # "arrow-right.svg",
            # "arrow-right-circle.svg",
            # "arrow-right-on-rectangle.svg",
            # "arrow-small-down.svg",
            # "arrow-small-left.svg",
            # "arrow-small-right.svg",
            # "arrow-small-up.svg",
            # "arrow-top-right-on-square.svg",
            # "arrow-trending-down.svg",
            # "arrow-trending-up.svg",
            # "arrow-up.svg",
            "arrow-up-circle.svg",
            "arrow-up-left.svg",
            "arrow-up-on-square.svg",
            "arrow-up-right.svg",
            "arrow-up-tray.svg",
            "arrow-uturn-down.svg",
            "arrow-uturn-left.svg",
            "arrow-uturn-right.svg",
            "arrow-uturn-up.svg",
            "arrows-pointing-in.svg",
            "arrows-pointing-out.svg",
            "arrows-right-left.svg",
            "arrows-up-down.svg",
            "at-symbol.svg",
            "backspace.svg",
            "backward.svg",
            "banknotes.svg",
            "bars-2.svg",
            "bars-3.svg",
            "bars-3-bottom-left.svg",
            "bars-3-bottom-right.svg",
            "bars-3-center-left.svg",
            "bars-4.svg",
            "bars-arrow-down.svg",
            "bars-arrow-up.svg",
            "battery-0.svg",
            "battery-50.svg",
            "battery-100.svg",
            "beaker.svg",
            "bell.svg",
            "bell-alert.svg",
            "bell-slash.svg",
            "bell-snooze.svg",
            "bolt.svg",
            "bolt-slash.svg",
            "book-open.svg",
            "bookmark.svg",
            "bookmark-slash.svg",
            "bookmark-square.svg",
            "briefcase.svg",
            "bug-ant.svg",
            "building-library.svg",
            "building-office.svg",
            "building-office-2.svg",
            "building-storefront.svg",
            "cake.svg",
            "calculator.svg",
            "calendar.svg",
            "calendar-days.svg",
            "camera.svg",
            "chart-bar.svg",
            "chart-bar-square.svg",
            "chart-pie.svg",
            "chat-bubble-bottom-center.svg",
            "chat-bubble-bottom-center-text.svg",
            "chat-bubble-left.svg",
            "chat-bubble-left-ellipsis.svg",
            "chat-bubble-left-right.svg",
            "chat-bubble-oval-left.svg",
            "chat-bubble-oval-left-ellipsis.svg",
            "check.svg",
            "check-badge.svg",
            "check-circle.svg",
            "chevron-double-down.svg",
            "chevron-double-left.svg",
            "chevron-double-right.svg",
            "chevron-double-up.svg",
            "chevron-down.svg",
            "chevron-left.svg",
            "chevron-right.svg",
            "chevron-up.svg",
            "chevron-up-down.svg",
            "circle-stack.svg",
            "clipboard.svg",
            "clipboard-document.svg",
            "clipboard-document-check.svg",
            "clipboard-document-list.svg",
            "clock.svg",
            "cloud.svg",
            "cloud-arrow-down.svg",
            "cloud-arrow-up.svg",
            "code-bracket.svg",
            "code-bracket-square.svg",
            "cog.svg",
            "cog-6-tooth.svg",
            "cog-8-tooth.svg",
            "command-line.svg",
            "computer-desktop.svg",
            "cpu-chip.svg",
            "credit-card.svg",
            "cube.svg",
            "cube-transparent.svg",
            "currency-bangladeshi.svg",
            "currency-dollar.svg",
            "currency-euro.svg",
            "currency-pound.svg",
            "currency-rupee.svg",
            "currency-yen.svg",
            "cursor-arrow-rays.svg",
            "cursor-arrow-ripple.svg",
            "device-phone-mobile.svg",
            "device-tablet.svg",
            "document.svg",
            "document-arrow-down.svg",
            "document-arrow-up.svg",
            "document-chart-bar.svg",
            "document-check.svg",
            "document-duplicate.svg",
            "document-magnifying-glass.svg",
            "document-minus.svg",
            "document-plus.svg",
            "document-text.svg",
            "ellipsis-horizontal.svg",
            "ellipsis-horizontal-circle.svg",
            "ellipsis-vertical.svg",
            "envelope.svg",
            "envelope-open.svg",
            "exclamation-circle.svg",
            "exclamation-triangle.svg",
            "eye.svg",
            "eye-dropper.svg",
            "eye-slash.svg",
            "face-frown.svg",
            "face-smile.svg",
            "film.svg",
            "finger-print.svg",
            "fire.svg",
            "flag.svg",
            "folder.svg",
            "folder-arrow-down.svg",
            "folder-minus.svg",
            "folder-open.svg",
            "folder-plus.svg",
            "forward.svg",
            "funnel.svg",
            "gif.svg",
            "gift.svg",
            "gift-top.svg",
            "globe-alt.svg",
            "globe-americas.svg",
            "globe-asia-australia.svg",
            "globe-europe-africa.svg",
            "hand-raised.svg",
            "hand-thumb-down.svg",
            "hand-thumb-up.svg",
            "hashtag.svg",
            "heart.svg",
            "home.svg",
            "home-modern.svg",
            "identification.svg",
            "inbox.svg",
            "inbox-arrow-down.svg",
            "inbox-stack.svg",
            "information-circle.svg",
            "key.svg",
            "language.svg",
            "lifebuoy.svg",
            "light-bulb.svg",
            "link.svg",
            "list-bullet.svg",
            "lock-closed.svg",
            "lock-open.svg",
            "magnifying-glass.svg",
            "magnifying-glass-circle.svg",
            "magnifying-glass-minus.svg",
            "magnifying-glass-plus.svg",
            "map.svg",
            "map-pin.svg",
            "megaphone.svg",
            "microphone.svg",
            "minus.svg",
            "minus-circle.svg",
            "minus-small.svg",
            "moon.svg",
            "musical-note.svg",
            "newspaper.svg",
            "no-symbol.svg",
            "paint-brush.svg",
            "paper-airplane.svg",
            "paper-clip.svg",
            "pause.svg",
            "pause-circle.svg",
            "pencil.svg",
            "pencil-square.svg",
            "phone.svg",
            "phone-arrow-down-left.svg",
            "phone-arrow-up-right.svg",
            "phone-x-mark.svg",
            "photo.svg",
            "play.svg",
            "play-circle.svg",
            "play-pause.svg",
            "plus.svg",
            "plus-circle.svg",
            "plus-small.svg",
            "power.svg",
            "presentation-chart-bar.svg",
            "presentation-chart-line.svg",
            "printer.svg",
            "puzzle-piece.svg",
            "qr-code.svg",
            "question-mark-circle.svg",
            "queue-list.svg",
            "radio.svg",
            "receipt-percent.svg",
            "receipt-refund.svg",
            "rectangle-group.svg",
            "rectangle-stack.svg",
            "rocket-launch.svg",
            "rss.svg",
            "scale.svg",
            "scissors.svg",
            "server.svg",
            "server-stack.svg",
            "share.svg",
            "shield-check.svg",
            "shield-exclamation.svg",
            "shopping-bag.svg",
            "shopping-cart.svg",
            "signal.svg",
            "signal-slash.svg",
            "sparkles.svg",
            "speaker-wave.svg",
            "speaker-x-mark.svg",
            "square-2-stack.svg",
            "square-3-stack-3d.svg",
            "squares-2x2.svg",
            "squares-plus.svg",
            "star.svg",
            "stop.svg",
            "stop-circle.svg",
            "sun.svg",
            "swatch.svg",
            "table-cells.svg",
            "tag.svg",
            "ticket.svg",
            "trash.svg",
            "trophy.svg",
            "truck.svg",
            "tv.svg",
            "user.svg",
            "user-circle.svg",
            "user-group.svg",
            "user-minus.svg",
            "user-plus.svg",
            "users.svg",
            "variable.svg",
            "video-camera.svg",
            "video-camera-slash.svg",
            "view-columns.svg",
            "viewfinder-circle.svg",
            "wallet.svg",
            "wifi.svg",
            "window.svg",
            "wrench.svg",
            "wrench-screwdriver.svg",
            "x-circle.svg",
            "x-mark.svg",
        ],
    },
}


class Command(BaseCommand):
    help = 'Downloads icons from various sources, uploads to R2, and saves to database'

    def __init__(self):
        super().__init__()
        self.setup_logging()
        self.r2_client = R2Client()
        self.icons_to_create = []  # Buffer for bulk creation

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def get_svg_dimensions(self, svg_content: str) -> tuple:
        """Extract width and height from SVG content"""
        try:
            # Create a new parser for each call to avoid potential threading issues
            parser = ET.XMLParser()
            root = ET.fromstring(svg_content, parser=parser)
            
            # Try to get dimensions from viewBox first
            viewbox = root.get('viewBox')
            if viewbox:
                try:
                    _, _, width, height = map(float, viewbox.split())
                    return int(width), int(height)
                except (ValueError, TypeError):
                    pass

            # Try width and height attributes
            width = root.get('width')
            height = root.get('height')
            
            if width and height:
                # Remove any units (px, etc.)
                width = re.sub(r'[^0-9.]', '', width)
                height = re.sub(r'[^0-9.]', '', height)
                return int(float(width)), int(float(height))

            # Default dimensions if nothing found
            return 24, 24

        except Exception as e:
            self.logger.error(f"Error parsing SVG dimensions: {str(e)}")
            return 24, 24

    @sync_to_async
    def save_icon_to_db(self, icon_data: dict):
        """Save icon to database"""
        try:
            with transaction.atomic():
                if icon_data['file_type'] == 'svg':
                    icon = SVGIcon(
                        title=icon_data['title'],
                        cdn_url=icon_data['url'],
                        width=icon_data['width'],
                        height=icon_data['height']
                    )
                else:
                    icon = VectorIcon(
                        title=icon_data['title'],
                        cdn_url=icon_data['url'],
                        file_format=icon_data['file_format']
                    )
                icon.save()
            return True
        except Exception as e:
            self.logger.error(f"Error saving to database: {str(e)}")
            return False

    async def download_and_process_icon(self, session: aiohttp.ClientSession, source: str, icon_name: str, base_url: str):
        """Download an icon, upload to R2, and save to database"""
        url = base_url + icon_name
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    binary_content = await response.read()
                    
                    # Create a file-like object
                    file_obj = BytesIO(binary_content)
                    file_obj.content_type = 'image/svg+xml'
                    
                    # Create the R2 path
                    r2_path = f"icons/{source}/{icon_name}"
                    
                    # Upload to R2
                    uploaded_url = await sync_to_async(self.r2_client.upload_file)(file_obj, r2_path)
                    
                    if uploaded_url:
                        # Get icon dimensions
                        width, height = await sync_to_async(self.get_svg_dimensions)(content)
                        
                        # Prepare the title
                        title = icon_name.replace('.svg', '').replace('-', ' ').title()
                        
                        # Prepare icon data
                        icon_data = {
                            'title': title,
                            'url': uploaded_url,
                            'width': width,
                            'height': height,
                            'file_type': 'svg' if icon_name.lower().endswith('.svg') else 'vector',
                            'file_format': icon_name.split('.')[-1].upper()
                        }
                        
                        # Save to database
                        saved = await self.save_icon_to_db(icon_data)
                        
                        if saved:
                            self.logger.info(f'Processed: {icon_name} - Uploaded to R2 and saved to database')
                            return {
                                'name': icon_name,
                                'source': source,
                                'url': uploaded_url,
                                'width': width,
                                'height': height,
                                'success': True
                            }
                        else:
                            return {
                                'name': icon_name,
                                'source': source,
                                'success': False,
                                'error': 'Database save failed'
                            }
                    else:
                        self.logger.error(f'Failed to upload {icon_name} to R2')
                        return {
                            'name': icon_name,
                            'source': source,
                            'success': False,
                            'error': 'Upload failed'
                        }
                else:
                    self.logger.error(f'Failed to download {icon_name}: Status {response.status}')
                    return {
                        'name': icon_name,
                        'source': source,
                        'success': False,
                        'error': f'Download failed with status {response.status}'
                    }
        except Exception as e:
            self.logger.error(f'Error processing {icon_name}: {str(e)}')
            return {
                'name': icon_name,
                'source': source,
                'success': False,
                'error': str(e)
            }

    async def process_all_icons(self):
        """Process all icons"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for source, config in ICON_SOURCES.items():
                for icon in config['icons']:
                    task = self.download_and_process_icon(session, source, icon, config['base_url'])
                    tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            return results

    @sync_to_async
    def clear_existing_icons(self):
        """Clear existing icons from database"""
        SVGIcon.objects.all().delete()
        VectorIcon.objects.all().delete()

    @sync_to_async
    def get_database_counts(self):
        """Get current database counts"""
        return {
            'svg_icons': SVGIcon.objects.count(),
            'vector_icons': VectorIcon.objects.count()
        }

    async def handle_async(self, *args, **options):
        """Async handler for the command"""
        try:
            # Clear existing records if needed
            if options.get('clear_existing'):
                await self.clear_existing_icons()
                self.stdout.write(self.style.SUCCESS('Cleared existing icons'))

            # Process all icons
            results = await self.process_all_icons()
            
            # Calculate statistics
            total_icons = len(results)
            successful = sum(1 for r in results if r['success'])
            failed = total_icons - successful
            
            # Get database counts
            db_counts = await self.get_database_counts()
            
            # Generate report
            report = {
                'total_processed': total_icons,
                'successful': successful,
                'failed': failed,
                'by_source': {},
                'database_counts': db_counts
            }
            
            # Break down by source
            for result in results:
                source = result['source']
                if source not in report['by_source']:
                    report['by_source'][source] = {'successful': 0, 'failed': 0}
                
                if result['success']:
                    report['by_source'][source]['successful'] += 1
                else:
                    report['by_source'][source]['failed'] += 1
            
            return report

        except Exception as e:
            self.logger.error(f'Command failed: {str(e)}')
            raise e

    def handle(self, *args, **options):
        """Command entry point"""
        report = asyncio.run(self.handle_async(*args, **options))
        
        # Print report
        self.stdout.write(self.style.SUCCESS(f"\nIcon Processing Report:"))
        self.stdout.write(f"Total Processed: {report['total_processed']}")
        self.stdout.write(self.style.SUCCESS(f"Successfully Uploaded: {report['successful']}"))
        if report['failed'] > 0:
            self.stdout.write(self.style.ERROR(f"Failed: {report['failed']}"))
        
        self.stdout.write("\nDatabase Status:")
        self.stdout.write(f"SVG Icons: {report['database_counts']['svg_icons']}")
        self.stdout.write(f"Vector Icons: {report['database_counts']['vector_icons']}")
        
        self.stdout.write("\nBreakdown by Source:")
        for source, stats in report['by_source'].items():
            self.stdout.write(f"\n{source}:")
            self.stdout.write(self.style.SUCCESS(f"  Successful: {stats['successful']}"))
            if stats['failed'] > 0:
                self.stdout.write(self.style.ERROR(f"  Failed: {stats['failed']}"))

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing icons before importing'
        )