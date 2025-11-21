from django.core.management.base import BaseCommand
from icons.models import SVGIcon, VectorIcon, FlatIcon, Pattern

class Command(BaseCommand):
    help = 'Changes all CDN URLs from R2 to the new domain'

    def handle(self, *args, **options):
        old_domain = "https://pub-ff5ad7b8238547eb868d9a8b58244c30.r2.dev"
        new_domain = "https://images.ainfographic.com"
        
        # Update SVGIcon models
        svg_icons = SVGIcon.objects.filter(cdn_url__contains=old_domain)
        svg_count = svg_icons.count()
        for icon in svg_icons:
            icon.cdn_url = icon.cdn_url.replace(old_domain, new_domain)
            icon.save()
        
        # Update VectorIcon models
        vector_icons = VectorIcon.objects.filter(cdn_url__contains=old_domain)
        vector_count = vector_icons.count()
        for icon in vector_icons:
            icon.cdn_url = icon.cdn_url.replace(old_domain, new_domain)
            icon.save()
        
        # Update FlatIcon models
        flat_icons = FlatIcon.objects.filter(cdn_url__contains=old_domain)
        flat_count = flat_icons.count()
        for icon in flat_icons:
            icon.cdn_url = icon.cdn_url.replace(old_domain, new_domain)
            icon.save()
        
        # Update Pattern models
        patterns = Pattern.objects.filter(cdn_url__contains=old_domain)
        pattern_count = patterns.count()
        for pattern in patterns:
            pattern.cdn_url = pattern.cdn_url.replace(old_domain, new_domain)
            pattern.save()
        
        # Report results
        total_updated = svg_count + vector_count + flat_count + pattern_count
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {total_updated} URLs:'))
        self.stdout.write(f'  - SVG Icons: {svg_count}')
        self.stdout.write(f'  - Vector Icons: {vector_count}')
        self.stdout.write(f'  - Flat Icons: {flat_count}')
        self.stdout.write(f'  - Patterns: {pattern_count}')
